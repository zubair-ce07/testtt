import json
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from kith_scraper.items import KithProductItem


class KithSpider(CrawlSpider):
    name = "kith"
    allowed_domains = ["kith.com"]
    start_urls = ["https://kith.com"]
    color_regex = re.compile(r"-.*?-")
    meta_var_regex = re.compile(r"var meta = ({.*?});", re.MULTILINE | re.DOTALL)

    rules = (
        Rule(LinkExtractor(restrict_css=['#MainNav a, span.next a'])),
        Rule(LinkExtractor(restrict_css=['.product-card-info']), callback="parse_item"),
    )

    def parse_item(self, response):
        item = KithProductItem()
        item['brand'] = self.parse_brand(response)
        item['name'] = self.parse_name(response)
        item['image_urls'] = self.parse_image_urls(response)
        item['description'] = self.parse_description(response)
        item['retailer'] = 'Kith-US'
        product_info = self.get_product_info(response)
        item['retailer_sku'] = self.parse_retailer_sku(product_info)
        item['skus'] = self.parse_skus(product_info)
        item['url'] = response.url
        return item

    def parse_brand(self, response):
        return (response.css('[itemprop=name] span:first-child ::text').extract())[0]

    def parse_name(self, response):
        return (response.css('[itemprop=name] span:last-child ::text').extract())[0]

    def parse_image_urls(self, response):
        return response.css('.js-super-slider-photo-img.super-slider-photo-img::attr(src)').extract()

    def parse_description(self, response):
        css_selector = '.rte ::text'
        return self.clean_object(response.css(css_selector).extract())

    def parse_retailer_sku(self, product_info):
        return product_info['id']

    def parse_skus(self, product_info):
        unformatted_skus = product_info['variants']
        formated_skus = {}
        for sku in unformatted_skus:
            key = sku['sku']
            name = sku['name']
            color_occurrences = self.color_regex.findall(name)
            color = ((color_occurrences[0])[1:-1]).strip()
            new_sku = {'colour': color,
                       'currency': 'USD',
                       'price': sku['price'],
                       'size': sku['public_title']}
            formated_skus[key] = new_sku
        return formated_skus

    def get_product_info(self, response):
        skus_info_var = response.xpath('//script[contains(text(),\'var meta\')]').re(self.meta_var_regex)
        skus_info_var = json.loads(skus_info_var[0].encode('utf-8'))
        return skus_info_var['product']

    def clean_object(self, object):
        clean_obj = [x.strip('\t\n ') for x in object]
        return [x for x in clean_obj if x]
