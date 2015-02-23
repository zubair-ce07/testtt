# -*- coding: utf-8 -*-
from ernstings.items import ErnstingsItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import re
import json
from urlparse import urljoin
from urlparse import urlparse
from scrapy.http.request import Request


def convert_into_absolute_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return urljoin('http://www.ernstings-family.de/', url)
    return url


class ErnstringspiderSpider(CrawlSpider):
    name = "ErnstringSpider"
    allowed_domains = ["ernstings-family.de"]
    start_urls = (
        'http://www.ernstings-family.de/',
    )
    main_menu_xpath = './/*[@id="navi_main"]/li/a'  # xpath for  main menus
    sub_menu_xpath = ".//li[contains(@id,'catListEntry')]/a"  # xpath for  sub menus
    products_page_xpath = '//a[@class="product_title"]'  # xpath for product
    rules = [

        Rule(LinkExtractor(deny=[u'/prospekt/das', u'/prospekt/', u'reisen'], restrict_xpaths=main_menu_xpath), callback='get_pagination', follow=True),
        Rule(LinkExtractor(deny=[u'/prospekt/das', u'/prospekt/', u'reisen', u'/service/', u'spielen-lernen'],
                           restrict_xpaths=sub_menu_xpath), callback='get_pagination', follow=True),
        Rule(LinkExtractor(restrict_xpaths=products_page_xpath, process_value=convert_into_absolute_url),
             callback='get_product_detail')
    ]

    def get_product_detail(self, response):
        item = ErnstingsItem()
        item['retailer'] = 'ernstings-de'
        item['spider_name'] = self.name
        item['category'] = self.get_category(response)
        item['url'] = response.url
        item['care'] = self.get_care(response)
        item['title'] = self.get_title(response)
        item['description'] = self.get_description(response)
        item['image_urls'] = self.get_images(response)
        item['retailer_sk'] = self.get_retailer_sk(response)
        item['brand'] = self.get_brand(response)
        item['industry'] = 'homewares' if 'My Home' in item['category'] and 'Disney & Co.' not in item[
            'category'] else None
        item['gender'] = 'Herren' if 'Herren' in item['category'] else 'Damen' if 'Damen' in item['category'] else None
        item['skus'] = self.get_skus(response)
        yield item

    def get_pagination(self, response):
        pagination_url = self.get_pagination_url(response)
        total_pages = self.get_pages_count(response)
        for i in range(2, int(total_pages) + 1):
            request_url = pagination_url + '&page=%i' % i
            yield Request(url=request_url)

    def get_category(self, response):
        categories = self.normalize(response.xpath(".//*[@id='navi_crumb']/li//a//text()").extract())
        return categories

    def get_brand(self, response):
        brand = self.get_text_from_node(response.xpath('.//*[@class="oosText"]//text()'))
        return brand

    def get_retailer_sk(self, response):
        retailer_sk = ''
        raw_retailer_sk = self.get_text_from_node(response.xpath('.//*[contains(@id,"prd_av_")]/@id'))
        if ('prd_av_' in raw_retailer_sk):
            matchResult = re.search("prd_av_(\d+)", raw_retailer_sk)
            retailer_sk = matchResult.group(1)
        return retailer_sk

    def get_pages_count(self, response):
        pagecount = response.xpath('//*[@class="category_product_list"]/@data-max-page').extract()
        return pagecount[0] if pagecount else '0'

    def get_pagination_url(self, response):
        scriptdata = response.xpath('//script[contains(.,"endlessScrollingUrl")]/text()').extract()
        if scriptdata:
            matchResult = re.search("'endlessScrollingUrl': '(.*)',", scriptdata[0])
            url = matchResult.group(1)
            return urljoin('http://www.ernstings-family.de/', url)

    def get_color(self, response):
        color = self.get_text_from_node(response.xpath('.//*[@class="prd_color"]/text()'))
        return color

    def get_description(self, response):
        description = self.normalize(response.xpath('.//p[@class="infotext"]//text()') \
                                     .extract())
        return description

    def get_title(self, response):
        title = self.get_text_from_node(response.xpath('.//*[@class="prd_name"]/text()'))
        return title.strip()

    def get_care(self, response):
        care = self.normalize(response.xpath('.//*[@class="care_instructions"]//li//img//@title') \
                              .extract())
        return care

    def get_images(self, response):
        images = response.xpath('.//*[@id="prd_thumbs"]/a/@data-zoom-image').extract()
        return images

    def get_text_from_node(self, node):
        text_array = node.extract()
        if text_array:
            return self.normalize(text_array[0])
        else:
            return ''

    def get_price(self, response):
        old_price = self.get_text_from_node(response.xpath(".//*[@id='prd_oldprice']//text()"))
        scriptdata = response.xpath('.//script[contains(.,"function init()")]/text()').extract()[0]
        price = ''
        if ('setDefaultPrice' in scriptdata):
            matchResult = re.search("varObj\.setDefaultPrice\('(.*)'", scriptdata)
            price = self.normalize(matchResult.group(1)).replace(u'&', u'').replace(u';', u'')
            if old_price:
                return {'new_price': price,
                        'old_price': old_price}
        return price

    def get_skus(self, response):
        skus = {}
        scriptdata = response.xpath('.//script[contains(.,"function init()")]/text()').extract()[0]
        if ('setVariations' in scriptdata):
            matchResult = re.search("setVariations\(Json\.evaluate\('(.*)'", scriptdata)
            jsonRespnse = json.loads(matchResult.group(1))
            sizes = jsonRespnse["dependencies"][u"Größe"]
            for size, value in sizes.items():
                for color, code in value['Farbe'].items():
                    arr = {}
                    arr['currency'] = 'Euro'
                    arr['colour'] = color
                    arr['size'] = size
                    arr['Price'] = self.get_price(response)
                    skus[sizes[size]["Farbe"][color]] = arr
        return skus

    def normalize(self, data):
        if type(data) is str or type(data) is unicode:
            return self.clean(data)
        elif type(data) is list:
            lines = [self.clean(x) for x in data]
            return [line for line in lines if line]
        else:
            return data

    def clean(self, data):
        data = data.replace(u'&amp;', u'&').replace(u'&nbsp;', u' ')
        return data.replace(u'\u00e2\u20ac\u2122', u"'").replace(u'\u00e2\u20ac\u0153', u'"').replace(
            u'\u00e2\u20ac\ufffd', u'"').replace(u'\u2013', u"-").replace(u'\u00a0', u' ') \
            .replace(u'\u2012', u"-").replace(u'\u2018', u"'").replace(u'\u2019', u"'").replace(u'\u201c', u'"') \
            .replace(u'\u201d', u'"').replace(u'\xd0', u'-').strip()
