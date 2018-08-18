from json import loads
from urllib.parse import urlparse

from scrapy import Request
from scrapy.spiders import Spider

from levi_pt.items import Product


class LeviptParseSpider(Spider):
    name = "levi_parser"
    gender_map = [
        ('homem', 'men'),
        ('mulher', 'women')
    ]

    visiting_ids = set()

    def parse(self, response):
        retailer_sku = self.item_retailer_sku(response)

        if retailer_sku in self.visiting_ids:
            return

        self.visiting_ids.add(retailer_sku)

        item = Product()
        item['retailer_sku'] = retailer_sku
        item['gender'] = self.item_gender(response)
        item['trail'] = response.meta.get('trail')
        item['category'] = self.item_category(response)
        item['brand'] = self.item_brand(response)
        item['url'] = response.url
        item['name'] = self.item_name(response)
        item['description'] = self.item_description(response)
        item['care'] = self.item_care(response)

        requests = self.colors_requests(response)
        response.meta['requests'] = requests
        response.meta['item'] = item

        return self.parse_item_stocks(response)

    def parse_item_skus(self, response):
        item = response.meta['item']
        skus = item.get('skus', [])
        common = response.meta.get('common', {})
        stocks = loads(response.text)
        item['skus'] = self.stock_to_skus(stocks, skus, common)
        requests = response.meta['requests']
        return self.request_or_item(requests, item)

    def parse_item_stocks(self, response):
        item = response.meta['item']
        image_urls = item.get('image_urls', [])
        image_urls += self.item_image_urls(response)
        item['image_urls'] = image_urls

        item_stock_request = Request(url=f'{response.url}/stocks',
                                     callback=self.parse_item_skus)
        item_stock_request.meta['common'] = self.item_skus_common(response)
        item_stock_request.meta['item'] = item
        item_stock_request.meta['requests'] = response.meta['requests']

        return item_stock_request

    @staticmethod
    def item_skus_common(response):
        curr_css = '[itemprop="priceCurrency"]::attr(content)'
        colour_css = '[itemprop="color"]::text'
        price_css = '[itemprop="lowPrice"]::text, [itemprop="price"]::text'
        prev_p_css = '[itemprop="highPrice"]::text'
        common = {
            'currency': response.css(curr_css).extract_first(default="EUR"),
            'colour': response.css(colour_css).extract_first(),
            'price': response.css(price_css).extract_first().replace("€", ''),
            'previous_prices': response.css(prev_p_css).extract()
        }

        return common

    @staticmethod
    def stock_to_skus(stocks, skus, common):
        for stock in stocks:
            sku = common.copy()
            sku['sku_id'] = stock.get('sku')
            if stock.get('stock', 0) == 0:
                sku['out_of_stock'] = True

            if stock.get('leg_size', '0') != '0':
                sku['size'] = f"{stock.get('size')}/{stock['leg_size']}"
            else:
                sku['size'] = stock.get('size')
            skus.append(sku)

        return skus

    @staticmethod
    def request_or_item(requests, item):
        if not requests:
            return item

        request = requests.pop()
        request.meta['requests'] = requests
        request.meta['item'] = item

        return request

    def colors_requests(self, response):
        requests = []
        css = '.color-list a:not(.active)::attr(href)'
        for url in response.css(css).extract():
            request = response.follow(response.urljoin(url),
                                      callback=self.parse_item_stocks)
            requests.append(request)

        return requests

    @staticmethod
    def item_retailer_sku(response):
        css = '.btn-add-to-favorites::attr(data-model-id)'
        return response.css(css).extract_first().split('-')[0]

    def item_gender(self, response):
        css = '.size-chart-lightbox .title::text'
        raw_gender = response.css(css).extract_first()

        if not raw_gender:
            return 'unisex-adults'

        for token, gender in self.gender_map:
            if token in raw_gender:
                return gender

        return 'unisex-adults'

    @staticmethod
    def item_category(response):
        url_path = urlparse(response.url).path
        return [cat for cat in url_path.split('/') if cat][1:-1]

    @staticmethod
    def item_brand(response):
        css = '[itemprop="brand"]::attr(content)'
        return response.css(css).extract_first()

    @staticmethod
    def item_name(response):
        css = '[itemprop="name"]::attr(content)'
        return response.css(css).extract_first()

    @staticmethod
    def item_care(response):
        css = '.product-materials ::text'
        return response.css(css).extract()

    @staticmethod
    def item_description(response):
        css = '.product-description .product-cut-sizes ::text'
        return response.css(css).extract()

    @staticmethod
    def item_image_urls(response):
        css = '.product-photos-img .xzoom-thumbs a::attr(href)'
        return [response.urljoin(url) for url in response.css(css).extract()]
