import json
from urllib.parse import urlencode

from scrapy import Selector, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from canda.items import CandaItem


class WhiteStuffSpider(CrawlSpider):
    DOWNLOAD_DELAY = 1
    name = 'c-and-a'
    start_urls = ['https://www.c-and-a.com/de/de/shop/']
    rules = (Rule(LinkExtractor(restrict_css='.nav-main__page-menu .nav-main__list-item'), follow=True),
             Rule(LinkExtractor(restrict_css='.pagination__next.js-view-click',
                                tags=('li',), attrs=('data-url',)), follow=True),
             Rule(LinkExtractor(restrict_css='.product-tile.product-tile--quickmenu'), callback='parse_item'))

    color_request_parameters = (('storeId', '10154'), ('langId', '-3'))
    color_request_url = 'https://www.c-and-a.com/webapp/wcs/stores/servlet/product/change/color?'
    currency = 'EURO'

    def parse_color(self, response):
        item = response.meta.get('item')
        remaining_requests = response.meta.get('requests')
        selector = Selector(text=json.loads(response.text)['html'][0]['product-stage'])
        item['image_urls'] += self.get_image_urls(selector)
        item['skus'] += self.get_skus(selector, item['retailer_sku'])
        if not remaining_requests:
            return item
        request_to_yield = remaining_requests.pop()
        request_to_yield.meta['requests'] = remaining_requests
        request_to_yield.meta['item'] = item
        return request_to_yield

    def get_skus(self, selector, retailer_sku):
        sku_common = {'currency': self.currency}
        sku_common['new_price'], sku_common['old_price'] = self.get_prices(selector)
        color = self.get_color(selector)
        sku_common['color'] = color
        all_sizes = [s.strip() for s in selector.css('.size-list .reveal__content li::text').extract()]
        out_of_stock_sizes = [s.strip() for s in selector.css('.size-list .reveal__content .is-sold::text').extract()]
        skus = []
        for size in all_sizes:
            sku = sku_common.copy()
            sku['size'] = size
            if size in out_of_stock_sizes:
                sku['is_out_of_stock'] = 'true'
            sku['sku_id'] = f'{retailer_sku}_{color}_{size}'
            skus.append(sku)
        return skus

    def parse_item(self, response):
        item = CandaItem()
        item['brand'] = self.get_brand_name(response)
        item['name'] = self.get_title(response)
        item['url'] = response.url
        item['categories'] = self.get_categories(response)
        retailer_sku = self.get_retailer_sku(response)
        item['retailer_sku'] = retailer_sku
        item['description'] = self.get_description(response)
        item['care'] = self.get_care(response)
        item['image_urls'] = self.get_image_urls(response)
        item['skus'] = self.get_skus(response, retailer_sku)
        current_color_id = self.get_current_color_id(response)
        color_ids = self.get_color_ids(response)
        color_ids.remove(current_color_id)
        if not color_ids:
            return item
        product_id = self.get_product_id(response)
        color_requests = self.make_color_requests(color_ids, product_id)
        color_request = color_requests.pop()
        color_request.meta['requests'] = color_requests
        color_request.meta['item'] = item
        return color_request

    def make_color_requests(self, color_ids, product_id):
        color_requests = []
        color_request_data = {'productId': product_id}
        for color_id in color_ids:
            color_request_data['colorId'] = color_id
            color_request = FormRequest(url=f'{self.color_request_url}{urlencode(self.color_request_parameters)}',
                                        callback=self.parse_color, formdata=color_request_data)
            color_requests.append(color_request)
        return color_requests

    @staticmethod
    def get_color(response):
        return response.css('.product-stage__color::text').extract_first().split(':')[1].strip()

    def get_prices(self, response):
        prices = response.css('.product-stage__price span::text').extract()[:2]
        prices = sorted([self.formatted_price(a) for a in prices])
        return prices[0], prices[1:]

    @staticmethod
    def formatted_price(price):
        price = price.translate(str.maketrans({u"\u20ac": '', ',': '.'}))
        return int(float(price) * 100)

    @staticmethod
    def get_brand_name(response):
        return response.css('.product-stage__title strong::text').extract()

    @staticmethod
    def get_image_urls(response):
        return response.css('[data-zoom-id="productImage"]::attr(href)').extract()

    @staticmethod
    def get_title(response):
        return list(filter(None, [a.strip() for a in response.css('.product-stage__title::text').extract()]))[0]

    @staticmethod
    def get_retailer_sku(response):
        return response.css('.col-md-6 h5::text').extract_first().split(':')[1].strip()

    @staticmethod
    def get_description(response):
        return list(filter(None, [a.strip() for a in response.css('.col-md-6 li::text').extract()]))

    @staticmethod
    def get_care(response):
        return list(filter(None, [a.strip() for a in response.css('td::text').extract()]))

    @staticmethod
    def get_categories(response):
        return response.css('.util-link-left.util-text-smaller::text').extract_first().strip()

    @staticmethod
    def get_color_ids(response):
        return response.css('.box--product .color-list li::attr(data-color)').extract()

    @staticmethod
    def get_product_id(response):
        return response.css('.product-stage::attr(data-productid)').extract()

    @staticmethod
    def get_current_color_id(response):
        return response.css('.box--product .color-list .is-active::attr(data-color)').extract_first()
