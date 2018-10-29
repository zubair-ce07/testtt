"""Orsay.com Spider"""

import json
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrap_orsay.items import OrsayItem

class OrsaySpider(CrawlSpider):

    """Orsay Crawler"""

    name = "orsay"
    allowed_domains = ["orsay.com"]
    start_urls = ["http://www.orsay.com/de-de/"]

    rules = {
        Rule(LinkExtractor(allow=(r'./produkte/\Z'))),
        # Rule(LinkExtractor(allow=(r'.*/produkte/.*.html/Z')), callback='parse_items_details'),
        Rule(LinkExtractor(allow=(r'.*/produkte/.*')), callback='parse_items'),
    }

    def parse_items(self, response):
        '''Parsing block items'''
        item_list = response.css("div.js-product-grid-portion li")
        #response.xpath("//div[contains(@class,'js-product-grid-portion')]//li").extract()
        for item in item_list:
            item_detail_url = item.css("div.product-image>a::attr(href)").extract_first()
            #response.xpath("//div[contains(@class, 'product-image')]/a/@href").extract_first()
            if item_detail_url:
                yield scrapy.Request(url=response.urljoin(item_detail_url), \
                callback=self.parse_items_details)

        next_btn = response.css("button.js-next-load").extract_first()
        #response.xpath("//button[contains(@class,'js-next-load')]/text()").extract_first().strip()
        if next_btn is not None:
            size = re.findall(r'[\d]+', response.url)[0] if re.findall(r'[\d]+', \
            response.url) else 0
            size = int(size)
            size += 72
            yield scrapy.Request(url=response.urljoin("?sz="+str(size)), callback=self.parse_items)

    def parse_items_details(self, response):
        '''Parsing item details from detail page'''
        json_data = json.loads(response.css("div.js-product-content-gtm \
        ::attr(data-product-details)").extract()[0])
        #response.xpath("//div[contains(@class,'js-product-content-gtm')] \
        # //@data-product-details").extract_first()
        product = OrsayItem()
        product = ItemLoader(item=product, response=response)
        product.add_value("name", json_data["name"])
        product.add_value("brand", json_data["brand"])
        product.add_xpath("care", "//div[contains(@class,'product-material')]/p/text()")
        product.add_value("category", json_data["categoryName"])
        product.add_xpath("description", "//div[contains(@class,'product-details')]/div/div[2]/text()")
        product.add_xpath("image_urls", "//div[@id='thumbnails']//img//@src")
        product.add_value("retailer_sku", json_data["idListRef6"])
        product.add_value("url", response.url)
        # product.add_value["skus", dict()]
        # product['skus'] = dict()
        color_scheme = dict()
        color_urls = response.css("ul.color a::attr(href)").extract()
        #response.xpath("//ul[contains(@class,'color')]//a/@href").extract()
        meta_dict = {
            "color_urls" : color_urls,
            "color_scheme" : color_scheme,
            "data" : product,
        }
        yield scrapy.Request(response.url, self.parse_item_color_scheme,\
        meta=meta_dict, dont_filter=True)

    def parse_item_color_scheme(self, response):
        """Parsing item colors"""
        json_data = json.loads(response.css("div.js-product-content-gtm::attr(data-product-details)").extract()[0])
        #response.xpath("//div[contains(@class,'js-product-content-gtm')]\
        # //@data-product-details").extract_first()
        product = response.meta['data']
        color_scheme = response.meta['color_scheme']
        color_scheme[json_data['color']+'_'+json_data['idListRef12']] = {
            "color" : json_data['color'],
            "price" : json_data['grossPrice'],
            "size" : json_data['size'],
        }
        color_urls = response.meta['color_urls']
        color_urls.remove(response.url)
        if color_urls:
            meta_data = {
                "color_urls": color_urls,
                "color_scheme": color_scheme,
                "data": product,
            }
            yield scrapy.Request(response.urljoin(color_urls[0]), self.parse_item_color_scheme,\
            meta=meta_data, dont_filter=True)
        else:
            product.add_value("skus", color_scheme)
            yield product.load_item()
