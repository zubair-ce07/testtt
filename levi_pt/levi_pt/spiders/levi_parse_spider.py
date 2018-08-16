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

    def parse(self, response):
        item = Product()
        item['retailer_sku'] = self.item_retailer_sku(response)
        item['gender'] = self.item_gender(response)
        item['trail'] = response.meta.get('trail', [])
        item['category'] = self.item_category(response)
        item['brand'] = self.item_brand(response)
        item['url'] = response.url
        item['name'] = self.item_name(response)
        item['description'] = self.item_description(response)
        item['care'] = self.item_care(response)
        item['image_urls'] = self.item_image_urls(response)
        response.meta['item'] = item
        return self.item_colors(response)

    def parse_item_skus(self, response):
        item = response.meta.get('item', [])
        skus = item.get('skus', [])
        common = response.meta.get('common', {})
        stocks = loads(response.text)
        item['skus'] = self.stock_to_skus(stocks, skus, common)
        return self.yield_request_or_item(response)

    def parse_item_stocks(self, response):
        item_stock_request = Request(url=f'{response.url}/stocks', callback=self.parse_item_skus)
        item_stock_request.meta['common'] = self.item_skus_common(response)
        item_stock_request.meta['item'] = response.meta.get('item', [])
        item_stock_request.meta['requests'] = response.meta.get('requests', [])
        yield item_stock_request

    @staticmethod
    def item_skus_common(response):
        price_css = '[itemprop="lowPrice"]::text, [itemprop="price"]::text'
        old_p_css = '[itemprop="highPrice"]::text'
        colour = response.css('[itemprop="color"]::text').extract_first()
        common = {
            'currency': response.css('[itemprop="priceCurrency"]::attr(content)').extract_first(),
            'colour': colour,
            'price': response.css(price_css).extract_first().replace("€", ''),
            'previous_prices': response.css(old_p_css).extract()
        }
        return common

    @staticmethod
    def stock_to_skus(stocks, skus, common):
        for stock in stocks:
            sku = common.copy()
            sku['sku_id'] = stock['sku']
            if stock['stock'] == 0:
                sku['out_of_stock'] = True

            if stock['leg_size'] and stock['leg_size'] != '0':
                sku['size'] = f"{stock['size']}/{stock['leg_size']}"
            else:
                sku['size'] = stock['size']
            skus.append(sku)
        return skus

    @staticmethod
    def yield_request_or_item(response):
        requests = response.meta.get('requests', [])
        if requests:
            request = requests.pop()
            response.meta['requests'] = requests
            yield request
        else:
            yield response.meta.get('item', [])

    def item_colors(self, response):
        item = response.meta.get('item', [])
        requests = []
        for url in response.css('.color-list a::attr(href)').extract():
            request = Request(response.urljoin(url), callback=self.parse_item_stocks,
                              dont_filter=True)
            requests.append(request)
            request.meta['requests'] = requests
            request.meta['item'] = item

        response.meta['requests'] = requests
        return self.yield_request_or_item(response)

    @staticmethod
    def item_retailer_sku(response):
        css = '.product-data .btn-add-to-favorites::attr(data-model-id)'
        return response.css(css).extract_first()

    def item_gender(self, response):
        raw_gender = response.css('.size-chart-lightbox .title::text').extract_first()
        if not raw_gender:
            return 'unisex-adults'
        for token, gender in self.gender_map:
            if token in raw_gender:
                return gender
        return 'unisex-adults'

    @staticmethod
    def item_category(response):
        categories = urlparse(response.url).path
        return [cat for cat in categories.split('/') if cat][1:-1]

    @staticmethod
    def item_brand(response):
        return response.css('.product-data [itemprop="brand"]::attr(content)').extract_first()

    @staticmethod
    def item_name(response):
        return response.css('.product-data [itemprop="name"]::attr(content)').extract_first()

    @staticmethod
    def item_care(response):
        title_css = '.product-description .product-materials .title::text'
        care_css = '.product-description .product-materials li::text'
        title = response.css(title_css).extract_first(default=None)
        care = response.css(care_css).extract()
        return [f'{title}: {care}']

    @staticmethod
    def item_description(response):
        title_css = '.product-description .product-cut-sizes .title::text'
        des_css = '.product-description .product-cut-sizes li::text'
        title = response.css(title_css).extract_first(default=None)
        description = response.css(des_css).extract()
        return [f'{title}: {description}']

    @staticmethod
    def item_image_urls(response):
        css = '.product-photos-img .xzoom-thumbs a::attr(href)'
        return [response.urljoin(url) for url in response.css(css).extract()]
