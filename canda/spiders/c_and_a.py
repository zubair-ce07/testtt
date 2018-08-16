import re
import json
from urllib.parse import urlencode

from scrapy import Selector, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from canda.items import CandaItem


class Canda(CrawlSpider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }
    name = 'c-and-a'
    start_urls = ['https://www.c-and-a.com/de/de/shop/']
    rules = (Rule(LinkExtractor(restrict_css='.nav-main__list-item, .pagination__next.js-view-click',
                                tags=('li', 'a'), attrs=('data-url', 'href')), follow=True),
             Rule(LinkExtractor(restrict_css='.product-tile'), callback='parse_item'))

    currencies = {'€': 'EUR'}
    color_parameters = (
        ('storeId', '10154'),
        ('langId', '-3')
    )
    color_url_t = 'https://www.c-and-a.com/webapp/wcs/stores/servlet/product/change/color?'
    genders = [
        ('herren', 'male'),
        ('damen', 'female'),
        ('jungen', 'boy'),
        ('maedchen', 'girl'),
        ('baby', 'kids'),
        ('kinder', 'kids')
    ]

    def parse_color(self, response):
        item = response.meta.get('item')

        selector = Selector(text=json.loads(response.text)['html'][0]['product-stage'])
        item['image_urls'] += self.get_image_urls(selector)
        item['skus'] += self.get_skus(selector, item['retailer_sku'])

        return self.yield_color_request(response.meta.get('requests'), item)

    def get_skus(self, selector, retailer_sku):
        sku_common = self.get_sku_common(selector)
        out_of_stock_sizes = self.get_out_of_stock_sizes(selector)
        skus = []

        for size in self.get_all_sizes(selector):
            sku = sku_common.copy()
            sku['size'] = size

            if size in out_of_stock_sizes:
                sku['is_out_of_stock'] = True

            sku['sku_id'] = f'{retailer_sku}_{sku["color"]}_{size}'
            skus.append(sku)

        return skus

    def get_sku_common(self, selector):
        sku_common = {'color': self.get_color(selector)}
        sku_common.update(self.get_pricing(selector))

        return sku_common

    def parse_item(self, response):
        item = CandaItem()
        item['brand'] = self.get_brand_name(response)
        item['name'] = self.get_title(response)
        item['url'] = response.url
        item['categories'] = self.get_categories(response)
        item['gender'] = self.get_gender(response)
        retailer_sku = self.get_retailer_sku(response)
        item['retailer_sku'] = retailer_sku
        item['description'] = self.get_description(response)
        item['care'] = self.get_care(response)
        item['image_urls'] = self.get_image_urls(response)
        item['skus'] = self.get_skus(response, retailer_sku)

        color_ids = self.get_color_ids(response)
        product_id = self.get_product_id(response)
        color_requests = self.make_color_requests(color_ids, product_id)

        return self.yield_color_request(color_requests, item)

    @staticmethod
    def yield_color_request(color_requests, item):
        if not color_requests:
            return item

        color_request = color_requests.pop()
        color_request.meta['requests'] = color_requests
        color_request.meta['item'] = item

        return color_request

    def make_color_requests(self, color_ids, product_id):
        color_requests = []
        color_data = {'productId': product_id}

        for color_id in color_ids:
            color_data['colorId'] = color_id
            color_request = FormRequest(url=f'{self.color_url_t}{urlencode(self.color_parameters)}',
                                        callback=self.parse_color, formdata=color_data)
            color_requests.append(color_request)

        return color_requests

    @staticmethod
    def get_color(response):
        return response.css('.product-stage__color::text').extract_first().split(':')[1].strip()

    def get_pricing(self, response):
        pricing = dict()

        prices_css = '.product-stage__price span:not(.product-stage__price-saving)::text'
        prices = [a.strip() for a in response.css(prices_css).extract()]
        prices = sorted([self.formatted_price(a) for a in prices])

        pricing['price'] = prices[0]
        pricing['previous_prices'] = prices[1:]
        pricing['currency'] = self.get_currency(response)

        return pricing

    @staticmethod
    def formatted_price(price):
        return int(''.join(re.findall("\d+", price)))

    def get_currency(self, response):
        currency_symbol = self.get_currency_symbol(response)
        return self.currencies.get(currency_symbol)

    @staticmethod
    def get_currency_symbol(response):
        return re.findall(
            r"[^\w\d_\s,.\\]", response.css('.product-stage__price span::text').extract_first(), re.UNICODE)[0]

    @staticmethod
    def get_brand_name(response):
        return response.css('.box__logolist-brand::attr(alt)').extract_first(default='C AND A')

    def get_gender(self, response):
        category_url = response.css('.util-link-left.util-text-smaller::attr(href)').extract_first()

        for gender_token, gender in self.genders:
            if gender_token in category_url:
                return gender

    @staticmethod
    def get_image_urls(response):
        return response.css('[data-zoom-id="productImage"]::attr(href)').extract()

    @staticmethod
    def get_title(response):
        return list(filter(None, [a.strip() for a in response.css('.product-stage__title::text').extract()]))[0]

    @staticmethod
    def get_retailer_sku(response):
        return re.findall('(\d+)/', response.url)[0]

    @staticmethod
    def get_description(response):
        return list(filter(None, [a.strip() for a in response.css('.col-md-6 li::text').extract()]))

    @staticmethod
    def get_care(response):
        return response.css('td:not(.util-text-center)::text').extract()

    @staticmethod
    def get_all_sizes(response):
        return [s.strip() for s in response.css('.size-list li::text').extract()]

    @staticmethod
    def get_out_of_stock_sizes(response):
        return [s.strip() for s in response.css('.size-list .is-sold::text').extract()]

    @staticmethod
    def get_categories(response):
        raw_category = response.css('.util-link-left::text').extract_first().strip()
        return [re.sub(r"Zurück zu ", '', raw_category)]

    @staticmethod
    def get_color_ids(response):
        return response.css('.box--product .color-list :not(.is-active)::attr(data-color)').extract()

    @staticmethod
    def get_product_id(response):
        return response.css('.product-stage::attr(data-productid)').extract()
