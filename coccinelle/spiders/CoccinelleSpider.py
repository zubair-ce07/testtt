import scrapy
from coccinelle.items import CoccinelleItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import locale
import re


class CoccinelleSpider(CrawlSpider):
    name = "coccinelle"
    allowed_domains = ["coccinelle.com"]
    start_urls = [
        "http://www.coccinelle.com/gb_en/"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//*[@id='nav']/li", "//*[@class='next']",))),
        Rule(LinkExtractor(allow=(".html",),
                           restrict_xpaths=("//*[@class = 'item' or @class ='item product_big right']",)),
             callback='parse_product'),
    )

    def parse_product(self, response):
        item = CoccinelleItem()
        item['description'] = self.get_description(response)
        item['image_urls'] = self.get_image_urls(response)
        item['name'] = self.get_product_name(response)
        item['url'] = response.url
        item['sku'] = self.get_sku(response)
        item['category'] = self.get_category(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['gender'] = 'women'
        item['brand'] = 'Coccinelle'
        yield item

    def get_description(self, response):
        return self.clean_list(response.xpath(
                "//*[@class='product-view_tabs']//*[@class='panel']//text()").extract())

    def get_image_urls(self, response):
        return self.clean_list(response.xpath(
                "//*[@class='more-views']//img/@src").extract())

    def get_product_name(self, response):
        return response.xpath("//*[@class='product-name']/h1/text()").extract()

    def get_sku(self, response):
        colors = self.get_colors(response)
        price = self.get_price(response)
        sku = {}
        self.sku(price, colors, sku)
        return sku

    def get_price(self, response):
        return response.xpath("//*[@class = 'product-type-data clearer'] //*[@class='price']/text()").extract()

    def get_colors(self, response):
        return response.xpath(
                "//*[@class ='product-options']//*[contains(@class , 'swatches_single-swatch swatch_color')]"
                "/img/@alt").extract()

    def get_category(self, response):
        return response.xpath("//script[contains(text(), 'cateory')]/text()").re('cateory":"([^\"]+)')

    def get_retailer_sku(self, response):
        return response.xpath("//script[contains(text(), 'cateory')]/text()").re('sku":"([^\"]+)')

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

    def sku(self, price, colors, sku):
        price = self.clean_list(price)
        currency = self.currency(price[0][0].encode('utf-8'))
        price_list = []
        for pr in price:
            price_list.append(re.sub(r'[^0-9.]+', '', pr))
        for c in colors:
            self.put_item(c, price_list, sku, currency)

        if not colors:
            self.put_item('', price_list, sku, currency)
        return sku

    def put_item(self, color, price_list, sku, currency):
        if len(price_list) > 1:
            item = {'currency': currency, 'price': price_list[0], 'previous_price': price_list[1],
                    'color': color, 'size': 'One Size'}
        else:
            item = {'currency': currency, 'price': price_list[0], 'color': color, 'size': 'One Size'}
        sku[color + '_One size'] = item
        return sku
