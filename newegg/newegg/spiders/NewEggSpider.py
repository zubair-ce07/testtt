# -*- coding: utf-8 -*-
import re
import urlparse
import urllib

from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy import log

from scrapinghub.spider import BaseSpider
from newegg.items import NeweggItem


class NeweggspiderSpider(BaseSpider):
    name = "NewEggSpider"
    # allowed_domains = ["newegg.com"]
    start_urls = (
        'http://www.newegg.com/',
    )

    rules = [Rule(SgmlLinkExtractor(
        deny=['name=Newegg-Mobile-Apps', 'Trade-In', 'Memory-Finder', 'Power-Supply-Wattage-Calculator',
              'Battery-Finder', 'Cable-Finder', 'Notebook-Finder', 'Tablet-Finder', 'Windows-Device-Finder',
              'HDTV-Finder'],
        restrict_xpaths=['.//h3[@class="aec-dcsnavHead" and contains(.,"Explore")]/following-sibling::div[@class="aec-dcsLinks aec-dcsLinksOpen"][1]//a',
                         './/*[@id="itmBrowseNav"]//*[@class="nav-row"]//a',
                         './/*[@class="categoryList primaryNav"]//a',
                         './/*[@class="categoryList secondaryNav"]//a'
        ]

    )
                  , callback='parse_pagination', follow=True),
             Rule(SgmlLinkExtractor(deny=['ShellShocker'],
                                    restrict_xpaths=['.//*[@title="View Details"]', './/*[@class="aec-listlink"]']),
                  callback='parse_item')
    ]

    def parse_item(self, response):
        if not response.xpath('.//*[@class="errorMsgWarning"]'):
            item = NeweggItem()
            item['sku'] = self.item_sku(response)
            item['title'] = self.item_title(response)
            item['url'] = self.item_url(response)
            json_data = self.item_json_data(response)
            item['brand'] = json_data['brand'] if json_data['brand'] else self.item_brand(response)
            item['price'] = json_data['price'] if json_data['price'] else self.item_price(response)
            if response.xpath('.//*[@class="priceAction"]') or 'MAP' in item['price'] or '$0.00' in item['price']:
                return Request('http://www.newegg.com/Product/MappingPrice2012.aspx?%s' % item['url'].split('?', 1)[1],
                               callback=self.parse_price, meta={'item': item})
            if item.get('sku') and 'Combo' in item.get('sku') and not item.get('price'):
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
        else:
            return self.get_text_from_node(response.xpath(".//li[span[contains(.,'UPC')]]/text()"))

    def item_title(self, response):
        title = response.xpath(".//*[@itemprop='name'][1]//text() | .//*[@id='aec-product-title']//h1/text()").extract()
        if title:
            return ' '.join(self.normalize(title[0]).split())

    def item_brand(self, response):
        return self.get_text_from_node(response.xpath(".//li[span[contains(.,'Label')]]/text()"))

    def item_price(self, response):
        price = self.get_text_from_node(response.xpath('(.//*[@class="aec-nowprice"])[1]/text()'))
        return price if price else self.get_text_from_node(
            response.xpath('(.//*[@class="aec-webamiprice-href"])[1]/text()'))

    def parse_price(self, response):
        item = response.meta['item']
        price = response.xpath(
            './/*[contains(@class,"price-current")]//text() | (.//*[@class="aec-nowprice"])[1]/text()').extract()
        item['price'] = ('').join(self.normalize(price)).strip(u'\u2013')
        return item

    def item_json_data(self, response):
        data = dict()
        json_string = response.xpath('//script[contains(text(), "ProductDetail")]//text()').extract()
        if json_string:
            json_string = self.normalize(json_string[0])
            price = re.search("product_sale_price:\['([^']+)'\]", json_string).group(1)
            brand = re.search("product_manufacture:\['([^']+)'\]", json_string).group(1)
            data['price'] = '$%s' % price if price else None
            data['brand'] = brand
            return data
        else:
            price = self.get_text_from_node(response.xpath('.//*[@id="singleFinalPrice"]/@content'))
            data['price'] = '$%s' % price if price else None
            data['brand'] = None
            return data

    def get_page_url(self, data):
        page_url = re.search(",'([^']+)", data).group(1)
        return page_url

    def get_page_number(self, data):
        page_number = re.search("',(\d+),", data).group(1)
        return page_number

    def parse_pagination(self, response):
        if response.xpath('.//*[@id="aec-totalresults"]'):
            total_results = self.get_text_from_node(
                response.xpath('.//*[@id="aec-totalresults"]/@value')) if response.xpath(
                './/*[@id="aec-totalresults"]') else 0
            if response.xpath('.//*[@id="aec-perpage"]'):
                items_per_page = self.get_text_from_node(
                    response.xpath('.//*[@id="aec-perpage"]/option[.="100"]/text()'))
            else:
                items_per_page = 25
            total_pages = int(total_results) / int(items_per_page) + (int(total_results) % int(items_per_page) != 0)
            for page_number in range(2, total_pages):
                parsed_url = urlparse.urlparse(response.url)
                yield Request(
                    url='http://newegg.directtoustore.com/catalog/getgrid?%s&type=productsearch&sortCol=BestMatch&pageNum=%s&perPage=%s' % (
                        parsed_url.query, page_number, items_per_page))

        if response.xpath('.//*[@title="last page"]/parent::li[@class="enabled"]'):
            last_page = response.xpath('.//*[@title="last page"]/@href').extract()
            if last_page:
                last_page_url = urllib.unquote(self.get_page_url(last_page[0]))
                self.log('url of last page: %s' % last_page_url, log.INFO)
                if 'newegg' not in last_page_url:
                    last_page_number = self.get_page_number(last_page[0])
                    for i in range(2, int(last_page_number) + 1):
                        yield Request('%s&Page=%s' % (response.url, i))
                else:
                    request_url, last_page_number = last_page_url.split('Page-', 1)
                    if '?' in last_page_number:
                        last_page_number = last_page_number.split('?')[0]
                    for i in range(2, int(last_page_number) + 1):
                        yield Request('%sPage-%s' % (request_url, i))
        elif (response.xpath('.//span[@class="pageNum"]')):
            for url in response.xpath('.//span[@class="pageNum"]/a/@href').extract():
                extracted_url = self.get_page_url(url)
                request_url = urllib.unquote(extracted_url)
                if 'newegg' not in request_url:
                    request_page_number = self.get_page_number(url)
                    request_url = '%s&Page=%s' % (response.url, request_page_number)
                yield Request(request_url)

