import itertools
import json

from scrapy import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class MixinIL:
    retailer = 'terminalx-il'
    market = 'IL'
    start_urls = ['https://www.terminalx.com']
    allowed_domains = ['terminalx.com']
    default_brand = 'TERMINALX'


class TerminalxParseSpiderIL(MixinIL, BaseParseSpider):
    name = MixinIL.retailer + '-parse'

    price_css = '.product-info-main .price::text'
    description_css = '#brandinfo ::text, [name="description"]::attr(content)'

    images_url_t = 'https://www.terminalx.com/swatches/ajax/media/'

    def parse(self, response):
        product_id = self.product_id(response)

        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = []
        garment['skus'] = self.skus(response)

        garment['meta'] = {'requests_queue': self.images_requests(response)}
        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def images_requests(self, response):
        colour_ids = self.colour_ids(response)
        payload = {
            'product_id': self.product_id(response)
        }

        requests = []
        for colour_id in colour_ids:
            payload['attributes[color]'] = colour_id
            requests.append(FormRequest(url=self.images_url_t, formdata=payload,
                                        callback=self.parse_images, dont_filter=True))
        return requests

    def colour_ids(self, response):
        swatch_json = self.swatch_json(response)
        return swatch_json['jsonSwatchConfig']['93'].keys()

    def product_id(self, response):
        css = '.product-info-main ::attr(data-product-id)'
        return clean(response.css(css))[0]

    def product_brand(self, response):
        brand_css = '.product-item-brand ::text'
        brand = clean(response.css(brand_css))
        return brand[0] if brand else self.default_brand

    def product_name(self, response):
        name_css = '.attribute_name ::text'
        return clean(response.css(name_css))[0]

    def product_gender(self, response):
        css = '.product-sizechart-wrapper ::attr(title)'
        soup = soupify(clean(response.css(css)))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_category(self, response):
        css = '.breadcrumbs ::text'
        return clean(clean(response.css(css)))[1:-1]

    def product_care(self, response):
        care_headings = clean(response.css('#technical .title::text'))
        care_details = clean(response.css('#technical:not(.title)::text'))

        care = clean(response.css('#technical p::text'))
        [care.append(f'{heading} {detail}') for heading, detail in zip(care_headings, care_details)]

        return care

    def swatch_json(self, response):
        css = 'script:contains("[data-role=swatch-options]") ::text'
        swatch_json = json.loads(clean(response.css(css))[0])
        return swatch_json['[data-role=swatch-options]']['IdusClass_ProductList/js/swatch-renderer']

    def image_urls(self, response):
        images_json = json.loads(response.text)
        return [image['large'] for _, image in images_json['gallery'].items()]

    def skus(self, response):
        attributes = self.swatch_json(response)['jsonConfig']['attributes']
        colours = attributes['93']['options']
        sizes = attributes['149']['options']

        sku_common = self.product_pricing_common(response)

        skus = {}
        for colour, size in itertools.product(colours, sizes):
            sku = sku_common.copy()

            sku['colour'] = colour['label']
            sku['size'] = size['label']

            if not any(s in colour['products'] for s in size['products']):
                sku['out_of_stock'] = True

            skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus


class TerminalxCrawlSpiderIL(MixinIL, BaseCrawlSpider):
    name = MixinIL.retailer + '-crawl'
    parse_spider = TerminalxParseSpiderIL()

    listings_css = '.level-top, .pages'
    product_css = '.product-item-photo'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )
