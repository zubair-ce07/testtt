import json
import re

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from kith_scraper.items import KithProductItem


class MySpider(CrawlSpider):
    name = "kith"
    allowed_domains = ["kith.com"]
    start_urls = ["https://kith.com",
                  "https://kith.com/pages/women",
                  "https://kith.com/pages/kids"
                  ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=['#MainNav']), follow=True),
        Rule(LinkExtractor(allow=(), restrict_css=['.product-card-info']), callback="parse_items", follow=True),
    )

    def parse_items(self, response):
        item = KithProductItem()
        item['brand'] = (response.css('h1.product-header-title > span:nth-child(1)::text').extract())[0]
        item['name'] = (response.css('h1.product-header-title > span:last-child::text').extract())[0]
        item['image_urls'] = response.css('.js-super-slider-photo-img.super-slider-photo-img::attr(src)').extract()
        item['description'] = response.css('.product-single-details-rte.rte.mb0 p::text, .product-single-details-rte.rte.mb0 li::text').extract()
        item['retailer'] = 'Kith-US'
        retailer_sku, formated_skus = self.parse_meta(response)
        item['retailer_sku'] = retailer_sku
        item['skus'] = formated_skus
        item['url'] = response.url
        return item

    def parse_meta(self, response):
        meta_pattern = re.compile(r"var meta = ({.*?});", re.MULTILINE | re.DOTALL)
        meta = response.xpath('//script/text()').re(meta_pattern)
        meta = json.loads(meta[0].encode('utf-8'))
        product_info = meta['product']
        retailer_sku = product_info['id']
        unformated_skus = product_info['variants']
        formated_skus = {}
        for sku in unformated_skus:
            key = self.unicode_to_utf8(sku['sku'])
            name = self.unicode_to_utf8(sku['name'])
            color_occurrences = re.findall(r"-.*?-", name)
            color = ((color_occurrences[0])[1:-1]).strip()
            new_sku = {'colour': color,
                       'currency': 'USD',
                       'price': sku['price'],
                       'size': self.unicode_to_utf8(sku['public_title'])}
            formated_skus[key] = new_sku
        return retailer_sku, formated_skus

    def unicode_to_utf8(self, unicode_input):
        return unicode_input.encode('utf-8')

