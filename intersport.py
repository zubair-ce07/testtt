import json

from scrapy import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from item_structure import Item
from helpers import extract_price_details


class ProductParser(Spider):
    def __init__(self):
        self.seen_ids = set()

    def parse(self, response):
        item = Item()
        retailer_sku = self.extract_product_id(response)
        color = self.extract_color(response)
        product_id = f"{retailer_sku}_{color}"

        if not self.is_new_item(product_id):
            return

        item['retailer_sku'] = retailer_sku
        item['name'] = self.extract_name(response)
        item['spider_name'] = 'intersport'
        item['brand'] = self.extract_brand(response)
        item['url'] = response.url
        item['description'] = self.extract_description(response)
        item['market'] = self.extract_market()
        item['retailer'] = self.extract_retailer()
        item['trail'] = response.meta.get('trail', [])
        item['image_urls'] = self.extract_image_urls(response)
        item['category'] = self.extract_categories(response)
        item['skus'] = self.extract_skus(response)

        return item

    def is_new_item(self, product):
        if product and product not in self.seen_ids:
            self.seen_ids.add(product)
            return True

        return False

    def extract_product_id(self, response):
        product_id = response.xpath("//script/text()").re('"productPage":(.*)')
        if product_id:
            product_page = json.loads('{"productPage":'+product_id[0])
            product_id = product_page['productPage']['productNumber']

        return product_id

    def extract_description(self, response):
        description = response.css('.iceberg-body .m-b-half p::text').extract_first()
        return [des.strip() for des in description.split('.') if des.strip()]

    def extract_name(self, response):
        return response.css('.product-name::text').extract_first()

    def extract_brand(self, response):
        return response.css('.product-information .product-meta .list-item::text').extract_first()

    def extract_categories(self, response):
        return response.css('.iceberg-body .list-item a::text').extract()

    def extract_image_urls(self, response):
        return response.css('.images a::attr(href)').extract()

    def extract_skus(self, response):
        skus, product_price = [], []
        price_details = self.extract_price(response)
        product_price.append(price_details['regularPrice'])
        product_price.append(price_details['price'])
        product_price.append(self.extract_currency())
        price_details = extract_price_details(product_price)

        item = {}
        item['color'] = self.extract_color(response)
        item.update(price_details)
        size_options = response.css('.button-list .item-button:enabled::text').extract()

        for option in size_options:
            size_option = item.copy()
            size_option['size'] = option
            size_option['sku_id'] = f"{item['color']}_{option}"
            skus.append(size_option)

        return skus

    def extract_color(self, response):
        return response.css('.product-information .product-meta .list-item:nth-child(3)::text').extract_first()

    def extract_market(self):
        return 'SE'

    def extract_price(self, response):
        price_details = response.xpath("//script/text()").re('("product":.*)')
        return json.loads("{" + price_details[0])['product']['price']

    def extract_retailer(self):
        return 'intersport.se'

    def extract_currency(self):
        return 'SEK'


class InterSportSpider(CrawlSpider):
    name = 'intersport-crawl-spider'
    allowed_domains = ['www.intersport.se']
    start_urls = ['https://www.intersport.se/']
    product_parser = ProductParser()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36'
    }

    product_css = ['.top-row-nav-container', '.nav-container']
    listing_css = ['.container','.slider-container']
    rules = [
        Rule(LinkExtractor(restrict_css=product_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_item')
    ]

    def parse(self, response):
        title = self.extract_title(response)
        trail = response.meta.get('trail', [])
        trail = trail + [[title, response.url]]

        for request in super().parse(response):
            request.meta['trail'] = trail
            yield request

    def parse_item(self, response):
        return self.product_parser.parse(response)

    def extract_title(self, response):
        title = response.css('title::text').extract_first()
        return title.split('|')[0] if title else title
