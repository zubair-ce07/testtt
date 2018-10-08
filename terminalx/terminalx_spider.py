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
    care_x = '//div[@id="technical"]/descendant::text()[not(ancestor::p/@dir="rtl")]'
    brand_css = '.product-item-brand ::text'

    images_url_t = 'https://www.terminalx.com/swatches/ajax/media/'

    def parse(self, response):
        product_id = self.magento_product_id(response)

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
        payload = {
            'product_id': self.magento_product_id(response)
        }

        requests = []
        for colour_id in self.colour_ids(response):
            payload['attributes[color]'] = colour_id
            requests.append(FormRequest(url=self.images_url_t, formdata=payload,
                                        callback=self.parse_images, dont_filter=True))
        return requests

    def colour_ids(self, response):
        magento_product = self.magento_product_data(response)
        return magento_product['jsonSwatchConfig']['93'].keys()

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

    def magento_product_data(self, response):
        css = 'script:contains("[data-role=swatch-options]") ::text'
        raw_skus = json.loads(clean(response.css(css))[0])
        return raw_skus['[data-role=swatch-options]']['IdusClass_ProductList/js/swatch-renderer']

    def image_urls(self, response):
        images_json = json.loads(response.text)
        return [image['large'] for _, image in images_json['gallery'].items()]

    def skus(self, response):
        magento_product_data = self.magento_product_data(response)['jsonConfig']
        raw_skus = self.magento_product_map(magento_product_data)
        sku_common = self.product_pricing_common(response)

        skus = {}
        for colour, size in raw_skus.values():
            sku = sku_common.copy()

            sku['colour'] = colour['label']
            sku['size'] = size['label']

            skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus


class TerminalxCrawlSpiderIL(MixinIL, BaseCrawlSpider):
    name = MixinIL.retailer + '-crawl'
    parse_spider = TerminalxParseSpiderIL()

    listings_css = ['.level-top', '.pages']
    product_css = ['.product-item-photo']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )
