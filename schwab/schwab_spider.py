import re
import json
import itertools

from scrapy import Request, FormRequest
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender, soupify


class Mixin:
    retailer = 'schwab-de'
    market = 'DE'
    allowed_domains = [
        'schwab.de'
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
        'baumkart/',
        'service/'
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

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}

        if self.is_homeware(response):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(response)

        variants_requests = self.make_variant_requests(response)
        size_availability_requests = self.make_items_availabilty_request(response)
        garment['meta'] = {'requests_queue': variants_requests + size_availability_requests}

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

        colour_css = '.js-color-value ::text'
        colour = clean(response.css(colour_css))
        if colour:
            sku['colour'] = clean(colour[0].strip('–'))

        variant_css = '.js-variant-value ::text'
        variant = clean(response.css(variant_css))
        variant = clean(variant[0].strip('–')) if variant else ''

        size_css = '.js-size-value ::text'
        size = clean(response.css(size_css))
        size = clean(size[0].strip('–')) if size else self.one_size

        article_number_css = '.js-artNr ::text'
        article_number = clean(response.css(article_number_css))[0]

        sku['size'] = f'{variant}_{size}' if variant else size

        size_lookup_key = clean(size.split('/')[0])
        if isinstance(size_availability[article_number], list) and 'ausverkauft' in \
                size_availability[article_number]:
            sku['out_of_stock'] = True
        if isinstance(size_availability[article_number], dict) and 'ausverkauft' in \
                size_availability[article_number].get(size_lookup_key, []):
            sku['out_of_stock'] = True

        sku_id = f'{sku["colour"]}_{sku["size"]}' if sku.get('colour') else sku['size']
        return{sku_id: sku}

    def image_urls(self, response):
        return ['https:' + url for url in clean(response.css('#thumbslider ::attr(data-zoom-image)'))]

    def product_id(self, response):
        return self.product_id_r.findall(response.url)[0]

    def product_name(self, response):
        return clean(response.css('.details__title ::text'))[0]

    def product_category(self, response):
        return clean(clean(response.css('.breadcrumb [itemprop="name"]::text'))[1:-1])

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
        soup = self.product_category(response) + self.product_description(response) + [self.product_name(response)]
        return self.gender_lookup(soupify(soup).lower(),
                                  greedy=True, use_default_gender_map=True) or Gender.ADULTS.value

    def is_homeware(self, response):
        soup = soupify(self.product_category(response)).lower()
        return any(hw in soup for hw in self.homeware_tokens)

    def make_variant_requests(self, response):
        colour_ids_css = '.colorspots__item::attr(data-varselid), .js-varselid-COLOR::attr(value)'
        colour_ids = clean(response.css(colour_ids_css)) or ['']
        colour_parameter_name = clean(response.css('.js-varselid-COLOR ::attr(name)'))
        colour_parameter_name = colour_parameter_name[0] if colour_parameter_name else ''

        variant_ids_css = '.variant [size="1"] ::attr(value), .variant .js-varselid::attr(value)'
        variant_ids = clean(response.css(variant_ids_css)) or ['']
        variant_parameter_name = clean(response.css('.variant .js-varselid ::attr(name)'))
        variant_parameter_name = variant_parameter_name[0] if variant_parameter_name else ''

        sizes_ids_css = '.c-size-box ::attr(data-selection-id), .size [size="1"] ::attr(value),' \
                        ' .size .js-varselid::attr(value)'
        size_ids = clean(response.css(sizes_ids_css)) or ['']
        size_parameter_name = clean(response.css('.size .js-varselid ::attr(name)'))
        size_parameter_name = size_parameter_name[0] if size_parameter_name else ''

        anid_css = '[name="anid"]::attr(value)'
        anid = clean(response.css(anid_css))[0]

        variant_requests = []
        for colour_id, variant_id, size_id in itertools.product(colour_ids, variant_ids, size_ids):
            variation_parameters = {
                colour_parameter_name: colour_id,
                variant_parameter_name: variant_id,
                size_parameter_name:  size_id
            }

            url = self.variants_url_t.format(
                    anid=anid,
                    varselid2=variation_parameters.get('varselid[2]', ''),
                    varselid1=variation_parameters.get('varselid[1]', ''),
                    varselid0=variation_parameters.get('varselid[0]', '')
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

    listings_css = '.next'
    products_css = '.c-product'
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )

    categories_urls_r = re.compile(r'url\":\"(.*?)\",', re.S)
    parse_spider = ParseSpider()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        categories_urls = self.categories_urls_r.findall(response.text)
        yield from self.make_categories_requests(categories_urls)

    def make_categories_requests(self, categories_urls):
        requests = []

        for url in categories_urls:
            if any(dc in url for dc in self.denied_categories):
                continue

            request = Request(url=url, callback=self.parse)
            requests.append(request)

        return requests
