# -*- coding: utf-8 -*-
import re
import urlparse
import urllib

from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapinghub.spider import BaseSpider
from scrapy import log
from newegg.items import NeweggItem


class NeweggspiderSpider(BaseSpider):
    name = "NewEggSpider"
    allowed_domains = ["newegg.com"]
    start_urls = (
        'http://www.newegg.com/',
    )

    rules = [Rule(SgmlLinkExtractor(deny = ['name=Newegg-Mobile-Apps'], restrict_xpaths=['.//*[@id="itmBrowseNav"]//*[@class="nav-row"]//a','.//*[@class="categoryList primaryNav"]//a'])
                  , callback='parse_pagination', follow=True),
             Rule(SgmlLinkExtractor(restrict_xpaths=['.//*[@title="View Details"]']),
                  callback='parse_item')
            ]

    def parse_item(self, response):
        item = NeweggItem()
        item['sku'] = self.item_sku(response)
        item['title'] = self.item_title(response)
        item['url'] = self.item_url(response)
        json_data = self.item_json_data(response)
        item['brand'] = json_data['brand']
        if response.xpath('.//*[@class="priceAction"]'):
            return Request('http://www.newegg.com/Product/MappingPrice2012.aspx?%s' % item['url'].split('?', 1)[1],
                           callback=self.parse_price, meta={'item': item})
        item['price'] = json_data['price']
        return item

    def item_url(self, response):
        return response.url

    def item_sku(self, response):
        query_string = urlparse.urlparse(response.url).query
        if query_string:
            if 'Item' in query_string:
                sku = urlparse.parse_qs(query_string)['Item'][0]
                return sku
            else:
                return None

    def item_title(self, response):
        title = response.xpath(".//*[@itemprop='name'][1]//text()").extract()
        if title:
            return ' '.join(self.normalize(title[0]).split())

    def parse_price(self, response):
        item = response.meta['item']
        price = response.xpath('.//*[contains(@class,"price-current")]//text()').extract()
        item['price'] = ('').join(self.normalize(price)).strip('-')
        return item

    def item_json_data(self, response):
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
                self.log('url of last page: %s' % last_page_url, log.INFO)
                if 'newegg' not in last_page_url:
                    last_page_number = last_page[0].split("',", 1)[1].split(",'")[0]
                    for i in range(2, int(last_page_number) + 1):
                        yield Request('%s&Page=%s' % (response.url, last_page_number))
                else:
                    request_url, last_page_number = last_page_url.split('Page-', 1)
                    if '?' in last_page_number:
                        last_page_number = last_page_number.split('?')[0]
                    for i in range(2, int(last_page_number) + 1):
                        yield Request('%sPage-%s' % (request_url, i))
        elif(response.xpath('.//span[@class="pageNum"]')):
                for url in response.xpath('.//span[@class="pageNum"]/a/@href').extract():
                    request_url = urllib.unquote(url.split(",'", 1)[1].split("',")[0])
                    yield Request(request_url)

