import json
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, CurrencyParser


class Mixin:
    allowed_domains = ["www.hypedc.com"]
    start_urls = ['http://www.hypedc.com/mens/']
    market = 'US'
    retailer = 'hypedc-us'

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
        if self.out_of_stock(response):
            garment['out_of_stock'] = True
        return garment

    def image_urls(self, response):
        return response.css('ul.slides img::attr(data-src)').extract()

    def skus(self, response):
        skus = {}
        categories = self.product_category(response)
        footwear_categories = ['Men\'s Footwear', 'Women\'s Footwear', 'Kid\'s Footwear']

        if any(c in footwear_categories for c in categories):
            size_selector_elems = response.css('ul#size-selector-desktop-tabs li')
            europe_label = [e for e in size_selector_elems
                            if e.css('a::text').extract_first() == 'Europe' ]
            if europe_label:
                europe_label = europe_label.pop()
                group_i = europe_label.css('::attr(data-sizegroup)').extract_first()
                size_elems = response.css('#size-selector-tab-desktop-{} li'.format(group_i))
                for elem in size_elems:
                    size = elem.css('a::text').extract_first()
                    value = elem.css('::attr(data-attributevalueid)').extract_first()
                    out_of_stock = elem.css('::attr(data-stock)').extract_first() == 'out'
                    skus.update(self.sku(response, size, value, out_of_stock))
        else:
            size_elems = response.css('div[id^=size-selector-tab-desktop] li')
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
            '{}_{}'.format(size, value) : sku
        }


    def product_id(self, response):
        return response.css('meta[property=og\:upc]::attr(content)').extract_first()

    def product_brand(self, response):
        return response.css('.product-manufacturer::text').extract_first()

    def product_name(self, response):
        title = response.css('meta[property=og\:title]::attr(content)').extract_first()
        brand = self.product_brand(response)
        return title.replace(brand,'')

    def product_description(self, response):
        return self.text_from_html(response.css('div[itemprop=description]').extract_first())

    def product_care(self, response):
        desc = self.product_description(response)
        care = []
        for line in desc:
            if self.care_criteria(line):
                care.append(line)
        return care

    def product_category(self, response):
        return response.css('li[class^=category] > a::attr(title)').extract()

    def product_gender(self, response):
        categories = self.product_category(response)
        gender_map = [('Mens', 'men'),
                      ('Womens', 'women'),
                      ('Kids', 'unisex-children')]
        for label, gender in gender_map:
            if label in categories:
                return gender
        return None

    def out_of_stock(self, response):
        return response.css('meta[property=og\:availability]::attr(content)').extract_first() != 'instock'

    def product_currency(self, response):
        return response.css('meta[property=og\:currency]::attr(content)').extract_first()

    def product_pricing(self, response):
        script = response.css('script:contains(Product\.OptionsPrice)::text').extract_first()
        script = script.replace('var optionsPrice = new Product.OptionsPrice(','')
        json_text = script[:-3]
        product = json.loads(json_text)
        price = CurrencyParser.float_conversion(product['productPrice'])
        if product['productOldPrice']:
            oldPrice = CurrencyParser.float_conversion(product['productOldPrice'])
            return oldPrice, price
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

if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute('scrapy parse --spider hypedc-us-parse https://www.hypedc.com/rocco-tan-perf-232260.html'.split())