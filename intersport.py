import json

from scrapy import Spider, Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

from item_structure import Item
from helpers import extract_price_details, extract_gender, item_or_request


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
        item['gender'] = self.extract_gender(response)
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
        item['meta'] = {'requests': self.extract_colour_requests(response)}

        return item_or_request(item)

    def parse_colour_item(self, response):
        item = response.meta.get('item', {})
        item['skus'].update(self.extract_skus(response))
        item['image_urls'] += self.extract_image_urls(response)
        return item_or_request(item)

    def extract_colour_requests(self, response):
        css = '.product-information .slider-container .list-item a:not([class^="item-link is-active"])::attr(href)'
        urls = response.css(css).extract()
        return [Request(url=response.urljoin(url), callback=self.parse_colour_item) for url in urls]

    def is_new_item(self, product):
        if product and product not in self.seen_ids:
            self.seen_ids.add(product)
            return True

        return False

    def extract_product_id(self, response):
        pattern = '"productPage":{"size":.*?"productNumber":"(.*?.)"'
        return response.xpath("//script/text()").re_first(pattern)

    def extract_description(self, response):
        description = response.css('.iceberg-body .m-b-half p::text').extract()
        if not description:
            return description
        return [des.strip() for des in description[0].split('.') if des.strip()]

    def extract_name(self, response):
        return response.css('.product-name::text').extract_first()

    def extract_care(self, response):
        return response.css('.iceberg-body .list-item::text').extract()

    def extract_brand(self, response):
        return response.css('.product-information .product-meta .list-item::text').extract_first()

    def extract_categories(self, response):
        category = response.css('.iceberg-body .list-item a::text').extract()
        return [cat.strip() for cat in category if cat.strip()]

    def extract_image_urls(self, response):
        return response.css('.images a::attr(href)').extract()

    def extract_skus(self, response):
        skus = {}
        common_sku = extract_price_details(self.extract_price(response))
        common_sku['colour'] = self.extract_colour(response)

        for raw_sku in self.extract_raw_skus(response):
            sku = common_sku.copy()
            sku['size'] = raw_sku['label']
            stock = raw_sku['saldo']
            if not stock or stock[0]['quantityAvailable'] < 1:
                sku['out_of_stock'] = True

            skus[f"{common_sku['colour']}_{sku['size']}"] = sku

        return skus

    def extract_colour(self, response):
        css = '.product-information .product-meta .list-item:nth-child(3)::text'
        return response.css(css).extract_first()

    def extract_market(self):
        return 'SE'

    def extract_gender(self, response):
        product_info = ' '.join(response.css('.product-information-head *::text').extract())
        return extract_gender(product_info)

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
        raw_skus = response.xpath(xpath).re_first(pattern)
        return json.loads(raw_skus)


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
