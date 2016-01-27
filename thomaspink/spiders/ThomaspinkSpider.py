from thomaspink.items import ThomaspinkItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import locale
import re
import copy
from scrapy.contrib.loader.processor import TakeFirst


class ThomaspinkSpider(CrawlSpider):
    name = "thomaspink"
    allowed_domains = ["thomaspink.com"]
    take_first = TakeFirst()
    start_urls = ["http://www.thomaspink.com/"]
    rules = (Rule(LinkExtractor(restrict_xpaths=(".//*[@id='main_navigation_level_1']//a", "//*[@class='next']",))),
             Rule(LinkExtractor(restrict_xpaths=("//*[@class='image_container']",)), callback='parse_product'),)

    def parse_product(self, response):
        item = ThomaspinkItem()
        item['description'] = self.get_description(response)
        item['image_urls'] = self.get_image_urls(response)
        item['name'] = self.get_product_name(response)
        item['url'] = response.url
        item['care'] = self.get_care(response)
        item['sku'] = self.get_sku(response)
        item['category'] = self.get_category(response)
        item['retailer_sku'] = self.get_retailer_sku(item['url'])
        item['gender'] = self.get_gender(response)
        item['brand'] = 'Thomas Pink'
        item['market'] = 'UK'
        yield item

    def get_description(self, response):
        return response.xpath("//*[@id='product_overview']/p[2]/text()").extract()

    def get_care(self, response):
        return [c for c in response.xpath("//*[@id='product_overview']//li/text()").extract() if '%' in c]

    def get_image_urls(self, response):
        return response.xpath("//*[@id='alternative_images']/li/img/@src").extract()

    def get_product_name(self, response):
        return self.clean_list(response.xpath("//*[@id='product_heading']/h1/text()").extract())

    def get_sku(self, response):
        colors = self.get_colors(response)
        price = self.get_price(response)
        sku = {}
        sizes = self.clean_list(self.get_size(response))
        if sizes[1] in sizes[2:]:
            regular_availability = self.check_regular_availability(response)
            long_availability = self.check_long_availability(response)
            self.sku(price, colors, sku, sizes[1:sizes.index(sizes[1], 2)], regular_availability, long_availability)
        else:
            availability = self.check_availability(response)
            long_availability = []
            self.sku(price, colors, sku, sizes[1:], availability, long_availability)
        return sku

    def get_price(self, response):
        return response.xpath("//*[@class='product_price']//text()").re('(.\w+[.]\d\d)')

    def get_colors(self, response):
        color = response.xpath("//*[@class='also_available']//*[@class = 'current_colour']/text()").extract()
        return self.take_first(color)

    def get_size(self, response):
        return response.xpath("//*[@id='size_selector']//thead/tr//text()").extract()

    def check_availability(self, response):
        return response.xpath("//tbody//td")

    def check_regular_availability(self, response):
        return response.xpath("//tbody/tr[@class = 'Regular sizing_row']//td")

    def check_long_availability(self, response):
        return response.xpath("//tbody/tr[@class = 'Long sizing_row']//td")

    def get_category(self, response):
        return response.xpath("//*[ @class = 'hide']/a/text()").extract()

    def get_gender(self, response):
        gender = response.xpath("//*[@id='crumbs']/li/a/text()").extract()
        if 'Sale' in gender:
            return gender[3].encode('utf-8').split("'")[0]
        elif 'Accessories' in gender:
            return 'Men'
        else:
            return gender[2][:-1]

    def get_retailer_sku(self, url):
        parse_url = url.split('/')
        return parse_url[-1]

    def clean_list(self, data):
        text = []
        for s in data:
            s = s.strip()
            if s.encode('utf-8'):
                text.append(s)
        return text

    def currency(self, curr_sign):
        locales = ('en_AU.utf8', 'en_BW.utf8', 'en_CA.utf8',
                   'en_DK.utf8', 'en_GB.utf8', 'en_HK.utf8', 'en_IE.utf8', 'en_IN', 'en_NG',
                   'en_PH.utf8', 'en_US.utf8', 'en_ZA.utf8',
                   'en_ZW.utf8', 'ja_JP.utf8')
        for l in locales:
            locale.setlocale(locale.LC_ALL, l)
            conv = locale.localeconv()
            if conv['currency_symbol'] == curr_sign:
                return conv['int_curr_symbol']

    def sku(self, price, color, sku, sizes, availability, long_availability):
        currency = self.currency(price[0][0].encode('utf-8'))
        price_list = []
        for pr in price:
            price_list.append(re.sub(r'[^0-9.]+', '', pr))
        item = self.put_item(color, price_list, currency)
        if not long_availability:
            for s, a in zip(sizes, availability[1:]):
                self.check_stock(self.is_available(a), item, "")
                item['size'] = s
                key = color + '_' + s if color is not None else s
                sku[key] = copy.deepcopy(item)
                self.del_stock_info('out_of_stock', item)
        else:
            for s, ra, la in zip(sizes, availability[1:], long_availability[1:]):
                self.check_stock(self.is_available(ra), item, "regular")
                self.check_stock(self.is_available(la), item, "long")
                item['size'] = s
                key = color + '_' + s if color is not None else s
                sku[key] = copy.deepcopy(item)
                self.del_stock_info('regular_out_of_stock', item)
                self.del_stock_info('long_out_of_stock', item)
            return sku

    def put_item(self, color, price_list, currency):
        if len(price_list) > 1:
            item = {'currency': currency, 'price': price_list[1], 'previous_price': price_list[0],
                    'color': color}
        else:
            item = {'currency': currency, 'price': price_list[0], 'color': color}
        return item

    def is_available(self, avail):
        return avail.xpath(".//*[@class='not_available']/text()").extract()

    def check_stock(self, is_available, item, check):
        if is_available and is_available[0].encode('utf-8') == 'Not available':
            if not check:
                item['out_of_stock'] = True
            else:
                item[check + '_out_of_stock'] = True

    def del_stock_info(self, out_of_stock, item):
        if out_of_stock in item:
            del item[out_of_stock]
