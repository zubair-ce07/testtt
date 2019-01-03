import json

from scrapy import Spider, Request
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

        if not self.is_new_item(retailer_sku):
            return

        item['retailer_sku'] = retailer_sku
        item['name'] = self.extract_name(response)
        item['spider_name'] = 'intersport'
        item['brand'] = self.extract_brand(response)
        item['care'] = self.extract_care(response)
        item['url'] = response.url
        item['description'] = self.extract_description(response)
        item['market'] = self.extract_market()
        item['retailer'] = self.extract_retailer()
        item['trail'] = response.meta.get('trail', [])
        item['image_urls'] = self.extract_image_urls(response)
        item['category'] = self.extract_categories(response)
        item['skus'] = self.extract_skus(response)
        item['meta'] = self.extract_requests(response)

        return self.item_or_request(item)

    def extract_requests(self, response):
        request_urls = response.css('.product-information .slider-container .list-item a::attr(href)').extract()
        requests = [response.urljoin(url) for url in request_urls if url not in response.url]
        return {'requests': requests}

    def item_or_request(self, item):
        if item['meta']['requests']:
            url = item['meta']['requests'].pop()
            yield Request(url=url, callback=self.parse_color_item, meta={'item':item})
        else:
            item.pop('meta')
            yield item

    def parse_color_item(self, response):
        item = response.meta.get('item', {})
        item['skus'].update(self.extract_skus(response))
        item['image_urls'].extend(self.extract_image_urls(response))
        return self.item_or_request(item)

    def is_new_item(self, product):
        if product and product not in self.seen_ids:
            self.seen_ids.add(product)
            return True

        return False

    def extract_product_id(self, response):
        pattern = '"productPage":{"size":.*?"productNumber":"(.*?.)"'
        product_id = response.xpath("//script/text()").re_first(pattern)
        if not product_id:
            return None

        color = self.extract_color(response)
        return f"{product_id}_{color}"

    def extract_description(self, response):
        description = response.css('.iceberg-body .m-b-half p::text').extract_first()
        return [des.strip() for des in description.split('.') if des.strip()]

    def extract_name(self, response):
        return response.css('.product-name::text').extract_first()

    def extract_care(self, response):
        return response.css('.iceberg-body .list-item::text').extract()

    def extract_brand(self, response):
        return response.css('.product-information .product-meta .list-item::text').extract_first()

    def extract_categories(self, response):
        return response.css('.iceberg-body .list-item a::text').extract()

    def extract_image_urls(self, response):
        return response.css('.images a::attr(href)').extract()

    def extract_skus(self, response):
        skus = {}
        price = self.extract_price(response)
        common_sku = extract_price_details(price)
        common_sku['color'] = self.extract_color(response)
        raw_skus = self.extract_raw_skus(response)

        for raw_sku in json.loads(raw_skus):
            sku = common_sku.copy()
            sku['size'] = raw_sku['label']
            sku['sku_id'] = f"{common_sku['color']}_{sku['size']}"
            stock = raw_sku['saldo']
            if not stock or stock[0]['quantityAvailable'] < 1:
                sku['out_of_stock'] = True

            skus[sku['sku_id']] = sku

        return skus

    def extract_color(self, response):
        css = '.product-information .product-meta .list-item:nth-child(3)::text'
        return response.css(css).extract_first()

    def extract_market(self):
        return 'SE'

    def extract_price(self, response):
        price_details = []
        xpath = response.xpath("//script/text()")

        price_details.append(xpath.re_first('"product":{.*?"price":{"price":"(.*?.)"'))
        price_details.append(xpath.re_first('"product":{.*?"regularPrice":"(.*?.)"'))
        price_details.append(self.extract_currency())

        return price_details

    def extract_retailer(self):
        return 'intersport.se'

    def extract_currency(self):
        return 'SEK'

    def extract_raw_skus(self, response):
        xpath = "//script[contains(., 'sizes')]/text()"
        pattern = '"sizes":(.*),"supplierItemNumber"'
        return response.xpath(xpath).re_first(pattern)

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
        return title.split('|')[0] or None
