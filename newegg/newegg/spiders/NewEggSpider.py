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

    rules = [Rule(SgmlLinkExtractor(deny=['name=Newegg-Mobile-Apps', 'Trade-In', 'Power-Supply-Wattage-Calculator', 'Finder/'],
                                    restrict_xpaths=['.//*[@id="itmBrowseNav"]//*[@class="nav-row"]//a',
                                                     './/*[@class="categoryList primaryNav"]//a',
                                                     './/*[@class="categoryList secondaryNav"]//a'])
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
        item['price'] = json_data['price']
        if response.xpath('.//*[@class="priceAction"]') or 'MAP' in item['price']:
            return Request('http://www.newegg.com/Product/MappingPrice2012.aspx?%s' % item['url'].split('?', 1)[1],
                           callback=self.parse_price, meta={'item': item})
        if 'Combo' in item['sku'] and item['price'] == '$':
            return Request('http://www.newegg.com/Product/MappingPrice2012.aspx?ComboID=%s' % item['sku'],
                           callback=self.parse_price, meta={'item': item})
        return item

    def item_url(self, response):
        return response.url

    def item_sku(self, response):
        query_string = urlparse.urlparse(response.url).query
        if query_string:
            if 'ItemList' in query_string:
                sku = urlparse.parse_qs(query_string).get('ItemList')
                if sku:
                    return sku[0]
            elif 'Item' in query_string:
                sku = urlparse.parse_qs(query_string).get('Item')
                if sku:
                    return sku[0]
            else:
                return None

    def item_title(self, response):
        title = response.xpath(".//*[@itemprop='name'][1]//text()").extract()
        if title:
            return ' '.join(self.normalize(title[0]).split())

    def parse_price(self, response):
        item = response.meta['item']
        price = response.xpath('.//*[contains(@class,"price-current")]//text()').extract()
        item['price'] = ('').join(self.normalize(price)).strip(u'\u2013')
        return item

    def item_json_data(self, response):
        data = dict()
        json_string = response.xpath('//script[contains(text(), "ProductDetail")]//text()').extract()
        if json_string:
            json_string = self.normalize(json_string[0])
            price = re.search("product_sale_price:\['([^']+)'\]", json_string).group(1)
            brand = re.search("product_manufacture:\['([^']+)'\]", json_string).group(1)
            data['price'] = '$%s' % price
            data['brand'] = brand
            return data
        else:
            price = self.get_text_from_node(response.xpath('.//*[@id="singleFinalPrice"]/@content'))
            data['price'] = '$%s' % price
            data['brand'] = None
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
        elif (response.xpath('.//span[@class="pageNum"]')):
            for url in response.xpath('.//span[@class="pageNum"]/a/@href').extract():
                request_url = urllib.unquote(url.split(",'", 1)[1].split("',")[0])
                if 'newegg' not in request_url:
                    request_page_number = url.split("',", 1)[1].split(",'")[0]
                    request_url = '%s&Page=%s' % (response.url, request_page_number)
                yield Request(request_url)

