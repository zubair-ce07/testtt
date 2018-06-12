import scrapy
import copy
import re
import datetime
import js2py

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

import schutzcrawler.items as items
from schutzcrawler.price_parser import PriceParser
from schutzcrawler.description_parser import DescriptionParser


class RoamansMixins:
    name = 'roamans'
    allowed_domains = ['roamans.com', 'f.monetate.net']
    start_urls = ['https://roamans.com/']


class ParseSpider(CrawlSpider, RoamansMixins):
    name = f"{RoamansMixins.name}-parse"
    time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M")
    price_parser = PriceParser()
    description_parser = DescriptionParser()

    def parse(self, response):
        product = items.ProductItem()

        product["url"] = response.url
        product["retailer_sku"] = self.retailer_sku(response)
        product["gender"] = "women"
        product["retailer"] = "roamans-us"
        product["category"] = self.category(response)
        product["url_original"] = response.url
        product["name"] = self.product_name(response)
        product["spider_name"] = self.name
        product["description"] = self.description(response)
        product["care"] = self.care(response)
        product["trail"] = response.meta.get('trail', [])
        product["skus"] = {}
        product["crawl_start_time"] = self.time
        product["image_urls"] = self.image_urls(response)
        product["requests"] = []

        self.generate_size_requests(response, product)

        if response.css('.sizeFamily'):
            self.generate_size_family_requests(response, product)
        
        yield self.is_request_or_product(product)
        
    def is_request_or_product(self, product):
        if product["requests"]:
            return product["requests"].pop()
        else:
            return product

    def generate_size_requests(self, response, product):
        sizes = response.css('.selectable a.size::attr(data-href)').extract()
        for size in sizes:
            product.get("requests", []).append(scrapy.Request(url=size, callback=self.parse_color_skus,
                                                              meta={'product': product}))
    
    def generate_size_family_requests(self, response, product):
        url = response.url.split('?')[0]
        size_family_url = (f"https://f.monetate.net/trk/4/s/a-7736c7c2/p/allbrands.fullbeauty.com/907205417-0?"
                           + f"&mi=%272.953402026.1528278326053%27&cs=!t&e=!(viewPage,gt,viewProduct)"
                           + f"&pt=product&u=%27{url}%27&hvc=!t&eoq=!t")
        product.get("requests", []).append(scrapy.Request(url=size_family_url, callback=self.parse_size_family_values,
                                                          meta={'product': product}))
        
    def parse_size_family_values(self, response):
        size_family_sel = {}
        product = response.meta.get('product')

        response_js_text = response.text
        response_py = js2py.eval_js(response_js_text[response_js_text.find("["):response_js_text.rfind("]")+1])
        for item in response_py:
            if 'mntSwatchfamily' in str(item):
                size_family_sel = item
        size_family_sel = Selector(text=size_family_sel['args'][0])
        size_family = size_family_sel.xpath('//li[@class="selectable"]/@data-swatchvalue').extract()
        
        url = product.get('url')
        pid = product.get('retailer_sku')
        for family in size_family:
            if 'R' not in family:
                url_nxt = url.replace(pid, f"{pid}-{family}")
                product.get("requests", []).append(scrapy.Request(url=url_nxt, callback=self.parse_sizes,
                                                                  meta={'product': product}))
        yield self.is_request_or_product(product)

    def parse_sizes(self, response):
        requests = []
        sizes = response.css('.selectable a.size::attr(data-href)').extract()
        product = response.meta.get('product')
        for size in sizes:
            product.get("requests", []).append(scrapy.Request(url=size, callback=self.parse_color_skus,
                                                              meta={'product': product}))
            yield self.is_request_or_product(product)

    def parse_color_skus(self, response):
        xpath = '//ul[@class="swatches size"]/li[@class="selectable selected"]/span/text()'
        size = response.xpath(xpath).extract_first()
        raw_colors = response.xpath('//ul[@class="swatches color"]/li/span/text()').extract()
        colors = [c for c in raw_colors if re.match('^[a-zA-Z]+', c)]
        common_sku = self.price(response)
        skus = {}
        for color in colors:
            sku = copy.deepcopy(common_sku)
            sku['color'] = color
            sku['size'] = size
            skus[f"{color}{size}"] = sku

        product = response.meta['product']
        skus.update(product["skus"])
        product["skus"] = skus
        
        yield self.is_request_or_product(product)

    def image_urls(self, response):
        images = response.xpath('//a[@name="product_detail_image"]/img/@data-desktop-src').extract()
        return [i.split('?')[0] for i in images]

    def retailer_sku(self, response):
        retailer_sku_css = '//input[@name="pid"]/@value'
        return response.xpath(retailer_sku_css).extract_first()

    def category(self, response):
        name = self.product_name(response)
        categories_css = '.breadcrumb a::text'
        categories = response.css(categories_css).extract()
        return [c.strip('\n') for c in categories[1:] if name not in c]

    def product_name(self, response):
        return response.css('.top-wrap h1::text').extract_first()

    def price(self, response):
        return self.price_parser.prices(response.css('.product-price ::text').extract())
    
    def raw_description(self, response):
        raw_description = response.css('.product-details-description ::text').extract()
        return [d for d in raw_description if '\n' not in d]

    def description(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description[1:] if not self.description_parser.is_care(rd)]

    def care(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description[1:] if self.description_parser.is_care(rd)]


class RoamansSpider(CrawlSpider, RoamansMixins):
    name = f"{RoamansMixins.name}-crawl"
    parser = ParseSpider()

    category_xpath = '//ul[contains(@class,"menu-category")]'
    products_xpath = '//a[@class="name-link"]'
    pagination_xpath = '//li[@class="first-last"]'

    rules = [Rule(LinkExtractor(restrict_xpaths=[category_xpath,pagination_xpath]), callback='parse'),
             Rule(LinkExtractor(restrict_xpaths=products_xpath), callback=parser.parse)]

    def parse(self, response):
        trail = response.meta.get('trail', [])
        trail.append(response.url)

        for request in list(super(RoamansSpider, self).parse(response)):
            trail = copy.deepcopy(trail)
            request.meta['trail'] = trail
            yield request
