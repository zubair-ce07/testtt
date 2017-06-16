import re

import yaml
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from kmart_scraper.items import KmartItem


class KmartSpider(CrawlSpider):
    name = "kmart"
    allowed_domains = ['kmart.com.au']
    start_urls = ["http://www.kmart.com.au"]
    pagination_regex = re.compile(r"\'http.*?\'")

    rules = (
        Rule(LinkExtractor(restrict_css=['li.mega-menu li>a']), callback="handle_pagination", follow=True),
        Rule(LinkExtractor(restrict_css=['.product_image>a']), callback="parse_item"),
    )

    def handle_pagination(self, response):
        pages_count = int(response.css("#pages_list_id li:nth-last-child(2) ::text").extract_first() or '0')
        if not pages_count:
            return
        script_occurrence = response.xpath('//script[contains(text(),\'SearchBasedNavigationDisplayJS.init(\')]')
        pagination_url = script_occurrence.re(self.pagination_regex)
        for count in range(1, pages_count):
            begin_index = product_begin_index = count*30
            url = (pagination_url[0])[1:-1]
            yield FormRequest(url, formdata={
                                  'contentBeginIndex': '0',
                                  'productBeginIndex': str(product_begin_index),
                                  'beginIndex': str(begin_index),
                                  'orderBy': '5',
                                  'isHistory': 'false',
                                  'pageView': 'grid',
                                  'resultType': 'products',
                                  'langId': '-1',
                                  'pageSize': '30',
                                  'requesttype': 'ajax'})

    def parse_item(self, response):
        item = KmartItem()
        item['name'] = self.get_name(response)
        item['image_urls'] = self.get_image_urls(response)
        item['description'] = self.get_description(response)
        item['price'] = self.get_price(response)
        item['url'] = response.url
        item['skus'] = self.get_skus(response) or {
            "colour": 'no-color',
            "currency": "AUD",
            "price": item['price'],
            "sku_id": 'none',
            "size": 'one-size'
        }
        return item

    def get_name(self, response):
        return response.css('.h2[itemprop = "name"] ::text').extract_first()

    def get_image_urls(self, response):
        image_urls = response.css('.multipleimages + input ::attr(value)').extract() or \
                     response.css('#productMainImage ::attr(src)').extract()
        return [self.start_urls[0] + s for s in image_urls]

    def get_description(self, response):
        return response.css('#product-details li ::text, #product-details p ::text').extract()

    def get_price(self, response):
        return response.css('.price-wrapper [itemprop="price"] ::text').extract_first()

    def get_skus(self, response):
        json_wo_quotes = response.css('#catEntryParams ::attr(value)').extract_first()
        try:
            skus_json = yaml.load(json_wo_quotes)
        except:
            skus_json = yaml.load(json_wo_quotes.replace("'", '"'))
        skus_data = skus_json['skus']
        price = self.get_price(response)

        skus = []
        for sku in skus_data:
            curr_sku = {
                "colour": sku['attributes']['Colour'],
                "currency": "AUD",
                "price": price,
                "sku_id": sku['id'],
                "size": sku['attributes']['Size']
            }
            skus.append(curr_sku)
        return skus
