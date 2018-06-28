import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst
from JacklemkusCrawler.items import ProductItem


class JackLemkusSpider(CrawlSpider):
    name = 'JackLemkus-spider'
    start_urls = ['https://www.jacklemkus.com/']

    rules = (
        Rule(LinkExtractor(restrict_css='h5.product-name', allow=".com/\w+/"),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_css=[
            'li.level1:not(.first)', 'li.level0:not(.parent):not(.last)',
            'a.next'
            ]), callback='parse'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=ProductItem(), response=response)
        l.default_output_processor = TakeFirst()
        l.add_css('name', 'div.product-name > h1::text')
        l.add_xpath('description', '//th/text()|//td/text()')
        l.add_value('brand', self.product_brand(response))
        l.add_css('category', 'li[class^="category"] > a::text')
        l.add_value('gender', self.product_gender(response))
        l.add_value('skus', self.skus(response))
        l.add_css('image_urls', 'p.product-image ::attr(src)')
        l.add_css('retailer_sku', 'span.sku::text')
        l.add_value('market', 'ZA')
        l.add_css('url', 'link[rel="canonical"]::attr(href)')
        l.add_value('url_original', response.url)
        yield l.load_item()

    def skus(self, response):
        json_str = response.css('div.product-data-mine::attr(data-lookup)')
        json_obj = json.loads(json_str.extract_first().replace("'", '"'))
        currency = response.css('div.form-search script::text'). \
            re_first(r'.*currencycode:\'(...).*')
        price = response.css('span.price::text').extract_first()
        return [{'sku_id': json_obj[key]['id'], 'size': json_obj[key]['size'],
                 'currency': currency, 'price': price} for key in json_obj]

    def product_brand(self, r):
        return r.css('tr').re_first('Item Brand.*\n.*>(.*)<') \
            or r.css('div.breadcrumbs li:nth-last-child(2) a::text').extract()

    def product_gender(self, r):
        return r.css('tr').re_first('Gender.*\n.*>(\w{3,11}).*<') or 'Unisex'

