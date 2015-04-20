# -*- coding: utf-8 -*-
import re
import urlparse
import urllib

from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from newegg.items import NeweggItem


class NeweggspiderSpider(CrawlSpider):
    name = "NewEggSpider"
    allowed_domains = ["newegg.com"]
    start_urls = (
        'http://www.newegg.com/',
    )

    rules = [Rule(SgmlLinkExtractor(restrict_xpaths=['.//*[@id="itmBrowseNav"]//*[@class="nav-row"]//a','.//*[@class="categoryList primaryNav"]//a'])
                  , callback='parse_pagination', follow=True),
             Rule(SgmlLinkExtractor(restrict_xpaths=['.//*[@title="View Details"]']),
                  callback='parse_item')
            ]

    def parse_item(self, response):
        item = NeweggItem()
        item['sku'] = self.get_sku(response)
        item['title'] = self.get_title(response)
        item['url'] = self.get_url(response)
        json_data = self.get_json_data(response)
        item['brand'] = json_data['brand']
        if response.xpath('.//*[@class="priceAction"]'):
            return Request('http://www.newegg.com/Product/MappingPrice2012.aspx?%s' % item['url'].split('?', 1)[1],
                           callback=self.parse_price, meta={'item': item})
        item['price'] = json_data['price']
        return item

    def get_url(self, response):
        return response.url.split('&', 1)[0]

    def get_sku(self, response):
        query_string = urlparse.urlparse(response.url).query
        if query_string:
            sku = urlparse.parse_qs(query_string)['Item'][0]
            return sku

    def get_title(self, response):
        title = response.xpath(".//*[@itemprop='name'][1]//text()").extract()
        if title:
            return self.normalize(title[0])

    def parse_price(self, response):
        item = response.meta['item']
        price = response.xpath('.//*[contains(@class,"price-current")]//text()').extract()
        item['price'] = ('').join(self.normalize(price)).strip('-')
        return item

    def get_json_data(self, response):
        json_string = response.xpath('//script[contains(text(), "ProductDetail")]//text()').extract()[0]
        json_string = self.normalize(json_string)
        price = re.search("product_sale_price:\['([^']+)'\]", json_string).group(1)
        brand = re.search("product_manufacture:\['([^']+)'\]", json_string).group(1)
        data = dict()
        data['price'] = '$' + price
        data['brand'] = brand
        return data

    def parse_pagination(self, response):
        if response.xpath('.//*[@title="last page"]/parent::li[@class="enabled"]'):
            last_page = response.xpath('.//*[@title="last page"]/@href').extract()
            if last_page:
                last_page_url = urllib.unquote(last_page[0].split(",'", 1)[1].split("',")[0])
                request_url, last_page_number = last_page_url.split('Page-', 1)
                for i in range(2, int(last_page_number) + 1):
                    yield Request('%sPage-%s' % (request_url, i))

    def normalize(self, data):
        if type(data) is str or type(data) is unicode:
            return self.clean(data)
        elif type(data) is list:
            lines = [self.clean(x) for x in data]
            return [line for line in lines if line]
        else:
            return data

    def clean(data):
        return data.replace("\n", "")\
                .replace("\r", "")\
                .replace("\t", "").strip()
