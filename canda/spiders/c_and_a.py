import re
import json

from scrapy import Selector, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from canda.items import Item


class Canda(CrawlSpider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    name = 'c-and-a'
    start_urls = ['https://www.c-and-a.com/de/de/shop/']

    navigation_and_pagination = '.nav-main__list-item, .pagination__next.js-view-click'
    product_css = '.product-tile'
    rules = (
        Rule(LinkExtractor(restrict_css=navigation_and_pagination,
                           tags=('li', 'a'), attrs=('data-url', 'href')), follow=True),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    color_url_t = 'https://www.c-and-a.com/webapp/wcs/stores/servlet/product/change/color?storeId=10154&langId=-3'

    genders = [
        ('herren', 'male'),
        ('damen', 'female'),
        ('jungen', 'boy'),
        ('maedchen', 'girl'),
        ('baby', 'kids'),
        ('kinder', 'kids')
    ]
    currencies = (
        ('€', 'EUR'),
    )

    def parse_item(self, response):
        item = Item()
        item['brand'] = self.brand_name(response)
        item['name'] = self.title(response)
        item['url'] = response.url
        item['categories'] = self.categories(response)
        item['gender'] = self.gender(response)
        item['retailer_sku'] = self.retailer_sku(response)
        item['description'] = self.description(response)
        item['care'] = self.care(response)
        item['image_urls'] = self.image_urls(response)
        item['skus'] = self.skus(response)
        item['meta'] = {'requests': self.make_color_requests(response)}

        return self.next_request_or_item(item)

    def parse_color(self, response):
        item = response.meta.get('item')

        selector = Selector(text=json.loads(response.text)['html'][0]['product-stage'])
        item['image_urls'] += self.image_urls(selector)
        item['skus'] += self.skus(selector)

        return self.next_request_or_item(item)

    def make_color_requests(self, response):
        color_ids = self.color_ids(response)
        product_id = self.product_id(response)

        color_formdata = {'productId': product_id}

        color_requests = []
        for color_id in color_ids:
            color_formdata['colorId'] = color_id
            color_request = FormRequest(url=self.color_url_t,
                                        callback=self.parse_color, formdata=color_formdata)
            color_requests.append(color_request)

        return color_requests

    def next_request_or_item(self, item):
        if not item['meta']['requests']:
            del item['meta']
            return item

        request = item['meta']['requests'].pop()
        request.meta['item'] = item

        return request

    def skus(self, selector):
        sku_common = self.sku_common(selector)
        out_of_stock_sizes = self.out_of_stock_sizes(selector)

        skus = []
        for size in self.all_sizes(selector):
            sku = sku_common.copy()
            sku['size'] = size

            if size in out_of_stock_sizes:
                sku['is_out_of_stock'] = True

            sku['sku_id'] = f'{sku["color"]}_{size}'
            skus.append(sku)

        return skus

    def sku_common(self, selector):
        sku_common = {'color': self.color(selector)}
        sku_common.update(self.pricing(selector))

        return sku_common

    def color(self, response):
        return response.css('.product-stage__color::text').extract_first().split(':')[1].strip()

    def pricing(self, response):
        pricing = dict()

        prices_css = '.product-stage__price span:not(.product-stage__price-saving)::text'
        prices = [a.strip() for a in response.css(prices_css).extract()]
        prices = sorted([self.formatted_price(a) for a in prices])

        pricing['price'] = prices[0]
        pricing['previous_prices'] = prices[1:]
        pricing['currency'] = self.currency(response)

        return pricing

    def formatted_price(self, price):
        return int(''.join(re.findall("\d+", price)))

    def currency(self, response):
        price = response.css('.product-stage__price span::text').extract_first()
        for symbol, currency in self.currencies:
            if symbol in price:
                return currency

    def brand_name(self, response):
        return response.css('.box__logolist-brand::attr(alt)').extract_first(default='C AND A')

    def gender(self, response):
        category_url = response.css('.util-link-left::attr(href)').extract_first()

        for gender_token, gender in self.genders:
            if gender_token in category_url:
                return gender

    def image_urls(self, response):
        return response.css('[data-zoom-id="productImage"]::attr(href)').extract()

    def title(self, response):
        return response.css('.product-stage__title::text').re_first('.*\S.*').strip()

    def retailer_sku(self, response):
        return re.findall('(\d+)/', response.url)[0]

    def description(self, response):
        return [a.strip() for a in response.css('.col-md-6 li::text').re('.*\S.*')]

    def care(self, response):
        return response.css('td:not(.util-text-center)::text').extract()

    def all_sizes(self, response):
        return [s.strip() for s in response.css('.size-list li::text').extract()]

    def out_of_stock_sizes(self, response):
        return [s.strip() for s in response.css('.size-list .is-sold::text').extract()]

    def categories(self, response):
        raw_category = response.css('.util-link-left::text').extract_first().strip()
        return [raw_category.replace("Zurück zu ", '')]

    def color_ids(self, response):
        return response.css('.box--product .color-list :not(.is-active)::attr(data-color)').extract()

    def product_id(self, response):
        return response.css('.product-stage::attr(data-productid)').extract_first()
