import json

from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.linkextractors import LinkExtractor
from zlib import decompress
from base64 import b64decode

from urbanoutfitters.items import UrbanoutfittersItem


class OutfittersMixin:
    name = 'outfitters'
    allowed_domain = ['https://www.urbanoutfitters.com']
    start_urls = ['https://www.urbanoutfitters.com']


class OutFittersParserSpider(OutfittersMixin, Spider):
    name = 'outfitters-spider'
    gender_map = {
        "women's": 'Women',
        "men's": 'Men',
    }

    def product_package(self, response):
        product = UrbanoutfittersItem()

        encoded_data = response.css('script::text').re_first(r"window.productData = '(.+)';").encode()
        raw_data = decompress(b64decode(encoded_data)).decode()
        product_data = json.loads(raw_data)

        response.meta['product_data'] = product_data

        filtered_product = product_data['product']['product']
        # detail contain both content and care
        detail = filtered_product['longDescription'].split('**Content + Care**  ')

        product['retailer_sku'] = filtered_product['productId']
        product['name'] = filtered_product['displayName']
        product['brand'] = filtered_product.get('brand', None)
        product['price'] = int(product_data['product']['skuInfo'].get('salePriceLow')) * 100
        product['currency'] = product_data['product'].get('currencyCode')
        product['description'] = detail.pop().strip()
        product['url'] = response.url
        product['gender'] = filtered_product['facets']['genders'][0]
        product['category'] = filtered_product['categoryIds']
        product['care'] = detail.pop() if detail else None
        product['trail'] = response.meta.get('trail', [])
        product['retailer'] = "outfitters"
        product['images_urls'] = self.product_images(response)
        product['skus'] = self.product_skus(response)
        product['merch_info'] = self.product_merch_info(response)

        if not product['gender']:
            product['industry'] = "Homeware"

        return self.extract_requests(self.color_requests(response), product)

    def parse_color(self, response):
        product = response.meta['product']
        product['images_urls'] += self.product_images(response)

        return self.extract_requests(response.meta['requests'], product)

    def color_requests(self, response):
        colors = response.css('.o-list-swatches a::attr(href)').extract()
        requests = []

        for color in colors:
            requests += [response.follow(url=color, callback=self.parse_color, dont_filter=True)]

        return requests

    def product_skus(self, response):
        product_data = response.meta['product_data']
        colors = product_data['product']['controlsData'].get('colorData')

        all_skus = {}

        for color in colors.values():
            sizes_sku = color['fitData']['REGULAR'].get('sizeData')

            for size in sizes_sku.values():
                sku = {}
                prices = product_data['product']['skuInfo']
                sku['size'] = size.get('displayName', 'One Size')
                sku['color'] = color['displayName']
                sku['price'] = int(prices.get('salePriceLow')) * 100
                sku_id = f'{sku["color"] or ""}|{sku["size"]}'
                previous_price = prices.get('listPriceHigh')

                if previous_price:
                    sku['previous_price'] = int(previous_price) * 100
                if not size['inStock']:
                    sku['out_of_stock'] = True

                all_skus[sku_id] = sku

        return all_skus

    @staticmethod
    def extract_requests(requests, product):
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            request.meta['requests'] = requests
            yield request
        else:
            yield product

    @staticmethod
    def product_images(response):
        images = response.css(
            'div.o-carousel__slide.js-carousel-zoom__slide'
            ' img:not(.c-zoom-overlay__img):not([src*="loading-spacer"])::attr(src)').extract()
        return ["https:" + i for i in images]

    @staticmethod
    def product_merch_info(response):
        return response.css('.c-afterpay__message::text').extract_first().strip()


class SchwabCralwer(OutfittersMixin, CrawlSpider):
    items_per_page = 100

    outfitters_parser = OutFittersParserSpider()

    rules = (
        Rule(LinkExtractor(restrict_css='nav a'), callback='parse', follow=True),
        Rule(LinkExtractor(restrict_css='div.s-category-grid a, ul.o-pagination__ul a'),
             callback=outfitters_parser.product_package)
    )

    def parse(self, response):
        for request in super().parse(response):
            request.meta['trail'] = self.add_trail(response)
            yield request

    def add_trail(self, response):
        return response.meta.get('trail', []) + [response.url]
