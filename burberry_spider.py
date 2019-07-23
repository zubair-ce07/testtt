import json
from urllib.parse import urljoin

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    retailer = 'burberry-cn'
    market = 'CN'
    default_brand = 'Burberry'

    allowed_domains = ['cn.burberry.com']
    start_urls = ['https://cn.burberry.com/']


class BurberryParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

    product_url_t = 'https://cn.burberry.com/service/products/{}'

    raw_description_css = '.accordion-tab_content ::text'
    price_css = '.product-purchase_price ::text'
    brand_css = '.header-bar_logo ::attr(title)'

    def parse(self, response):
        csrf_token = clean(response.css('.csrf-token ::attr(value)'))[0]
        product_url = clean(response.css('.product-detail-page ::attr(data-product-default-url)'))[0]
        headers = {
            'x-csrf-token': csrf_token
        }

        product_request = Request(self.product_url_t.format(product_url), headers=headers, callback=self.parse_product)
        product_request.meta['product_response'] = response

        yield product_request

    def parse_product(self, response):
        raw_product = json.loads(response.text)
        response = response.meta['product_response']
        garment = self.new_unique_garment(self.product_id(raw_product))

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = self.product_name(raw_product)
        garment['brand'] = self.product_brand(response)
        garment['category'] = self.product_category(raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['care'] = self.product_care(response)
        garment['description'] = self.product_description(response)
        garment['skus'] = self.skus(response, raw_product)

        garment['meta'] = {
            'requests_queue': self.colour_requests(response)
        }

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        raw_product = json.loads(response.text)
        garment = response.meta['garment']

        garment['skus'].update(self.skus(response.meta['product_response'], raw_product))
        garment['image_urls'] += self.image_urls(raw_product)

        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        csrf_token = clean(response.css('.csrf-token ::attr(value)'))[0]
        requests = []
        headers = {
            'x-csrf-token': csrf_token
        }

        for colour_url in response.css('.product-purchase_options ::attr(href)').getall():
            product_request = Request(self.product_url_t.format(colour_url), headers=headers, callback=self.parse_colour)
            product_request.meta['product_response'] = response

            requests.append(product_request)

        return requests

    def skus(self, response, raw_product):
        skus = {}
        common_sku = self.product_pricing_common(response)

        if raw_product['findInStore'].get('colour'):
            common_sku['colour'] = raw_product['findInStore']['colour']['value']

        raw_skus = raw_product['findInStore'].get('size')

        if raw_skus:

            for raw_sku in raw_skus['items']:
                sku = common_sku.copy()
                sku['size'] = raw_sku['label']

                if not raw_sku['isAvailable']:
                    sku['out_of_stock'] = True

                skus[raw_sku['value']] = sku

            return skus

        common_sku['size'] = self.one_size
        skus[f'{common_sku["size"]}-{common_sku["colour"]}' if common_sku.get('colour') else common_sku['size']] = common_sku

        return skus

    def product_id(self, raw_product):
        return raw_product['itemNumber']

    def product_name(self, raw_product):
        return raw_product['name']

    def product_category(self, raw_product):
        return raw_product['dataDictionaryProductInfo']['categoryMerch'].split('|')

    def product_gender(self, raw_product):
        return self.gender_lookup(raw_product['dataDictionaryProductInfo']['categoryMerch']) or Gender.ADULTS.value

    def image_urls(self, raw_product):
        return [urljoin(self.start_urls[0], raw_image['img']['src']) for raw_image in raw_product['carousel'] if raw_image.get('img')]


class BurberryCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = BurberryParseSpider()

    pagination_url_t = 'https://cn.burberry.com{}'

    listings_css = ['.nav-level2_main']
    products_css = ['.product_container .product_link']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse_pagination(self, response):
        yield from super().parse(response)

        csrf_token = clean(response.css('.csrf-token ::attr(value)'))[0]
        all_products_links = clean(response.css('.shelves_container ::attr(data-all-products)'))
        headers ={
            'x-csrf-token': csrf_token
        }

        yield from [Request(self.pagination_url_t.format(product_link), headers=headers, callback=self.parse_category)
                    for product_link in all_products_links]

    def parse_category(self, response):
        raw_category = json.loads(response.text)
        yield from [Request(urljoin(self.start_urls[0], product['link']), callback=self.parse_item) for product in raw_category]
