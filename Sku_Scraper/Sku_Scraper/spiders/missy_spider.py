import json
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from ..items import Product


class MissyParseSpider(scrapy.Spider):
    name = "missy_parse_spider" 

    def parse(self, response):
        product_loader = ItemLoader(item=Product(), response=response)

        product_id = self.extract_pid(response)
        product_loader.add_value('pid', product_id)

        gender = self.detect_gender(response)
        product_loader.add_value('gender', gender)

        category = self.extract_category(response)
        product_loader.add_value('category', category)

        url = self.get_product_url(response)
        product_loader.add_value('url', url)

        name = self.extract_name(response)
        product_loader.add_value('name', name)

        description = self.extract_description(response)
        product_loader.add_value('description', description)

        image_urls = self.extract_image_urls(response)
        product_loader.add_value('image_urls', image_urls)

        skus = self.extract_skus(response)
        product_loader.add_value('skus', skus)

        yield product_loader.load_item()

    def extract_pid(self, response):
        css = '[name="product"]::attr(value)'
        return response.css(css).extract_first()

    def detect_gender(self, response):
        return 'women'

    def extract_category(self, response):
        css = '.breadcrumbs a::text, .product strong::text'
        return response.css(css).extract()

    def get_product_url(self, response):
        return response.url

    def extract_name(self, response):
        css = '.detail-produt-name::text'  
        return response.css(css).extract_first().strip()

    def extract_description(self, response):
        css = '.short-des > ul span::text'
        return response.css(css).extract()

    def extract_image_urls(self, response):
        css = '.cloud-zoom-gallery > img::attr(data-lazy)'
        return response.css(css).extract()

    def extract_skus(self, response):
        skus = []
        price_css = '[itemprop="priceCurrency"]::attr(content)'
        price = response.css(price_css).extract_first()

        currency_css = '[itemprop="price"]::attr(content)' 
        currency = response.css(currency_css).extract_first()

        colour_css = '.color-title > span::text'
        raw_colour = response.css(colour_css).extract_first()
        colour = raw_colour.split(':')[1].strip() if raw_colour else ""

        raw_sizes = self.extract_raw_sizes(response)
        raw_stocks = self.extract_availability(response)

        common_sku = {
            "price" : price,
            "currency" : currency
        }

        if colour:
            common_sku["colour"] = colour

        for raw_size in raw_sizes:
            sku = common_sku.copy()

            size = raw_size["label"]
            sku["size"] = size

            if raw_stocks[raw_size["products"][0]] != "1":
                sku["out_of_stock"] = True
    
            sku["sku_id"] = f"{colour}_{size}" if colour else f"{size}"
    
            skus.append(sku)

        return skus

    def extract_raw_sizes(self, response):
        raw_sizes_x = '//script[contains(., "new Product.Config")]/text()'
        raw_sizes = response.xpath(raw_sizes_x).re_first(r'{.*}')
        raw_sizes = json.loads(raw_sizes)
        return raw_sizes["attributes"]["173"]["options"]

    def extract_availability(self, response):
        raw_stock_x = '//script[contains(., "switcherConfig")]/text()' 
        raw_stocks = response.xpath(raw_stock_x).re_first(r'{.*}')
        raw_stocks = json.loads(raw_stocks)
        return raw_stocks["stock"]
             

class MissyCrawlSpider(CrawlSpider):
    name = "missy_crawl_spider"
    start_urls = ["https://www.missyempire.com"]
    allowed_domains = ["missyempire.com"]
    parse_spider = MissyParseSpider()

    listings_css = ['.parent', '.i-next']
    product_css = '.list-page .each-product .product-image'

    rules = (
        Rule(LinkExtractor(restrict_css=(listings_css))),
        Rule(LinkExtractor(restrict_css=(product_css)), callback="parse_item"),
    )
    
    def parse_item(self, response):
        return self.parse_spider.parse(response)
        
