import html.entities
import time

import base64
import hashlib
import os
import re
from scrapy import signals
from scrapy.http import Request, TextResponse
from scrapy.selector import XPathSelector
from scrapy.signalmanager import dispatcher
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Spider
from scrapy.utils.misc import arg_to_iter

import skuscraper.settings as skuscraper_settings
from skuscraper import akamai
from skuscraper import log_details
from skuscraper import settings
from skuscraper.items import Garment
from scrapy.linkextractors import LinkExtractor
from skuscraper.utils.colours import SORTED_COLOURS
from skuscraper.utils.generate_crawl_id import generate_crawl_id
from ..parsers.currencyparser import CurrencyParser, CurrencyParseException
from ..parsers.jsparser import JSParser


def reset_cookies(request):
    request.meta['dont_merge_cookies'] = True
    request.cookies = {}
    return request


def _sanitize(input_val):
    """ Shorthand for sanitizing results, removing unicode whitespace and normalizing end result"""
    if isinstance(input_val, XPathSelector):
        # caller obviously wants clean extracted version
        to_clean = input_val.extract()
    else:
        to_clean = input_val

    return re.sub('\s+', ' ', to_clean.replace('\xa0', ' ')).strip()


def clean(lst_or_str):
    """ Shorthand for sanitizing results in an iterable, dropping ones which would end empty """
    if not isinstance(lst_or_str, str) and getattr(lst_or_str, '__iter__', False):  # if iterable and not a string like
        return [x for x in (_sanitize(y) for y in lst_or_str if y is not None) if x]
    return _sanitize(lst_or_str)


sanitize = clean


def remove_jsession(url):
    return re.sub(';jsessionid=[^&?/]+', '', url, re.I)


def slugify(bad_str, prefix=None):
    """ Make url/mongo friendly slug from string. """
    slug = re.sub('_+', '_', re.sub('[^a-z0-9-_]', '_', bad_str.lower()))
    if prefix:
        return (prefix + '_' + slug).rstrip('_')
    return slug.rstrip('_')


def tokenize(lst_or_str):
    """
        Splits string or list of strings into set of lowercase word tokens.
    """
    if not isinstance(lst_or_str, str):
        to_convert = ' '.join(lst_or_str)
    else:
        to_convert = lst_or_str

    return set(re.split('\W+', to_convert.lower(), flags=re.U))


class BaseSpiderMixin:
    # while it is not necessary belong here, this template is very commonly used
    html_t = '<html><body>%s</body></html>'

    REGEX_QUOTE_R = re.compile('([.+*\|\(\)\[\]\}\{])')
    max_retries = 3

    def merge_products(self, items):
        merged_products = {}
        for item in items:
            if item['retailer_sku'] in merged_products:
                merged_products[item['retailer_sku']]['skus'].update(item['skus'])
                for image in item['image_urls']:
                    if image not in merged_products[item['retailer_sku']]['image_urls']:
                        merged_products[item['retailer_sku']]['image_urls'] += [image]
            else:
                merged_products[item['retailer_sku']] = item

        return list(merged_products.values())

    def quote_regex(self, str_to_quote):
        """
            Quotes regex special characters so resulting string could be included into regex
            without any side effects.

            Added as member function as its use is common for brand/name separation
        """

        return self.REGEX_QUOTE_R.sub(r'\\\1', str_to_quote)

    def initialize_mixins(self):
        self.seen_ids = set()
        self.seen_product_sale_pairs = set()
        self.seen_product_ids = set()
        self.seen_urls = set()

        # Override market/flash_sales from env if provided
        if hasattr(self, 'market'):
            self.market = os.environ.get('retailer_market', self.market)

        if hasattr(self, 'flash_sales') and 'retailer_is_flash_sales' in os.environ:
            self.flash_sales = os.environ['retailer_is_flash_sales'].lower() == 'true'

        self.crawl_id = settings.CRAWL_ID or generate_crawl_id(self.retailer)
        self.logger.info("initialising %s. crawl id: %s" % (self.__class__, self.crawl_id))

    def product_hash(self, unique_identifier):
        return str(hashlib.sha1(unique_identifier.encode('utf-8')).hexdigest()[0:24])

    def hash_and_b64encode(self, plain_text):
        hash_bytes = hashlib.sha1(plain_text.encode('utf-8')).digest()
        b64_text = base64.urlsafe_b64encode(hash_bytes)
        return b64_text.decode().strip("=")

    def utc_now(self):
        """Return utc epoch timestamp.
        Send the epoch integer across the wire and convert back to datetime at deque time,
        as JSON cannot serialize datetime objects.
        """
        return int(time.time())

    def to_timestamp(self, datetime_object):
        """
            Convert a datetime object *relative to local timezone* to a (int) timestamp.
        """
        return int(time.mktime(datetime_object.utctimetuple()))

    def unescape(self, text):
        """
            Removes HTML or XML character references and entities from a text string.
            From http://effbot.org/zone/re-sub.htm#unescape-html
        """

        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return chr(int(text[3:-1], 16))
                    else:
                        return chr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = chr(html.entities.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text  # leave as is

        return re.sub("&#?\w+;", fixup, text)

    def text_from_html(self, partial_html, xpath=''):
        """
            partial_html: unicode. Packed string will not be handled correctly
            xpath: specific expression to extract
        """
        html = self.html_t % partial_html
        response = TextResponse('', body=html, encoding='utf-8')
        return clean(response.xpath(xpath or '//text()'))

    def elevate_request_priority(self, request):
        request.priority += 1
        return request

    def retry_request(self, response, callback=None):
        callback = callback or self.parse
        retries = response.meta.get('retries', 0)

        if retries < self.max_retries:
            self.logger.info(response.url + " [Retry Attempt: %i]" % (retries + 1))
            meta = response.meta
            meta['retries'] = retries + 1
            return Request(url=response.url, callback=callback, headers=response.request.headers,
                           method=response.request.method, body=response.request.body,
                           meta=meta, dont_filter=True)

        self.logger.info(response.url + " [Giving up retry]")
        return


class BaseParseSpider(Spider, BaseSpiderMixin):
    one_size = 'One Size'

    care_materials = [
        'polyamide', 'polyester', 'lycra', 'silk', 'cotton', 'nylon', 'spandex',
        'wool', 'leather', 'spandex', 'cashmere', 'linen', 'viscose', 'elastane',
        'textile', 'polyurethan', 'synthetic', 'acrylic', 'rayon', 'polyester',
        'rubber', 'vinyl', 'latex', 'lyocell', 'stainless steel', 'wood', 'lambskin',
        'metal', 'plastic', 'suede', 'shearling', 'denim', 'poly', 'flyknit', 'snakeskin', 'mesh',
        'ponte', 'poylester', 'palyacryl', 'acryl', 'sheepskin', 'satin', 'calfskin',

        # German
        'leder', 'textil', 'kunststoff', 'wolle', 'elasthan', 'futter', 'elastische', 'synthetik',

        # Swedish
        'acetat', 'akryl', 'ankdun', 'fjädrar', 'fjäder', 'bomull', 'cupro', 'elastan',
        'jute', 'gummi', 'kashmir',
        'läder', 'linne', 'lurex', 'lykra', 'lyocel', 'metallfiber', 'mocka', 'modal',
        'neopren', 'nyull', 'papperstrå', 'päls',
        'polyamid', 'polyetser', 'polyolefin', 'polyster', 'polypropen', 'polyuretan', 'pvc',
        'rami', 'siden', 'silikon', 'skinn', 'syntetiskt hår', 'polyuréthane',
        'ull', 'viskos',

        # Finnish (often trimmed to match more cases)
        'akryylia', 'angoraa', 'elastaan', 'höyheniä',
        'modaal', 'kashmirista', 'lykraa', 'mohair', 'mokasta',
        'nahkaa', 'nahasta', 'nailon', 'paperia', 'pellava',
        'polyolefiinia', 'polyamiidia', 'polyeserist', 'polypropeenist',
        'polyuretaania', 'raionia', 'raffiaa', 'silkkiä', 'synteettiä',
        'tekstiiliä', 'tencellistä', 'villaa', 'villasta', 'viskoos',

        # Danish
        'algodón', 'andedun', 'andefjer', 'bast', 'bomuld', 'canvas', 'gedhår', 'fjer', 'hør',
        'lammelæder', 'lammeuld', 'læder', 'lino', 'kunstpels', 'merino', 'papirstrå', 'polyacryl',
        'poliéster', 'polyrethan', 'ruskind', 'skind', 'syntetiske', 'tekstil', 'tencel',

        # Norwegian (not matched in Danish/Sweden)
        'fjær', 'keramiske', 'kanvas', 'lær', 'mokka',

        # Portuguese
        'composi\xe7\xe3o', 'tecido', 'algodao', 'algodão',

        # french
        'coton', 'cuir', 'synthetique', 'laine',

        # Czech
        'polyamid', 'hedvábí', 'bavlna', 'vlna', 'kůže', 'kašmír', 'prádlo', 'viskóza',
        'elastan', 'textilní', 'polyuretan', 'syntetický', 'akryl',
        'umělé hedvábí', 'guma', 'nerezová ocel', 'dřevo',

        # Polish
        'poliamid', 'poliester', 'jedwab', 'bawełna', 'wełna', 'rzemienny', 'kaszmir', 'bielizna',
        'wiskoza', 'elastan', 'włókienniczy', 'poliuretan', 'syntetyczny', 'akryl', 'sztuczny jedwab',
        'poliester', 'gumowy', 'płyta winylowa', 'lateks', 'stal nierdzewna', 'drewno',

        # Russian
        'хлопок', 'полиэстер', 'эластан', 'нейлон', 'полиуретан', 'положении', 'mатериал', 'хлопок',
        'кожа', 'меринос', 'pезина', 'текстиль', 'состав',

        # Korean
        '제품소재', '폴리아미드', '코튼', '가죽', '코', '엘라스테인', '폴리에스테르', '리넨', '폴리프로필렌',  # Product Materials

        # Hungarian
        'viszkóz', 'pamut', 'poliészter', 'elasztán', 'poliuretán', 'gumi', 'szintetikus',

        # Italian
        'seta', 'lana', 'capretto', 'scamosciato',

        # Turkish
        'pamuk', 'deri', 'akrilik', 'poliamit', 'viskoz', 'naylon',

        # Dutch
        'materiaal', 'katoen',

        # Chinese
        '材质成分', '锦纶', '棉', '材质成分', '聚氨酯', '聚酯纤维', '面料', '材质', '魔术贴', '橡胶', '革', '合成',

        # Japanese
        'コットン', 'ナイロン', '革', 'ポリウレタン', 'ポリエステル', 'ポリプロピレン', '麻', 'ポリ塩化ビニル',
    ]

    care_wash = [
        'do not wash', 'cannot be washed', 'machine wash', 'hand wash', 'do not iron',
        "don't iron", 'do not bleach', "don't bleach", 'warm iron', 'gentle cycle',
        'wash dark colours separatedly', 'wash dark colors separatedly', 'specialist cleaning',
        'professional cleaning', 'dry clean', 'tumble dry', 'iron on low', 'wipe clean',
        'wash cold', 'cool wash', 'sponge clean', 'dishwasher safe', 'safe for dishwasher',
        'machine-wash', 'iron at', 'no use of dryer', 'hang dry', 'hang to dry', 'reshape whilst damp',
        'line drying', 'iron with medium', 'low temp.', 'high temp.', 'handwash', 'wash method',

        # German
        'waschung', 'trockner', 'maschinenw', 'chemisch reinigen', 'trockner nicht verwenden',
        'mittlerer Stufe bügeln', 'zum trocknen aufhängen', 'nicht bleichen', 'bei höchsttemperatur bügeln',
        'bei niedriger temperatur bügeln', 'trockner niedrig', 'handwäsche', 'wasinstructies', 'wassen',

        # Swedish
        'endast tvätt', 'handtvätt', 'kemtvätt', 'maskintvätt', 'tvättas separat', 'skontvätt',

        # Finnish
        'käsinpesua', 'konepesu',

        # Danish
        'håndvask',
        'maskinvask',
        'maskinevaskes',
        'stryges',

        # Norwegian
        'strykes',

        # French
        'laver à',
        'lavable en machine', 'lavage à la main', 'traitement au chlore interdi', 'sèche-linge interdit',
        'repasser', 'nettoyage',

        # Korean
        '세탁 및 취급 주의사항',  # Washing and Handling Precautions

        # Hungarian
        'Mosás',

        # Russian
        'стирка', 'химчистка',

        # Italian
        'lavabile in lavatrice',
        'lavare',  # Wash
        'lavatrice',  # Washing Machine

        # Dutch
        'wasvoorschriften',

        # Chinese
        '机洗', '漂白', '手洗', '干洗',
        
        # Chille
        'lavado', 'lavar', 'secado', 'lejía', 'cloro', 'cuidar'
    ]

    GENDER_MAP = [
        # token, gender, to be matched in this order
        # adding more records is not advised; there will be side effects
        ('woman', 'women'),
        ('women', 'women'),
        ('womens', 'women'),
        ('ladies', 'women'),
        ('man', 'men'),
        ('men', 'men'),
        ('mens', 'men'),
        ('him', 'men'),
        ('maternity', 'women'),
        ('her', 'women'),
        ('boy', 'boys'),
        ('boys', 'boys'),
        ('girl', 'girls'),
        ('girls', 'girls'),
        ('kid', 'unisex-kids'),
        ('kids', 'unisex-kids'),
        ('baby', 'unisex-kids'),
        ('babies', 'unisex-kids'),
        ('toddler', 'unisex-kids'),
        ('toddlers', 'unisex-kids'),
        ('newborn', 'unisex-kids'),
        ('children', 'unisex-kids'),
        ('unisex', 'unisex-adults'),
    ]

    def __init__(self, *args, **kwargs):
        super(BaseParseSpider, self).__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseParseSpider, cls).from_crawler(crawler, *args, **kwargs)
        start_urls = kwargs.get("start_urls", [])
        if start_urls:
            spider.start_urls = start_urls

        spider.initialize_mixins()

        return spider

    def _sanitize(self, thestr):
        """ For compatibility """
        return _sanitize(thestr)

    def sanitize(self, lst_or_str):
        """ For compatibility """
        return clean(lst_or_str)

    def care_criteria(self, copy_line):
        """
            True if copy_line looks like product care/composition.
            Detection is extremely naive and is expected to miss some cases by definition
        """
        copy_lc = copy_line.lower()
        if re.search('^(?:hand)made (?:in|from)\s', copy_lc, re.I):
            return True

        if any(x in copy_lc for x in self.care_materials) and '%' in copy_lc:
            return True

        if any(x in copy_lc for x in self.care_wash):
            return True

        return False

    def care_criteria_simplified(self, copy_line):
        """
            True if copy_line looks like product care/composition, with a bit more
            relaxed criteria as compared to care_criteria.
            Detection is extremely naive and is expected to miss some cases by definition
        """
        copy_lc = copy_line.lower()

        if any(x in copy_lc for x in self.care_materials):
            return True

        if any(x in copy_lc for x in self.care_wash):
            return True

        return False

    def preset_attributes(self):
        return {x: getattr(self, x) for x in ('lang', 'gender', 'outlet')
                if hasattr(self, x) and (isinstance(getattr(self, x), str) or
                                         isinstance(getattr(self, x), bool))}

    def new_garment(self, sku_id):
        return Garment(retailer_sku=sku_id, **self.preset_attributes())

    def new_unique_garment(self, sku_id):
        """
            Slightly less ugly shorthand for garment creation and duplication check.

            Returns new Garment instance if provided :sku_id has not been used before.
            Otherwise None is returned.

            If spider instance has lang, gender or outlet attributes,
            these are applied to garment as well.

            Typical usage:

                garment = self.new_unique_garment(self.product_id(hxs)
                if garment is None:
                    return
        """
        if sku_id in self.seen_ids:
            return None

        self.seen_ids.add(sku_id)

        return self.new_garment(sku_id)

    def new_unique_garment_sale(self, retailer_product_id, sale_id):
        """This should only be used for flash sales sites.
        I.e. when we do care about seeing a product multiple times, as we want
        to see it in every sale that it features in.
        """
        if (retailer_product_id, sale_id) in self.seen_product_sale_pairs:
            return None

        self.seen_product_sale_pairs.add((retailer_product_id, sale_id))
        return self.new_garment(retailer_product_id)

    def out_of_stock(self, hxs, response):
        return False

    def out_of_stock_garment(self, response, sku_id):
        """ Return an out-of-stock garment. """

        garment = Garment(out_of_stock=True,
                          date=self.utc_now(),
                          url=response.url,
                          retailer=self.retailer,
                          market=self.market,
                          retailer_sku=sku_id,
                          product_hash=self.product_hash(self.retailer + '_' + sku_id),
                          crawl_id=self.crawl_id,
                          gender=response.meta.get('gender'),
                          industry=response.meta.get('industry'))

        # this will override gender in meta
        garment.update(self.preset_attributes())

        return garment

    def out_of_stock_item(self, hxs, response, sku_id):
        """
            Return an out-of-stock item.

            It will attempt to extract product_name, pricing and currency to fill into oos item
        """
        garment = self.out_of_stock_garment(response, sku_id)

        try:
            garment['name'] = self.product_name(hxs)
        except:
            pass

        try:
            garment['brand'] = self.product_brand(hxs)
        except:
            pass

        try:
            garment['care'] = self.product_care(hxs)
        except:
            pass

        try:
            garment['description'] = self.product_description(hxs)
        except:
            pass

        try:
            garment['category'] = self.product_category(hxs)
        except:
            pass

        try:
            _, garment['price'], garment['currency'] = self.product_pricing_new(hxs)
        except:
            pass

        try:
            # should work for about half of reasonable spiders for reasonable sites
            garment['image_urls'] = self.image_urls(hxs)
        except:
            pass

        return garment

    def canonical_url(self, hxs):
        canonical_rel = hxs.xpath('//link[@rel="canonical"]/@href').extract()
        if canonical_rel:
            return canonical_rel[0]

        og_content = hxs.xpath('//meta[@property="og:url"]/@content').extract()
        if og_content:
            return og_content[0]

        return None

    def product_category(self, hxs):
        return []

    def product_brand(self, hxs):
        return self.retailer

    def get_product_hash_text(self, garment):
        if type(garment['retailer_sku']) == bytes:
            garment['retailer_sku'] = garment['retailer_sku'].decode()
        return '{0}_{1}'.format(garment['retailer'], garment['retailer_sku'])

    def generate_product_hash_for_garment(self, garment):
        text = self.get_product_hash_text(garment)
        return self.product_hash(text)

    def boilerplate_minimal(self, garment, response, url=''):
        """ Hides extra boring stuff which is the same for almost any spider"""
        passed_meta = ('uuid', 'trail', 'gender', 'category', 'industry')

        for meta in passed_meta:
            garment.setdefault(meta, response.meta.get(meta))

        garment['url'] = url or response.url
        garment['date'] = self.utc_now()

        garment['market'] = self.market
        garment['retailer'] = self.retailer

        garment['product_hash'] = self.generate_product_hash_for_garment(garment)

        garment['crawl_id'] = self.crawl_id

    def boilerplate(self, garment, response, url=''):
        self.boilerplate_minimal(garment, response, url=url)

        canonical_url = self.canonical_url(response)
        if canonical_url:
            garment['url_original'] = garment['url']
            if canonical_url.find('://') != -1:
                garment['url'] = canonical_url
            else:
                garment['url'] = response.urljoin(canonical_url)

    def boilerplate_normal(self, garment, response):
        """ Hides nearly all assignments """
        self.boilerplate(garment, response)

        garment['brand'] = self.product_brand(response)
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)

        category = self.product_category(response)
        if not garment['category']:
            garment['category'] = category

    def garment_or_next_colour(self, garment, callback=None):
        callback = callback or self.parse
        if garment['sku_urls']:
            request = Request(garment['sku_urls'].pop(),
                              meta=dict(garment=garment),
                              dont_filter=True, callback=callback)

            return [self.elevate_request_priority(request)]

        garment.pop('sku_urls')
        return garment

    def detect_colour(self, colour_str):
        try:
            colours = self.SORTED_COLOURS
        except AttributeError:
            colours = SORTED_COLOURS

        for test_colour in colours:
            if re.search('(^|\s)%s(\s+|$)' % test_colour, colour_str, re.I | re.U):
                return test_colour
        return ''

    def detect_colour_from_name(self, hxs):
        return self.detect_colour(self.product_name(hxs))

    def detect_gender_from_tokens(self, tokens, gender_map=[]):
        """ Naive gender detection, for last resort use. """
        for token, gender in gender_map or self.GENDER_MAP:
            if token in tokens:
                return gender
                # intentionally returning nothing

    def detect_gender(self, str_or_iterable, gender_map=[]):
        return self.detect_gender_from_tokens(tokenize(str_or_iterable), gender_map)

    def detect_gender_from_name(self, hxs, gender_map=[]):
        name = self.product_name(hxs)
        return self.detect_gender(name, gender_map)

    def next_request_or_garment(self, garment, drop_meta=True):
        """
            Assuming that ['meta']['requests_queue'] contains queue of prepared requests,
            to be processed from right to left
        """
        if not 'meta' in garment:
            return garment

        if garment['meta']['requests_queue']:
            request = garment['meta']['requests_queue'].pop()
            request.meta.setdefault('garment', garment)
            return [self.elevate_request_priority(request)]

        garment['meta'].pop('requests_queue')
        if drop_meta or not garment['meta']:
            garment.pop('meta')
        return garment

    def magento_product_id(self, hxs):
        """ All Magento sites seem to have same element for product id """
        return hxs.xpath('//input[@name="product"]/@value').extract()[0]

    def magento_product_data(self, hxs):
        """ Typical Magento JS payload extraction """
        script = hxs.xpath('//script[contains(., "var spConfig =")]/text()').extract()
        if script:
            raw_data = re.findall('new Product\.Config\((.*)\);', script[0])[0]
            return JSParser('x = ' + raw_data)['x']

    def magento_product_map(self, spConfig):
        product_map = {}

        for attr in spConfig['attributes'].values():
            for dimension in attr['options']:
                dimension['name'] = attr['label']
                for product_id in dimension['products']:
                    product = product_map.setdefault(product_id, [])
                    product += [dimension]

        return product_map

    def magento_pricing(self, hxs):
        script = hxs.xpath('//script[contains(.,"var optionsPrice")]/text()').extract()[0]
        raw_data = re.search('.*?(\{.*\}).*', script).group(1)
        price_data = JSParser('x = ' + raw_data)['x']

        previous_price = CurrencyParser.float_conversion(price_data['productOldPrice'])
        price = CurrencyParser.float_conversion(price_data['productPrice'])

        if not previous_price or previous_price == price:
            previous_price = None

        return previous_price, price

    def extract_prices(self, hxs, xpath, sale_first=False, post_process=None):
        # See extract_all_prices for multile discounts case
        money_string = clean(hxs.xpath(xpath).extract())
        if post_process:
            money_string = post_process(money_string)

        currency, price = CurrencyParser.currency_and_price(money_string[0 if sale_first else -1])

        previous_price = None
        if len(money_string) > 1:
            pmoney_string = money_string[-1 if sale_first else 0]
            # sometimes currency is only present for previous price
            if currency:
                previous_price = CurrencyParser.lowest_price(pmoney_string)
            else:
                currency, previous_price = CurrencyParser.currency_and_price(pmoney_string)

        return previous_price, price, currency

    def extract_all_prices(self, hxs, xpath, process_value=None):
        """
        Args:
            xpath(str): defines all nodes containing nodes similar to price

            process_value (Optional[function]): applied to all string results of xpath

        Returns:
            list of integers, of prices in cents. Order is the same as in XPath selector results

        Raises IndexError on no prices extracted.
        """

        money_strs = clean(hxs.xpath(xpath).extract())
        if not money_strs:
            raise IndexError('Provided XPath yields no usable results')

        currencies = set()
        prices = []
        for money_str in money_strs:
            if process_value:
                money_str = process_value(money_str)

            currency, price = CurrencyParser.currency_and_price(money_str)

            if currency:
                currencies.add(currency)

            prices.append(price)

        if len(currencies) > 1:
            raise CurrencyParseException('Multiple currencies are detected in single pricing set')

        currency = currencies.pop() if currencies else None

        return prices, currency

    def product_pricing(self, hxs):
        """
            Expects price_x in parse spider or mixin.

            Takes care of usual pricing issues, save for rare case where regular price is
            indeed greater than previous price.

        """
        previous_price, price, currency = self.extract_prices(hxs, self.price_x)
        if previous_price:
            if previous_price == price:
                return None, price, currency

            if previous_price < price:
                return price, previous_price, currency

        return previous_price, price, currency

    _CURRENCY_REMAP = {
        ('CN', 'JPY'): 'CNY',
        ('AU', 'USD'): 'AUD',
        ('HK', 'USD'): 'HKD',
        ('CA', 'USD'): 'CAD',
        ('MX', 'USD'): 'MXN',
    }

    _FRENCH_FORMAT = {'FR', 'RO', 'RU'}
    _SPACE_THOUSANDS = re.compile('(\d{1,3})\s(\d{3})', re.U)

    def mangle_french_numbers(self, money_str):
        """
        A helper function to remove spaces separating thousands in numbers.
        """

        return self._SPACE_THOUSANDS.sub('\\1\\2', money_str)

    def product_pricing_common(self, hxs, xpath=None, process_value=None,
                               locale=None,
                               locale_specific=True):
        """
        Args:
            xpath (Optional[str]): defines all nodes containing nodes similar to price.
                Spider's price_x attribute is required if omitted.

            process_value (Optional[function]): applied to all string results of xpath.

            locale (Optional[str]): overrides default locale value.

            locale_specific (Optional[bool]): optional workarounds based on locale value.
                Default value is market attribute. Current implicit workarounds is locale
                specific currency for yuan and dollar, as well as preference for decimal number
                format.
        Returns:
            {
                'currency': <detected currency or None>,
                'price': <lowest price detected>,
                'previous_prices':[<list of other prices detected, sorted in reverse order>]
            '}

        Raises IndexError on no prices extracted.
        """
        common = {}
        prices = []
        price_x = xpath or self.price_x
        locale = (locale or self.market).upper()

        if not process_value and locale_specific and locale in self._FRENCH_FORMAT:
            process_value = self.mangle_french_numbers

        prices, currency = self.extract_all_prices(hxs, price_x, process_value)
        prices = list(sorted(set(prices), reverse=True))
        common['price'] = prices.pop()
        if prices:
            common['previous_prices'] = prices

        if currency and locale_specific:
            currency = self._CURRENCY_REMAP.get((locale, currency), currency)

        common['currency'] = currency

        return common

    def product_pricing_common_new(self, response, money_strs=None, post_process=None):
        common = {}
        pprices, price, currency = self.product_pricing_new(response, money_strs=money_strs, post_process=post_process)

        common['price'] = price
        common['currency'] = currency
        if pprices:
            common['previous_prices'] = pprices
        return common

    def product_pricing_new(self, response, money_strs=None, post_process=None, locale=None):
        money_strs = money_strs or []

        locale = (locale or self.market).upper()

        if hasattr(self, "price_x") and response:
            money_strs += clean(response.xpath(self.price_x).extract())
        if hasattr(self, "price_css") and response:
            money_strs += clean(response.css(self.price_css).extract())

        if not money_strs:
            raise IndexError('Provided Selector yields no usable results')

        money_strs = [str(m) for m in money_strs]

        if post_process:
            money_strs = post_process(money_strs)

        return CurrencyParser.extract_prices(money_strs, locale=locale)


class BaseCrawlSpider(CrawlSpider, BaseSpiderMixin):
    def __init__(self, *args, **kwargs):
        super(BaseCrawlSpider, self).__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseCrawlSpider, cls).from_crawler(crawler, *args, **kwargs)

        spider.initialize_mixins()
        spider.parse_spider.initialize_mixins()

        dispatcher.connect(log_details.spider_opened, signals.spider_opened)

        spider.crawler_settings = spider.custom_settings or {}

        spider.load_akamai_headers(
            akamai_headers_from_settings=spider.crawler_settings.get("akamai_headers"),
            akamai_headers_from_env_vars=os.getenv("akamai_headers"),
        )

        spider.possible_proxies = []
        try:
            spider.load_proxies()
        except Exception as e:
            spider.logger.info("Couldn't load proxies: {0}".format(e))

        return spider

    def start_requests(self):
        reqs = []
        if hasattr(self, 'start_urls_with_meta') and self.start_urls_with_meta:
            for url, meta in self.start_urls_with_meta:
                request = Request(url, meta=meta, dont_filter=True)
                reqs.append(request)
        else:
            for url in self.start_urls:
                reqs.extend(arg_to_iter(self.make_requests_from_url(url)))
        return reqs

    def add_trail(self, response):
        trail_part = [(clean(response.meta.get('link_text', '')), response.url)]
        return response.meta.get('trail', []) + trail_part

    def process_request(self, request):
        return request

    def parse(self, response):
        # pass trail, gender, category, industry etc to callback
        for request in super(BaseCrawlSpider, self).parse(response):
            if isinstance(request, Request):
                request.meta['trail'] = self.add_trail(response)
                for meta in ('gender', 'category', 'industry', 'outlet'):
                    request.meta[meta] = request.meta.get(meta) or response.meta.get(meta)

                yield request

    def parse_and_add_women(self, response):
        response.meta['gender'] = 'women'
        response.meta.pop('industry', None)
        return self.parse(response)

    def parse_and_add_men(self, response):
        response.meta['gender'] = 'men'
        response.meta.pop('industry', None)
        return self.parse(response)

    def parse_and_add_unisex_adults(self, response):
        response.meta['gender'] = 'unisex-adults'
        response.meta.pop('industry', None)
        return self.parse(response)

    def parse_and_add_children(self, response):
        response.meta['gender'] = 'children'
        response.meta.pop('industry', None)
        return self.parse(response)

    def parse_and_add_girls(self, response):
        response.meta['gender'] = 'girls'
        response.meta.pop('industry', None)
        return self.parse(response)

    def parse_and_add_boys(self, response):
        response.meta['gender'] = 'boys'
        response.meta.pop('industry', None)
        return self.parse(response)

    def parse_and_add_unisex_kids(self, response):
        response.meta['gender'] = 'unisex-kids'
        response.meta.pop('industry', None)
        return self.parse(response)

    def parse_and_reset_meta(self, response):
        """ One of uses is to counter parse_and_add_homeware,
            if other parse_and_add_* callbacks are not applicable. """
        response.meta.pop('industry', None)
        response.meta.pop('gender', None)
        return self.parse(response)

    def parse_and_add_homeware(self, response):
        response.meta['industry'] = 'homeware'
        response.meta.pop('gender', None)
        return self.parse(response)

    def parse_item(self, response):
        return self.parse_spider.parse(response)

    def process_links(self, links):
        for link in links:
            if not link.url in self.seen_urls:
                self.logger.info('listing => %s' % link.url)
                self.seen_urls.add(link.url)
        return links

    seen_product_links = set()

    def print_product_links(self, links):
        for link in links:
            if link.url not in self.seen_product_links:
                self.logger.info("product => %s" % link.url)
                self.seen_product_links.add(link.url)
        return links

    def load_akamai_headers(
            self,
            akamai_headers_from_settings=None,
            akamai_headers_from_env_vars=None,
    ):

        self.logger.info("akamai headers: from settings: {}, from env vars: {}".format(
            akamai_headers_from_settings,
            akamai_headers_from_env_vars
        ))
        # We take akamai headers from env vars first, but if there are none then we
        # fall back to crawler settings
        if akamai_headers_from_env_vars:
            akamai_headers = akamai_headers_from_env_vars
        elif akamai_headers_from_settings:
            akamai_headers = akamai_headers_from_settings
        else:
            akamai_headers = "auto"

        if akamai_headers == "never":
            self.use_akamai_headers = False
        elif akamai_headers == "always":
            self.use_akamai_headers = True
        elif akamai_headers == "auto":
            try:
                akamai_prediction = akamai.get_akamai_prediction(self)
                self.log("akamai_prediction={0}".format(akamai_prediction))
                self.use_akamai_headers = akamai_prediction["is_akamai"]
            except:
                self.logger.exception("Couldn't get akamai prediction")
                self.use_akamai_headers = False

    def load_proxies(self):
        proxy_requirement = os.getenv("http_proxy")
        if not proxy_requirement:
            return

        if proxy_requirement.startswith("http://"):
            # We are being told to use a direct proxy!
            self.possible_proxies = [proxy_requirement]


class GenderException(Exception):
    pass
