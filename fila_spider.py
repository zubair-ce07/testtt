import json
from itertools import product

from scrapy import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean, soupify


class Mixin:
    retailer = 'fila'
    default_brand = 'fila'
    deny_care = ['review', 'logged', 'cancel', 'You must be']
    merch_map = [
        ('limited edition', 'Limited Edition')
    ]


class MixinAU(Mixin):
    retailer = Mixin.retailer + '-au'
    market = 'AU'
    allowed_domains = ['fila.com.au']
    start_urls = ['https://fila.com.au/']
    sku_request_url = 'https://fila.com.au/?wc-ajax=get_variation'


class FilaParseSpider(BaseParseSpider):
    sentence_delimiter_r = ','
    price_css = '.summary .price ::text'
    raw_description_css = '.tab-content .active ::text'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(garment)
        garment['merch_info'] = self.merch_info(garment)
        garment['skus'] = self.skus(response)

        if not garment.get('skus'):
            garment['meta'] = {'requests_queue': self.sku_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_sku(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('[data-product-id]::attr(data-product-id)'))[0]

    def product_name(self, response):
        return clean(response.css('[itemprop="name"]::text')[0])

    def product_category(self, response):
        css = 'script:contains("ecomm_category")::text'
        return json.loads(response.css(css).re(r'(\[\".*\"\])')[0])

    def image_urls(self, response):
        css = '.product-images--main a::attr(href)'
        return clean(response.css(css))

    def product_gender(self, garment):
        trail = soupify([url for _, url in garment.get('trail') or []])
        soup = soupify([garment['name']] + garment['category'])
        return self.gender_lookup(soup) or self.gender_lookup(trail) or Gender.ADULTS.value

    def merch_info(self, garment):
        soup = ' '.join(garment['description'] + garment['care']).lower()
        return [merch for merch_str, merch in self.merch_map if merch_str in soup]

    def skus(self, response):
        common_sku = response.meta.get('common_sku')
        css = '.variations_form::attr(data-product_variations)'
        raw_skus = [json.loads(response.text)] if common_sku else json.loads(clean(response.css(css))[0]) or []
        common_sku = common_sku or self.product_pricing_common(response)
        skus = {}

        for raw_sku in raw_skus:
            sku = common_sku.copy()
            sku['colour'] = raw_sku['attributes']['attribute_pa_colour']
            sku['size'] = raw_sku['attributes'].get('attribute_pa_size') or self.one_size

            if not raw_sku['is_in_stock']:
                sku['out_of_stock'] = True

            skus[raw_sku['sku']] = sku

        return skus

    def sku_requests(self, response):
        requests = []
        colours = clean(response.css('#pa_colour ::attr(value)'))
        sizes = clean(response.css('#pa_size ::attr(value)'))
        formdata = {'product_id': self.product_id(response)}
        common_sku = self.product_pricing_common(response)
        meta = {'common_sku': common_sku.copy()}

        for colour, size in product(colours, sizes):
            formdata['attribute_pa_colour'] = colour
            formdata['attribute_pa_size'] = size

            requests.append(FormRequest(self.sku_request_url, formdata=formdata,
                                        meta=meta.copy(), callback=self.parse_sku))

        return requests


class FilaCrawlSpider(BaseCrawlSpider):
    listings_css = [
        '.sub-menu',
        '.pagination'
    ]
    products_css = ['.item-image']
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )


class FilaParseSpiderAU(FilaParseSpider, MixinAU):
    name = MixinAU.retailer + '-parse'


class FilaCrawlSpiderAU(FilaCrawlSpider, MixinAU):
    name = MixinAU.retailer + '-crawl'
    parse_spider = FilaParseSpiderAU()
