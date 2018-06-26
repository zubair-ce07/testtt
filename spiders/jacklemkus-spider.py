import json
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst
from JacklemkusCrawler.items import ProductItem


def get_skus(response):
    json_str = response.css('div.product-data-mine::attr(data-lookup)')
    json_data = json.loads(json_str.extract_first().replace("'",'"'))
    currency = response.css('div.form-search script::text'). \
        re(r'.*currencycode:\'(...).*')[0]
    price = response.css('span.price::text').extract_first()
    return [{'sku_id': json_data[key]['id'], 'size': json_data[key]['size'],
             'currency': currency, 'price': price} for key in json_data]


def get_description(response):
    it = iter(response.xpath('//tbody/tr/child::*/child::text()').extract())
    return dict(zip(*[it] * 2))


def get_brand(res, desc):
    if 'Item Brand' in desc:
        return desc['Item Brand']
    else:
        return res.css('div.breadcrumbs li:nth-last-of-type(2) a::text').\
            extract()


def get_gender(desc):
    if 'Gender' in desc:
        return re.search(r'(\w{3,11})', desc['Gender']).group()
    else:
        return 'Unisex'


class JackLemkusSpider(CrawlSpider):
    name = 'JackLemkus-spider'
    start_urls = ['https://www.jacklemkus.com/sneakers/buy-vans-sneakers-online-jack-lemkus']

    rules = (
        # items list
        Rule(LinkExtractor(restrict_css='ol.products-grid>li'),
             callback='parse_item'),
        # menu links main page with sub menus
        Rule(LinkExtractor(restrict_css='li.level0.parent li.level1:not(.first)'
                                        ' > a.menu-link')),
        # menu link main page without submenus
        Rule(LinkExtractor(restrict_css='li.level0:not(.parent):not(.last)'
                                        ' > a.menu-link')),
        # next page items
        Rule(LinkExtractor(restrict_css='a.next')),
    )

    def parse_item(self, response):
        skus = get_skus(response)
        desc = get_description(response)
        l = ItemLoader(item=ProductItem(), response=response)
        l.default_output_processor = TakeFirst()
        l.add_css('name', 'div.product-name > h1::text')
        l.add_value('brand', get_brand(response, desc))
        l.add_css('category', 'ul.clearfix > li[class^="category"] > a::text')
        l.add_value('gender', get_gender(desc))
        l.add_value('description', desc)
        l.add_value('skus', skus)
        l.add_css('image_urls', 'p.product-image img::attr(src)')
        l.add_css('retailer_sku', 'span.sku::text')
        l.add_value('market', 'ZA')
        l.add_css('url','link[rel="canonical"]::attr(href)')
        l.add_value('url_original', response.url)
        yield l.load_item()

