# -*- coding: utf-8 -*-
from baby_walz.items import BabyWalzItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import re
import json
from urlparse import urljoin


def convert_into_absolute_url(value):
    if ('http:/' not in value):
        value = urljoin('http://www.baby-walz.de/', value)
    return value


class BabywalzspiderSpider(CrawlSpider):
    name = "babyWalzSpider"
    allowed_domains = ["baby-walz.de"]
    start_urls = [
        'http://www.baby-walz.de/'
    ]

    products_page_xpath = '(.//a[@class="urldetail"])[1]'
    pagination_xpath = '(.//a[@class="arrowHeadNextPage"])[1]'
    main_menu_items_xpath = '(.//*[@class="groupNavi"]//li//a)[1]'
    main_menu_sub_items_xpath = '(.//*[@id="naviLeft"]//li//a[@class="l1"])[1]'
    sub_menu_items_xpath = '(.//*[@class="l1 selected"]//li/a)[1]'
    rules = [

        Rule(LinkExtractor(restrict_xpaths=main_menu_items_xpath,
                           process_value=convert_into_absolute_url)),
        Rule(LinkExtractor(restrict_xpaths=main_menu_sub_items_xpath)),
        Rule(LinkExtractor(restrict_xpaths=products_page_xpath, process_value=convert_into_absolute_url),
             callback='get_product_detail'),
        Rule(LinkExtractor(restrict_xpaths=sub_menu_items_xpath, process_value=convert_into_absolute_url)),
        # Rule(LinkExtractor(restrict_xpaths=pagination_xpath))
    ]

    def get_skus(self, size):
        skus = {}
        for result in size:
            arr = {}
            arr['currency'] = 'Euro'
            arr['colour'] = result[0]
            arr['available'] = result[2]
            arr['size'] = result[1]
            arr['Price'] = result[3]
            skus[arr['size'] + u'_' + arr['colour']] = arr
        return skus

    def get_category(self, response):
        category = response.xpath('.//*[@id="groupnavigationBreadcrumb"]/a/text()').extract()
        return category

    def get_title(self, response):
        title = response.xpath('.//*[@class="prodName"]/text()').extract()
        return title

    def get_images(self, response):
        img_url = []
        for keys in response['media']:
            if ('.' in response['media'][keys]['name']) and ('/506/' not in response['media'][keys]['path']):
                img_url.append('http://walz-images.walz.de/fsicache/images?type=image&profile=560_baby&source=' +
                               response['media'][keys]['path'] + response['media'][keys]['fileName'])
        return img_url

    def get_description(self, response):
        description = response.xpath('.//*[@class="productCopytext"]//text()').extract()
        return description

    def get_price(self, response, jsonresponse):
        new_price = jsonresponse
        old_price = response.xpath(".//*[@id='productOldPrice_span']/text()").extract()
        if len(old_price) == 0:
            return new_price
        else:
            if (old_price[0] == u"0,00 €"):
                return new_price
            else:
                return {'new_price': new_price, 'old_price': (' ').join(old_price[0].split())}

    def get_product_detail(self, response):
        item = BabyWalzItem()
        jsonResponse = response.xpath(
            '//script[@type="text/javascript" and contains(.,"articles") and contains(.,"product")]/text() ').extract()
        match_result = re.findall("componentConf\[\w+\] = ({.*});", jsonResponse[0])
        jsondecode = json.loads(match_result[1])
        item['image_urls'] = self.get_images(jsondecode)
        available_colors = []
        skus = []
        for colors in jsondecode['product']['componentData']['1']:
            if (colors['relMediaPk']):
                available_colors.append([colors['relValue'], colors['relCode']])
        if not available_colors:
            available_colors.append(['', jsondecode['product']['productNumber']])
        for clr in available_colors:
            if re.search(r'\w+', clr[1]):
                clr[1] = jsondecode['product']['productNumber']
            sizedata = jsondecode['articles'][clr[1]]
            if isinstance(sizedata, list):
                for child in sizedata:
                    for allkeys in child['componentData']['1'].keys()[::-1]:
                        if re.match(r'[a-zA-Z]', child['componentData']['1'][allkeys]['relValue']):
                            clr[0] = child['componentData']['1'][allkeys]['relValue']
                    price = self.get_price(response, child['currentPrice'])
                    skus.append([clr[0], 'OneSize', child['selectable'], price])
            else:
                for size in sizedata:
                    if '/' in size:
                        key = sizedata[size]['componentData'].keys()[1]
                        comnentdata = sizedata[size]['componentData'][key]
                        if '/' in comnentdata[comnentdata.keys()[0]]['relValue']:
                            sizevalue = comnentdata[comnentdata.keys()[0]]['relValue']
                        else:
                            if '/' in comnentdata[comnentdata.keys()[1]]['relValue']:
                                sizevalue = comnentdata[comnentdata.keys()[1]]['relValue']
                            else:
                                sizevalue = comnentdata[comnentdata.keys()[2]]['relValue']

                        comnentdata = sizedata[size]['componentData']['1']
                        if re.match(r'\d+', comnentdata[comnentdata.keys()[3]]['relValue']):
                            clr[0] = comnentdata[comnentdata.keys()[0]]['relValue']
                        else:
                            clr[0] = comnentdata[comnentdata.keys()[1]]['relValue']
                        price = self.get_price(response, sizedata[size]['currentPrice'])
                        skus.append([clr[0], sizevalue, sizedata[size]['selectable'], price])
                    else:

                        price = self.get_price(response, sizedata[size]['currentPrice'])
                        if not clr[0]:
                            comnentdata = sizedata[size]['componentData']['1']
                            clr[0] = comnentdata[comnentdata.keys()[0]]['relValue']
                        skus.append([clr[0], size, sizedata[size]['selectable'], price])
        item['category'] = self.get_category(response)
        item['description'] = self.get_description(response)
        item['title'] = self.get_title(response)
        item['url'] = response.url
        item['spider_name'] = self.name
        item['skus'] = self.get_skus(skus)
        item['retailer'] = 'baby-walz'
        yield item
