import pdb
import copy
import datetime
import js2py

from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy import Request

import schutzcrawler.items as items
from schutzcrawler.price_parser import PriceParser
from schutzcrawler.description_parser import DescriptionParser


class RoamansMixins:
    name = 'roamans'
    allowed_domains = ['roamans.com', 'f.monetate.net']
    start_urls = ['https://roamans.com/']


class ParseSpider(Spider, RoamansMixins):
    name = f"{RoamansMixins.name}-parse"
    time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M")
    price_parser = PriceParser()
    description_parser = DescriptionParser()
    size_family_url = ("https://f.monetate.net/trk/4/s/a-7736c7c2/p/allbrands.fullbeauty.com/907205417-0?"
                       + "&mi=%272.953402026.1528278326053%27&cs=!t&e=!(viewPage,gt,viewProduct)"
                       + "&pt=product&u=%27{}%27&hvc=!t&eoq=!t")
    retailer_skus = []

    def parse(self, response):
        product = items.ProductItem()

        product["url"] = response.url
        retailer_sku = self.retailer_sku(response)
        if retailer_sku in self.retailer_skus:
            return
        self.retailer_skus.append(retailer_sku)
        product["retailer_sku"] = retailer_sku
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

        product["requests"].extend(self.generate_color_requests(response, product))

        if response.css('.sizeFamily'):
            product["requests"].append(self.generate_size_family_requests(response, product))

        yield self.is_request_or_product(product)

    def parse_colors(self, response):
        product = response.meta.get('product')
        product["requests"].extend(self.generate_color_requests(response, product))
        yield self.is_request_or_product(product)

    def parse_size_family_values(self, response):
        product = response.meta.get('product')
        product["requests"].extend(self.generate_size_family_value_request(response))
        yield self.is_request_or_product(product)

    def parse_sizes(self, response):
        product = response.meta.get('product')
        product["requests"].extend(self.generate_size_requests(response))
        yield self.is_request_or_product(product)

    def parse_color_skus(self, response):
        product = response.meta['product']
        product["skus"].update(self.skus(response))
        yield self.is_request_or_product(product)

    def generate_color_requests(self, response, product):
        requests = []
        color_css = '.selectable a.color ::attr(data-href)'
        color_urls = response.css(color_css).extract()
        for color in color_urls:
            requests.append(Request(url=color, callback=self.parse_sizes,
                                    meta={'product': product}))
        return requests

    def generate_size_family_requests(self, response, product):
        url = response.url.split('?')[0]
        return Request(url=self.size_family_url.format(url), callback=self.parse_size_family_values,
                       meta={'product': product})

    def generate_size_family_value_request(self, response):
        requests = []
        product = response.meta.get('product')
        raw_text = response.text
        parsed_text = js2py.eval_js(raw_text[raw_text.find("["):raw_text.rfind("]") + 1])
        raw_size_family = [i for i in parsed_text if 'mntSwatchfamily' in str(i)]
        size_family_sel = Selector(text=dict(raw_size_family)['args'][0])

        size_family = size_family_sel.xpath('//li[@class="selectable"]/@data-swatchvalue').extract()
        url = product.get('url')
        pid = product.get('retailer_sku')
        for family in size_family:
            if 'R' in family:
                continue
            url_nxt = url.replace(pid, f"{pid}-{family}")
            requests.append(Request(url=url_nxt, callback=self.parse_color_requests,
                                    meta={'product': product}))
        return requests

    def generate_size_requests(self, response):
        requests = []
        sizes = response.css('li.selectable a.size::attr(data-href)').extract()
        for size in sizes:
            requests.append(Request(url=size, callback=self.parse_color_skus,
                                    meta={'product': response.meta.get('product')}))
        return requests

    def is_request_or_product(self, product):
        if product["requests"]:
            return product["requests"].pop()
        else:
            return product

    def skus(self, response):
        size_xpath = '//ul[@class="swatches size"]/li[contains(@class, "selected")]/span/text()'
        size = response.xpath(size_xpath).extract_first()
        color_xpath = '//ul[@class="swatches color"]/li[contains(@class, "selected")]/span/text()'
        color = response.xpath(color_xpath).extract_first()
        skus = {}
        sku = self.price(response)
        sku['color'] = color
        sku['size'] = size
        skus[f"{color}{size}"] = sku

        return skus

    def image_urls(self, response):
        images = response.xpath('//a[@name="product_detail_image"]/img/@data-desktop-src').extract()
        return [i.split('?')[0] for i in images]

    def retailer_sku(self, response):
        retailer_sku_css = '//input[@name="pid"]/@value'
        return response.xpath(retailer_sku_css).extract_first()

    def category(self, response):
        categories_xpath = '//div[@class="breadcrumb"]/a[not(contains(@class, "current-element"))]/text()'
        categories = response.xpath(categories_xpath).extract()
        return categories[1:-1]

    def product_name(self, response):
        return response.css('.top-wrap h1::text').extract_first()

    def price(self, response):
        return self.price_parser.prices(response.css('.product-price ::text').extract())

    def raw_description(self, response):
        raw_description = response.css('.product-details-description ::text').extract()
        return [d for d in raw_description if '\n' not in d and not d.isspace()]

    def description(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description[1:] if not self.description_parser.is_care(rd)]

    def care(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description[1:] if self.description_parser.is_care(rd)]


class RoamansSpider(CrawlSpider, RoamansMixins):
    name = f"{RoamansMixins.name}-crawl"
    parser = ParseSpider()

    listing_x = ['//ul[contains(@class,"menu-category")]', '//li[@class="first-last"]']
    products_xpath = '//a[@class="name-link"]'

    rules = [Rule(LinkExtractor(restrict_xpaths=listing_x), callback='parse'),
             Rule(LinkExtractor(restrict_xpaths=products_xpath), callback=parser.parse)]

    def parse(self, response):
        trail = response.meta.get('trail', [])
        trail.append(response.url)

        for request in super(RoamansSpider, self).parse(response):
            trail = copy.deepcopy(trail)
            request.meta['trail'] = trail
            yield request
