import re
import json
import itertools

from scrapy import Request, FormRequest
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class Mixin:
    retailer = 'schwab-de'
    market = 'DE'
    allowed_domains = [
        'schwab.de',
    ]
    start_urls = ['https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true']

    homeware_tokens = [
        'heimtextilien',
        'haushalt'
    ]

    denied_categories = [
        'sport/',
        'spielzeug/',
        'multimedia/',
        'beauty/',
        'landkueche/',
        'sale/',
        'marken/',
        'baumkart/'
    ]


class ParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    sizes_url_t = 'https://www.schwab.de/request/itemservice.php?fnc=getItemInfos'
    variants_url_t = 'https://www.schwab.de/index.php?cl=oxwarticledetails&' \
                     'anid={anid}&varselid[2]={varselid2}&varselid[1]={varselid1}&varselid[0]={varselid0}'

    product_id_r = re.compile('_(\d+)\.')
    items_r = re.compile(r'articlesString.*?\'(.*?)\\', re.S)

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['name'] = self.product_name(response)
        garment['category'] = self.product_category(response)
        garment['brand'] = self.product_brand(response)
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)
        garment['skus'] = {}

        if self.is_homeware(response):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(response)

        variants_requests = self.make_variant_requests(response)
        size_availibilty_requests = self.make_items_availabilty_request(response)
        garment['meta'] = {'requests_queue': variants_requests + size_availibilty_requests}

        return self.next_request_or_garment(garment)

    def parse_variant(self, response):
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response, garment['meta']['size_availability']))

        return self.next_request_or_garment(garment, drop_meta=True)

    def parse_size_availability(self, response):
        garment = response.meta['garment']

        size_availability = json.loads(response.text)
        garment['meta'].update({"size_availability": size_availability})

        return self.next_request_or_garment(garment)

    def skus(self, response, size_availability):
        price_css = '.pricing__norm--wrong ::text, .pricing__norm--new ::text'
        sku = self.product_pricing_common(response, price_css=price_css)

        color_css = '.js-color-value ::text'
        color = clean(response.css(color_css))
        if color:
            sku['color'] = ' '.join(color[0].split(' ')[1:])

        variant_css = '.js-variant-value ::text'
        variant = clean(response.css(variant_css))
        variant = ' '.join(variant[0].split(' ')[1:]) if variant else ''

        size_css = '.js-size-value ::text'
        size = clean(response.css(size_css))
        size = ' '.join(size[0].split(' ')[1:]) if size else self.one_size

        article_number_css = '.js-artNr ::text'
        article_number = clean(response.css(article_number_css))[0]

        sku['size'] = f'{variant}/{size}' if variant else size
        if size_availability:
            if isinstance(size_availability[article_number], list) and 'ausverkauft' in size_availability[article_number]:
                sku['out_of_stock'] = True
            if isinstance(size_availability[article_number], dict) and 'ausverkauft' in size_availability[article_number].get(size, []):
                sku['out_of_stock'] = True

        sku_id = f'{sku["color"]}_{sku["size"]}' if sku.get('color') else sku['size']
        return{sku_id: sku}

    def image_urls(self, response):
        return ['https:' + url for url in clean(response.css('#thumbslider ::attr(data-zoom-image)'))]

    def product_id(self, response):
        return self.product_id_r.findall(response.url)[0]

    def product_name(self, response):
        return clean(response.css('.details__title ::text'))[0]

    def product_category(self, response):
        return clean(clean(response.css('.breadcrumb [itemprop="name"]::text'))[1:])

    def product_raw_description(self, response):
        css = '.details__variation__hightlights ::text, .details__desc__more__content ::text'
        return sum([rd.split('. ') for rd in clean(response.css(css))], [])

    def product_description(self, response):
        return [rd for rd in self.product_raw_description(response) if not self.care_criteria(rd)]

    def product_care(self, response):
        return [rd for rd in self.product_raw_description(response) if self.care_criteria(rd)]

    def product_brand(self, response):
        brand_css = '[itemprop="brand"]::attr(content)'
        brand = clean(response.css(brand_css))
        return brand[0] if brand else 'Schwab'

    def product_gender(self, response):
        return self.gender_lookup(''.join(self.product_category(response)), greedy=True, use_default_gender_map=True)

    def is_homeware(self, response):
        soup = ''.join(self.product_category(response)).lower()
        return any(hw in soup for hw in self.homeware_tokens)

    def make_variant_requests(self, response):
        color_ids_css = '.colorspots__item::attr(data-varselid), .js-varselid-COLOR::attr(value)'
        color_ids = clean(response.css(color_ids_css)) or ['']
        color_ids = list(set(color_ids))
        color_name = clean(response.css('.js-varselid-COLOR ::attr(name)'))
        color_name = color_name[0] if color_name else ''

        variant_ids_css = '.variant [size="1"] ::attr(value), .variant .js-varselid::attr(value)'
        variant_ids = clean(response.css(variant_ids_css)) or ['']
        variant_ids = list(set(variant_ids))
        variant_name = clean(response.css('.variant .js-varselid ::attr(name)'))
        variant_name = variant_name[0] if variant_name else ''

        sizes_ids_css = '.c-size-box ::attr(data-selection-id), .size [size="1"] ::attr(value),' \
                        ' .size .js-varselid::attr(value)'
        size_ids = clean(response.css(sizes_ids_css))
        size_ids = list(set(size_ids)) or ['']
        size_name = clean(response.css('.size .js-varselid ::attr(name)'))
        size_name = size_name[0] if size_name else ''

        anid_css = '[name="anid"]::attr(value)'
        anid = clean(response.css(anid_css))[0]

        variant = {
            color_name: '',
            variant_name: '',
            size_name: ''
        }
        variant_requests = []
        for color_id, variant_id, size_id in itertools.product(color_ids, variant_ids, size_ids):
            variant['color_name'] = color_id
            variant['variant_name'] = variant_id
            variant['size_name'] = size_id

            url = self.variants_url_t.format(
                    anid=anid,
                    varselid2=variant.get('varselid[2]', ''),
                    varselid1=variant.get('varselid[1]', ''),
                    varselid0=variant.get('varselid[0]', '')
            )
            variant_requests.append(Request(url=url, callback=self.parse_variant))
        return variant_requests

    def make_items_availabilty_request(self, response):
        payload_items = response.css('script::text').re_first(self.items_r)
        payload = {
            'items': payload_items
        }
        return [FormRequest(url=self.sizes_url_t, formdata=payload, callback=self.parse_size_availability)]


class CrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    listing_css = '.next'
    product_css = '.c-product'
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    parse_spider = ParseSpider()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        all_categories = json.loads(response.text)

        categories_urls = []
        for main_category in all_categories:
            categories_urls.append(main_category['url'])
            for level_2_category in main_category.get('sCat', {}):
                categories_urls.append(level_2_category.get('url'))
                for level_3_category in level_2_category.get('sCat', {}):
                    categories_urls.append(level_3_category.get('url'))
                    for level_4_category in level_3_category.get('sCat', {}):
                        categories_urls.append(level_4_category.get('url'))

        yield from self.make_categories_requests(categories_urls)

    def make_categories_requests(self, categories_urls):
        requests = []

        for url in categories_urls:
            if any(dc in url for dc in self.denied_categories):
                continue

            request = Request(url=url, callback=self.parse)
            requests.append(request)

        return requests






