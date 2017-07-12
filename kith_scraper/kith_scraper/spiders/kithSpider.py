import json
import re

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule

from kith_scraper.items import KithItem


class KithSpider(CrawlSpider):
    name = "kith"
    start_urls = ['https://kith.com']
    allowed_domains = ['kith.com']
    restrict_css = ['.ksplash-header-upper-items',
                    '.main-nav-list-item',
                    ]
    rules = (
        Rule(LinkExtractor(restrict_css=restrict_css)),
        Rule(LinkExtractor(restrict_css='.product-card-info'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = KithItem()

        item['retailer_sku'] = self.get_retailer_sku(response)
        item['skus'] = self.get_skus(response)
        item['brand'] = self.get_brand(response)
        item['category'] = self.get_category(response)
        item['description'] = self.get_description(response)
        item['gender'] = self.get_gender(response)
        item['image_url'] = self.get_image_urls(response)
        item['name'] = self.get_name(response, item['brand'])
        item['retailer'] = self.get_retailer()
        item['url'] = response.url

        yield item

    def get_skus(self, response):
        product_skus = {}
        currency = self.get_currency(response)
        color = self.get_color(response)
        price = self.get_price(response)

        regex_for_skus_json = '(\[{"id".*available.*}\])'
        raw_skus_json = response.css('script').re_first(regex_for_skus_json)
        skus_json = json.loads(raw_skus_json)
        for sku_item in skus_json:
            product_skus[sku_item['id']] = {'color': color,
                                            'currency': currency,
                                            'price': price,
                                            'size': sku_item["title"],
                                            'availability': sku_item["available"],
                                            }

        return product_skus

    def get_description(self, response):
        raw_descriptions = response.css('.product-single-details-rte p::text').extract()
        return [description.strip() for description in raw_descriptions if description.strip()]

    def get_category(self, response):
        return response.css('.breadcrumb a::text').extract()[1:]

    def get_image_urls(self, response):
        raw_urls = response.css(".super-slider-photo-img::attr(src)").extract()
        image_urls = [url.strip('/') for url in raw_urls]
        return image_urls

    def get_brand(self, response):
        return response.css(".analytics::text").re_first('"brand":"(.*?)"')

    def get_name(self, response, brand):
        product_title = response.css('.product-header-title span::text').extract_first()
        brand_pattern = re.compile(re.escape(brand), re.IGNORECASE)
        name = brand_pattern.sub('', product_title)
        return name

    def get_color(self, response):
        color = response.css('.-variant::text').extract_first()
        if not color:
            return
        return color.strip()

    def get_price(self, response):
        return response.css(".analytics::text").re('"price":"([0-9]*\.?[0-9]*)"')[0]

    def get_currency(self, response):
        return response.css(".analytics::text").re('"currency":"(\w+)"')[0]

    def get_retailer_sku(self, response):
        return response.css(".analytics::text").re('"productId":(\d+)')[0]

    def get_retailer(self):
        return 'kith-us'

    def get_gender(self, response):
        if 'wmns' in response.url:
            return 'Women'
        if 'kidset' in response.url:
            return 'Kids'
        return 'Men'
