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
    categories_selector = '.mega-menu li>a'
    item_card_selector = '.product_image>a'
    allowed_categories = ['/category/men/mens-clothing/',
                          '/category/women/womens-clothing/',
                          '/kids-clothing/',
                          '/baby-manchester/',
                          '/baby-clothing/']

    rules = (
        Rule(LinkExtractor(allow=allowed_categories, restrict_css=[categories_selector]), callback="handle_pagination",
             follow=True),
        Rule(LinkExtractor(restrict_css=[item_card_selector]), callback="parse_item"),
    )

    def handle_pagination(self, response):
        pages_count_selector = "#pages_list_id li:nth-last-child(2) ::text"
        pages_count = int(response.css(pages_count_selector).extract_first() or '0')

        pagination_xpath = '//script[contains(text(),\'SearchBasedNavigationDisplayJS.init(\')]'
        pagination_url = response.xpath(pagination_xpath).re(self.pagination_regex)

        for count in range(1, pages_count):
            begin_index = product_begin_index = count * 30
            url = (pagination_url[0])[1:-1]
            form_data = {
                'contentBeginIndex': '0',
                'productBeginIndex': str(product_begin_index),
                'beginIndex': str(begin_index),
                'orderBy': '5',
                'isHistory': 'false',
                'pageView': 'grid',
                'resultType': 'products',
                'langId': '-1',
                'pageSize': '30',
                'requesttype': 'ajax'}
            yield FormRequest(url, formdata=form_data)

    def parse_item(self, response):
        item = KmartItem()
        item['name'] = self.get_name(response)
        item['image_urls'] = self.get_image_urls(response)
        item['description'] = self.get_description(response)
        item['price'] = self.get_price(response)
        item['skus'] = self.get_skus(response) or self.get_default_sku(item['price'])
        item['url'] = response.url
        return item

    def get_name(self, response):
        name_selector = '.h2[itemprop = "name"] ::text'
        return response.css(name_selector).extract_first()

    def get_image_urls(self, response):
        images_selector = '.multipleimages + input ::attr(value)'
        default_image_selector = '#productMainImage ::attr(src)'
        image_urls = response.css(images_selector).extract() or \
                     response.css(default_image_selector).extract()
        return [self.start_urls[0] + s for s in image_urls]

    def get_description(self, response):
        description_selector = '#product-details li ::text, #product-details p ::text'
        return response.css(description_selector).extract()

    def get_price(self, response):
        price_selector = '.price-wrapper [itemprop="price"] ::text'
        return response.css(price_selector).extract_first()

    def get_skus(self, response):
        skus_json_selector = '#catEntryParams ::attr(value)'
        json_wo_quotes = response.css(skus_json_selector).extract_first()

        skus_json = yaml.load(json_wo_quotes.replace("'", '"'))
        skus_data = skus_json['skus']
        price = self.get_price(response)

        skus = []
        for sku in skus_data:
            colour = sku['attributes'].get('Colour', 'N/A')
            size = sku['attributes'].get('Size', 'N/A')
            curr_sku = {
                "colour": colour,
                "currency": "AUD",
                "price": price,
                "sku_id": sku['id'],
                "size": size
            }
            skus.append(curr_sku)

        return skus

    def get_default_sku(self, default_price):
        return {
            "currency": "AUD",
            "price": default_price,
            "sku_id": 'N/A',
            "size": 'N/A'
        }
