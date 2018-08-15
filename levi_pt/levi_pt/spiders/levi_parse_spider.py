import json

from scrapy import Request
from scrapy.spiders import Spider

from levi_pt.items import Product


class LeviptParseSpider(Spider):
    name = "levi_parser"
    gender_map = [
        ('homem', 'men'),
        ('mulher', 'women')
    ]
    domain = "https://www.levi.pt/pt"

    def parse(self, response):
        item = Product()
        item['retailer_sku'] = self.item_retailer_sku(response)
        item['gender'] = self.item_gender(response)
        item['trail'] = self.item_trail(response)
        item['category'] = self.item_category(response)
        item['brand'] = self.item_brand(response)
        item['url'] = response.url
        item['name'] = self.item_name(response)
        item['description'] = self.item_description(response)
        item['care'] = self.item_care(response)
        item['image_urls'] = self.item_image_urls(response)
        response.meta['item'] = item
        return self.parse_item_colors(response)

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
    def item_trail(response):
        trail = response.meta.get('trail', [])
        trail.append(response.url)
        return trail

    def item_category(self, response):
        categories = response.url.split(self.domain)[-1]
        categories = [cat for cat in categories.split('/') if cat][:-1]
        return categories

    @staticmethod
    def item_brand(response):
        return response.css('.product-data [itemprop="brand"]::attr(content)').extract_first()

    @staticmethod
    def item_name(response):
        return response.css('.product-data [itemprop="name"]::attr(content)').extract_first()

    @staticmethod
    def item_care(response):
        title = response.css('.product-description .product-materials .title::text').extract_first()
        care = response.css('.product-description .product-materials li::text').extract()
        if title:
            return [f'{title}: {care}']
        return None

    @staticmethod
    def item_description(response):
        title = response.css('.product-description .product-cut-sizes .title::text').extract_first()
        description = response.css('.product-description .product-cut-sizes li::text').extract()
        if title:
            return [f'{title}: {description}']
        return None

    @staticmethod
    def item_image_urls(response):
        css = '.product-photos-img .xzoom-thumbs a::attr(href)'
        return [response.urljoin(url) for url in response.css(css).extract()]

    def parse_item_colors(self, response):
        item = response.meta.get('item', [])
        requests = []
        for url in response.css('.color-list a::attr(href)').extract():
            request = Request(response.urljoin(url), callback=self.parse_item_stocks,
                              dont_filter=True)
            request.meta['item'] = item
            requests.append(request)
            request.meta['requests'] = requests

        yield from requests

    def parse_item_stocks(self, response):
        item = response.meta.get('item', [])
        item_stock_request = Request(url=f'{response.url}/stocks', callback=self.item_skus)
        item_stock_request.meta['common'] = self.item_skus_common(response)
        item_stock_request.meta['item'] = item
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
    def item_skus(response):
        item = response.meta.get('item')
        requests = response.meta.get('requests', [])
        if requests:
            requests.pop()

        response.meta['requests'] = requests
        skus = item.get('skus', [])

        for stock in json.loads(response.text):
            sku = response.meta.get('common', {}).copy()
            sku['sku_id'] = stock['sku']
            if stock['stock'] == 0:
                sku['out_of_stock'] = True

            if stock['leg_size'] and stock['leg_size'] != '0':
                sku['size'] = f"{stock['size']}/{stock['leg_size']}"
            else:
                sku['size'] = stock['size']

            skus.append(sku)
        item['skus'] = skus

        if not requests:
            yield item
