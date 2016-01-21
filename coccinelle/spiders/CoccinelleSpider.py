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
        "http://www.coccinelle.com/gb_en"]
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
        cat_sku = self.get_category(response)
        item['category'] = cat_sku[0]
        item['retailer_sku'] = cat_sku[1]
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
        colors = response.xpath(
                "//*[@class ='product-options']//*[contains(@class , 'swatches_single-swatch swatch_color')]"
                "/img/@alt").extract()
        price = response.xpath(
                "//*[@class = 'product-type-data clearer']//*[@class= 'special-price' or @class= 'regular-price']"
                "//*[@class='price']/text()").extract()

        price = self.clean_list(price)
        currency = self.currency(price[0][0].encode('utf-8'))
        price = re.sub(r'[^0-9.]+', '', price[0])
        sku = {}
        for c in colors:
            item = {'currency': currency, 'price': price, 'color': c, 'size': 'One Size'}
            sku[c + '_One size'] = item
        if colors:
            sku['_One Size'] = {'currency': currency, 'price': price, 'color': '', 'size': 'One Size'}
        return sku

    def get_category(self, response):
        script = response.xpath("//script[contains(text(), 'cateory')]/text()")
        category = script.re('cateory":"([^\"]+)')
        retailer_sku = script.re('sku":"([^\"]+)')
        return category, retailer_sku

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
