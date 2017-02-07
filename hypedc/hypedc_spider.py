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
    gender_map = [('Women', 'women'),
                  ('Men', 'men'),
                  ('Kids', 'unisex-children')]

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
        selector_css = 'ul#size-selector-desktop-tabs li'
        size_selector_elems = response.css(selector_css)
        europe_label = [e for e in size_selector_elems
                        if e.css('a::text').extract_first() in ['Europe', 'EU', 'European']]
        size_css = 'div[id^=size-selector-tab-desktop] li'
        if europe_label:
            label = europe_label.pop()
            group_i = label.css('::attr(data-sizegroup)').extract_first()
            size_css = '#size-selector-tab-desktop-{} li'.format(group_i)

        size_elems = response.css(size_css)
        prev_price, price = self.product_pricing(response)
        currency = self.product_currency(response)
        color = self.product_color(response)
        for elem in size_elems:
            size = elem.css('a::text').extract_first()
            value = elem.css('::attr(data-attributevalueid)').extract_first()
            out_of_stock = elem.css('::attr(data-stock)').extract_first() == 'out'
            sku = {
                'size': size,
                'color': color,
                'price': price,
                'currency': currency,
            }
            if prev_price:
                sku['previous_prices'] = [prev_price]
            if out_of_stock:
                sku['out_of_stock'] = True
            sku_id = '{}_{}'.format(size, value)
            skus[sku_id] = sku
        return skus

    def product_id(self, response):
        id_css = "meta[property='og:upc']::attr(content)"
        return response.css(id_css).extract_first()

    def product_brand(self, response):
        brand_css = '.product-manufacturer::text'
        return response.css(brand_css).extract_first()

    def product_name(self, response):
        title_css = "meta[property='og:title']::attr(content)"
        title = response.css(title_css).extract_first()
        brand = self.product_brand(response)
        name = title.replace(brand, '')
        return re.sub(' +', '', name)

    def product_description(self, response):
        return [d for d in self.raw_description(response) if not self.care_criteria(d)]

    def raw_description(self, response):
        desc_raw = response.css('div[itemprop=description]').extract_first()
        return self.text_from_html(desc_raw)

    def product_care(self, response):
        return [d for d in self.raw_description(response) if self.care_criteria(d)]

    def product_category(self, response):
        cat_css = 'li[class^=category] > a::attr(title)'
        return response.css(cat_css).extract()

    def product_gender(self, response):
        categories = ','.join(self.product_category(response))
        for label, gender in self.gender_map:
            if label in categories:
                return gender
        return None

    def out_of_stock(self, response):
        availability_css = "meta[property='og:availability']::attr(content)"
        availability = response.css(availability_css).extract_first()
        sold_out_css = 'button.btn-soldout'
        sold_out = response.css(sold_out_css)
        return sold_out or availability != 'instock'

    def product_currency(self, response):
        css = "meta[property='og:currency']::attr(content)"
        return response.css(css).extract_first()

    def product_pricing(self, response):
        script_css = "script:contains('Product.OptionsPrice')::text"
        json_re = 'new Product.OptionsPrice\((.*)\);'
        json_text = response.css(script_css).re_first(json_re)
        product = json.loads(json_text)
        price = CurrencyParser.float_conversion(product['productPrice'])
        old_price = None
        if product['productOldPrice']:
            old_price = CurrencyParser.float_conversion(product['productOldPrice'])
        return (old_price, price) if old_price != price else (None, price)

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
