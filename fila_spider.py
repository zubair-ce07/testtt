import json
from itertools import product

from scrapy import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    retailer = 'fila'
    default_brand = 'fila'


class MixinAU(Mixin):
    retailer = Mixin.retailer + '-au'
    market = 'AU'
    allowed_domains = ['fila.com.au']
    start_urls = ['https://fila.com.au/']
    sku_request_url = 'https://fila.com.au/?wc-ajax=get_variation'


class FilaParseSpider(BaseParseSpider):
    price_css = '.summary .price ::text'
    raw_description_css = '.tab-content .active ::text'
    care_css = '.tab-content .active :contains(Fabric)::text'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)

        if not garment['skus']:
            garment['meta'] = {'requests_queue': self.sku_requests(response, garment)}

        return self.next_request_or_garment(garment)

    def parse_sku(self, response):
        garment = response.meta['garment']
        sku_id, sku = self.single_sku(response)
        garment['skus'][sku_id] = sku
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('[data-product-id]::attr(data-product-id)'))[0]

    def product_name(self, response):
        return clean(response.css('[itemprop="name"]::text')[0])

    def product_category(self, response):
        css = 'script:contains("ecomm_category")::text'
        return json.loads(response.css(css).re(r'(\[\".*\"\])')[0])

    def image_urls(self, response):
        css = '.woocommerce-product-gallery__image a::attr(href)'
        return set(clean(response.css(css)))

    def product_gender(self, response):
        return self.detect_gender_from_name(response) or Gender.KIDS.value

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        css = '.variations_form::attr(data-product_variations)'
        raw_skus = json.loads(clean(response.css(css))[0])
        skus = {}

        if not raw_skus:
            return skus

        for raw_sku in raw_skus:
            sku = common_sku.copy()
            sku['colour'] = raw_sku['attributes']['attribute_pa_colour']
            sku['size'] = raw_sku['attributes'].get('attribute_pa_size') or self.one_size

            if not raw_sku['is_in_stock']:
                sku['out_of_stock'] = True

            skus[raw_sku['sku']] = sku

        return skus

    def sku_requests(self, response, garment):
        requests = []
        colours = clean(response.css('#pa_colour ::attr(value)'))
        sizes = clean(response.css('#pa_size ::attr(value)'))
        common_sku = self.product_pricing_common(response)
        formdata = {
            'product_id': garment['retailer_sku']
        }

        for colour, size in product(colours, sizes):
            formdata['attribute_pa_colour'] = colour
            formdata['attribute_pa_size'] = size
            meta = {'common_sku': common_sku.copy()}

            requests.append(FormRequest(self.sku_request_url, formdata=formdata,
                                        meta=meta.copy(), callback=self.parse_sku))

        return requests

    def single_sku(self, response):
        raw_sku = json.loads(response.text)
        sku = response.meta['common_sku']
        sku['colour'] = raw_sku['attributes']['attribute_pa_colour']
        sku['size'] = raw_sku['attributes']['attribute_pa_size']

        if not raw_sku['is_in_stock']:
            sku['out_of_stock'] = True

        return raw_sku['sku'], sku


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
