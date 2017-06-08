import json
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from kith_scraper.items import KithProductItem


class KithSpider(CrawlSpider):
    name = "kith"
    allowed_domains = ["kith.com"]
    start_urls = ["https://kith.com"]

    rules = (
        Rule(LinkExtractor(restrict_css=['#MainNav'])),
        Rule(LinkExtractor(restrict_css=['.product-card-info']), callback="parse_item"),
    )

    def __init__(self, *a, **kw):
        super(KithSpider, self).__init__(*a, **kw)
        self.color_regex = re.compile(r"-.*?-")
        self.meta_var_regex = re.compile(r"var meta = ({.*?});", re.MULTILINE | re.DOTALL)

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
        return (response.css('h1.product-header-title > span:nth-child(1)::text').extract())[0]

    def parse_name(self, response):
        return (response.css('h1.product-header-title > span:last-child::text').extract())[0]

    def parse_image_urls(self, response):
        return response.css('.js-super-slider-photo-img.super-slider-photo-img::attr(src)').extract()

    def parse_description(self, response):
        css_selector = '.product-single-details-rte.rte.mb0 p::text, .product-single-details-rte.rte.mb0 li::text'
        return response.css(css_selector).extract()

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
        meta = response.xpath('//script/text()').re(self.meta_var_regex)
        meta = json.loads(meta[0].encode('utf-8'))
        return meta['product']
