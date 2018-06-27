import json
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst
from JacklemkusCrawler.items import ProductItem


class JackLemkusSpider(CrawlSpider):
    name = 'JackLemkus-spider'
    start_urls = ['https://www.jacklemkus.com/']

    rules = (
        Rule(LinkExtractor(restrict_css='h5.product-name'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_css=[
            'li.level0.parent li.level1:not(.first)',
            'li.level0:not(.parent):not(.last)', 'a.next'
            ])),
    )

    def parse_item(self, response):
        skus = self.get_skus(response)
        desc = self.get_description(response)
        l = ItemLoader(item=ProductItem(), response=response)
        l.default_output_processor = TakeFirst()
        l.add_css('name', 'div.product-name > h1::text')
        l.add_value('brand', self.get_brand(response, desc))
        l.add_css('category', 'ul.clearfix > li[class^="category"] > a::text')
        l.add_value('gender', self.get_gender(desc))
        l.add_value('description', desc)
        l.add_value('skus', skus)
        l.add_css('image_urls', 'p.product-image img::attr(src)')
        l.add_css('retailer_sku', 'span.sku::text')
        l.add_value('market', 'ZA')
        l.add_css('url', 'link[rel="canonical"]::attr(href)')
        l.add_value('url_original', response.url)
        yield l.load_item()

    def get_skus(self, response):
        json_str = response.css('div.product-data-mine::attr(data-lookup)')
        json_obj = json.loads(json_str.extract_first().replace("'", '"'))
        currency = response.css('div.form-search script::text'). \
            re(r'.*currencycode:\'(...).*')[0]
        price = response.css('span.price::text').extract_first()
        return [{'sku_id': json_obj[key]['id'], 'size': json_obj[key]['size'],
                 'currency': currency, 'price': price} for key in json_obj]

    def get_description(self, response):
        it = response.xpath('//tbody/tr/child::*/child::text()').extract()
        return dict(zip(*[iter(it)] * 2))

    def get_brand(self, res, desc):
        if 'Item Brand' in desc:
            return desc['Item Brand']
        return res.css('div.breadcrumbs li:nth-last-child(2) a::text')\
            .extract()

    def get_gender(self, desc):
        if 'Gender' in desc:
            return re.search(r'(\w{3,11})', desc['Gender']).group()
        return 'Unisex'

