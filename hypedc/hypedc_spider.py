import json
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, CurrencyParser


class Mixin:
    allowed_domains = ["www.hypedc.com"]
    start_urls = ['http://www.hypedc.com/mens/']
    market = 'AU'
    retailer = 'hypedc-au'


class HypeDcParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)
        if self.out_of_stock(response) or not garment['skus']:
            garment['out_of_stock'] = True
        return garment

    def image_urls(self, response):
        css = 'ul.slides img::attr(data-src)'
        return response.css(css).extract()

    def skus(self, response):
        skus = {}
        categories = self.product_category(response)
        if self.is_footwear_category(categories):
            selector_css = 'ul#size-selector-desktop-tabs li'
            size_selector_elems = response.css(selector_css)
            europe_label = [e for e in size_selector_elems
                            if e.css('a::text').extract_first() in ['Europe', 'EU', 'European']]
            if europe_label:
                label = europe_label.pop()
                group_i = label.css('::attr(data-sizegroup)').extract_first()
                elems_css = '#size-selector-tab-desktop-{} li'.format(group_i)
                size_elems = response.css(elems_css)
                skus.update(self.sku_from_size_elems(response, size_elems))
                return skus

        size_elems = response.css('div[id^=size-selector-tab-desktop] li')
        skus.update(self.sku_from_size_elems(response, size_elems))
        return skus

    def is_footwear_category(self, categories):
        footwear_categories = ['Men\'s Footwear',
                               'Women\'s Footwear',
                               'Kid\'s Footwear'
                               ]
        return any(c in footwear_categories for c in categories)

    def sku_from_size_elems(self, response, size_elems):
        skus = {}
        for elem in size_elems:
            size = elem.css('a::text').extract_first()
            value = elem.css('::attr(data-attributevalueid)').extract_first()
            out_of_stock = elem.css('::attr(data-stock)').extract_first() == 'out'
            skus.update(self.sku(response, size, value, out_of_stock))
        return skus

    def sku(self, response, size, value, out_of_stock):
        prev_price, price = self.product_pricing(response)
        currency = self.product_currency(response)
        color = self.product_color(response)
        sku = {
            'size': size,
            'color': color,
            'price': price,
            'currency': currency,
        }
        if prev_price:
            sku.update({'previous_prices': [prev_price]})
        if out_of_stock:
            sku.update({'out_of_stock': True})
        return {
            '{}_{}'.format(size, value): sku
        }

    def product_id(self, response):
        id_css = 'meta[property=og\:upc]::attr(content)'
        return response.css(id_css).extract_first()

    def product_brand(self, response):
        brand_css = '.product-manufacturer::text'
        return response.css(brand_css).extract_first()

    def product_name(self, response):
        title_css = 'meta[property=og\:title]::attr(content)'
        title = response.css(title_css).extract_first()
        brand = self.product_brand(response)
        return title.replace(brand, '')

    def product_description(self, response):
        desc_raw = response.css('div[itemprop=description]').extract_first()
        return self.text_from_html(desc_raw)

    def product_care(self, response):
        desc = self.product_description(response)
        care = []
        for line in desc:
            if self.care_criteria(line):
                care.append(line)
        return care

    def product_category(self, response):
        cat_css = 'li[class^=category] > a::attr(title)'
        return response.css(cat_css).extract()

    def product_gender(self, response):
        categories = self.product_category(response)
        gender_map = [('Mens', 'men'),
                      ('Men\'s Sale', 'men'),
                      ('Womens', 'women'),
                      ('Women\'s Sale', 'women'),
                      ('Kids', 'unisex-children'),
                      ('Kid\'s Sale', 'unisex-children')]
        for label, gender in gender_map:
            if label in categories:
                return gender
        return None

    def out_of_stock(self, response):
        availability_css = 'meta[property=og\:availability]::attr(content)'
        availability =  response.css(availability_css).extract_first()
        sold_out_css = 'button.btn-soldout'
        sold_out = response.css(sold_out_css)
        return sold_out or availability != 'instock'

    def product_currency(self, response):
        css = 'meta[property=og\:currency]::attr(content)'
        return response.css(css).extract_first()

    def product_pricing(self, response):
        script_css = 'script:contains(Product\.OptionsPrice)::text'
        script = response.css(script_css).extract_first()
        find = 'var optionsPrice = new Product.OptionsPrice('
        script = script.replace(find, '')
        json_text = script[:-3]
        product = json.loads(json_text)
        price = CurrencyParser.float_conversion(product['productPrice'])
        if product['productOldPrice']:
            old_price = CurrencyParser.float_conversion(product['productOldPrice'])
            if old_price != price:
                return old_price, price
        return None, price

    def product_color(self, response):
        return response.css('.product-colour::text').extract_first()


class HypeDcCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = HypeDcParseSpider()

    listing_css = [
        ".nav-primary",
        ".next"
    ]

    product_css = [
        ".item"
    ]

    rules = (Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'))

