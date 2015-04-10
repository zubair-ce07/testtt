# -*- coding: utf-8 -*-
import re
from urlparse import urljoin, urlparse
import json

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import FormRequest, Request

from hhgregg.items import HhgreggItem


class HhgreggspiderSpider(CrawlSpider):
    name = "hhgreggSpider"
    allowed_domains = ["hhgregg.com",
                       "scene7.com"]
    start_urls = (
        'http://www.hhgregg.com/',
    )

    rules = [

        Rule(LinkExtractor(deny=['/productfinder/'],
                           restrict_xpaths=['.//*[contains( @id,"WC_CachedHeaderDisplay_links")]',
                                            './/*[@class="product_group_name product_info"]']),
             callback='parse_pagination', follow=True),
        Rule(LinkExtractor(restrict_xpaths=['.//*[@class="information"]/h3/a']),
             callback='get_product_detail')
    ]

    def get_product_detail(self, response):
        if response.xpath('.//*[@class="kitItemList"]'):
            return self.parse_packages(response)
        else:
            item = HhgreggItem()
            item['description'] = self.item_description(response)
            item['title'] = self.item_title(response)
            item['brand'] = self.item_brand(response)
            item['product_id'] = self.item_product_id(response)
            item['sku'] = self.item_sku(item['product_id'])
            item['model'] = self.item_model(response)
            item['rating'] = self.item_rating(response)
            item['mpn'] = self.item_mpn(response)
            item['upc'] = self.item_upc(response)
            item['trail'] = self.item_trail(response)
            item['features'] = self.item_features(response)
            item['specifications'] = self.item_specification(response)
            item['price'] = self.item_price(response)
            item['currency'] = self.item_currency(
                self.get_text_from_node(response.xpath('.//*[@class="price spacing"]/text()')))
            item['source_url'] = response.url
            item['primary_image_url'] = self.item_primary_image_url(response)
            return Request(
                url='http://hhgregg.scene7.com/is/image//hhgregg/%s?req=set,json,UTF-8' % self.item_sku(
                    item['product_id']),
                callback=self.item_images, meta={'item': item})

    def parse_packages(self, response):
        item = HhgreggItem()
        item['description'] = self.item_description(response, True)
        item['title'] = self.item_title(response)
        item['brand'] = self.item_brand(response)
        item['product_id'] = self.item_product_id(response)
        item['sku'] = self.item_sku(item['product_id'])
        item['model'] = self.item_model(response)
        item['source_url'] = response.url
        products = []
        for product_info_div in response.xpath(
                './/*[@id="mainBundleTabContainer"]//*[contains(@class,"kitTarget target")]'):
            product = dict()
            product['title'] = self.item_title(product_info_div, True)
            product['model'] = self.item_model(product_info_div)
            product['primary_image_url'] = self.item_primary_image_url(product_info_div, True)
            product['product_id'] = self.item_product_id(product['primary_image_url'], True)
            product['specifications'] = self.item_specification(product_info_div, True)
            product['sku'] = self.item_sku(product['product_id'])
            product['mpn'] = self.item_mpn(product_info_div, True)
            product['upc'] = self.item_upc(product_info_div, True)
            product['features'] = self.item_features(product_info_div, True)
            product['price'] = self.item_price(product_info_div, True)
            product['currency'] = self.item_currency(
                self.get_text_from_node(response.xpath('(.//*[@class="price spacing"]/text())[1]')))
            products.append(product)
        item['products'] = products
        return Request(
            url='http://hhgregg.scene7.com/is/image//hhgregg/%s?req=set,json,UTF-8' % self.item_sku(item['product_id']),
            callback=self.item_images, meta={'item': item})

    def item_title(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(response.xpath('.//*[@class="bundles_kits_prod_details"]/h1/text()'))
        return self.get_text_from_node(response.xpath(".//*[@id='prod_detail_main']/h1/text()"))

    def item_description(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(response.xpath('//meta[@name="description"]/@content'))
        return self.get_text_from_node(response.xpath('//meta[@property="og:description"]/@content'))

    def item_sku(self, product_id):
        return product_id + '_is'

    def item_product_id(self, response, package_flag=False):
        if package_flag:
            product_id = re.search("hhgregg\/([^_]+)_", response).group(1)
        else:
            script_text = response.xpath(".//script[contains(.,'entity.id')]").extract()
            product_id = re.search("'entity.id=(.*)'", script_text[0]).group(1)
        return product_id

    def item_brand(self, response):
        script_text = response.xpath(".//script[contains(.,'entity.brand')]").extract()
        brand = re.search("'entity.brand=(.*)'", script_text[0]).group(1)
        return brand

    def item_rating(self, response):
        if response.xpath('.//*[@class="pr-rating pr-rounded average"]'):
            rating_in_points = self.get_text_from_node(
                response.xpath('.//*[@class="pr-rating pr-rounded average"]/text()'))
            rating = "%.2f" % (float(rating_in_points) * 100 / 5)
        else:
            rating = 'No rating Yet'
        return rating

    def item_model(self, response):
        model_text = self.get_text_from_node(response.xpath('.//*[@class="model_no"]/text()')).strip('(').strip(')')
        model = model_text.split(':')[1]
        return model

    def item_features(self, response, package_flag=False):
        features = []
        if package_flag:
            features_group = response.xpath('(.//*[@id="Features"])[1]//*[@class="features_list"]/ul/li')
        else:
            features_group = response.xpath('.//*[@class="features_list"]/ul/li')
        for li in features_group:
            li_text = ' '.join(li.xpath('.//text()').extract())
            if 'View Energy Guide' not in li_text:
                features.append(li_text)
        return self.normalize(features)

    def item_price(self, response, package_flag=False):
        if package_flag:
            original_price = response.xpath("(.//*[@id='price_details'])[1]//*[contains(@class,'reg_price')]")
            current_price = response.xpath("(.//*[@id='price_details'])[1]//*[@class='price spacing']")
        else:
            original_price = response.xpath(".//*[contains(@class,'reg_price')]")
            current_price = response.xpath('.//*[@class="price spacing"]')

        if response.xpath(".//*[contains(@class,'reg_price')]"):
            price = {'original_price': self.get_text_from_node(
                original_price.xpath("./span[2]/text()")),
                     'current_price': self.get_text_from_node(current_price.xpath('./text()')),
                     'currency': self.item_currency(
                         self.get_text_from_node(current_price.xpath('./text()')))
            }
        else:
            price = {'current_price': self.get_text_from_node(current_price.xpath('./text()')),
                     'currency': self.item_currency(
                         self.get_text_from_node(current_price.xpath('./text()')))
            }
        return price

    def item_trail(self, response):
        trail = []
        for url in response.xpath('.//*[@id="breadcrumb"]/a[position()>1]/@href').extract():
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                trail.append(urljoin('http://www.hhgregg.com/', url))
        return trail

    def item_upc(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(
                response.xpath(
                    '(.//*[@id="Specifications"])[1]//*[span[contains(text(),"Product UPC")]]/'
                    'following-sibling::*[1]/text()'))
        else:
            return self.get_text_from_node(
                response.xpath('//*[span[contains(text(),"Product UPC")]]/'
                               'following-sibling::*[1]/text()'))

    def item_mpn(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(
                response.xpath(
                    '(.//*[@id="Specifications"])[1]//*[span[contains(text(),"Manufacturer Model Number: ")]]'
                    '/following-sibling::*[1]/text()'))
        else:
            return self.get_text_from_node(
                response.xpath(
                    '//*[span[contains(text(),"Manufacturer Model Number: ")]]/following-sibling::*[1]/text()'))

    def item_specification(self, response, package_flag=False):
        if package_flag:
            specification_group = response.xpath('(.//*[@id="Specifications"])[1]//*[@class="specGroup"]')
        else:
            specification_group = response.xpath('.//*[@class="specGroup"]')
        specification = dict()
        for specs in specification_group:
            detail_specs = []
            for sub_specs in specs.xpath('./*[@class="specDetails"]/div'):
                detail_specs.append({
                    self.get_text_from_node(sub_specs.xpath('./*[@class="specdesc"]//text()')): self.get_text_from_node(
                        sub_specs.xpath('./*[@class="specdesc_right"]//text()'))})
            specification[self.get_text_from_node(specs.xpath('./*[@class="specHeader"]//text()'))] = detail_specs
        return specification

    def item_currency(self, data):
        return '$' if '$' in data else ''

    def item_primary_image_url(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(response.xpath('//*[@class="static_img"]/@src'))
        else:
            return self.get_text_from_node(response.xpath('//meta[@property="og:image"]/@content')).split('?')[0]

    def item_images(self, response):
        item = response.meta['item']
        image_urls = []
        json_response = response.body
        if json_response:
            extract_json = re.search('s7jsonResponse\((.*})', json_response).group(1)
            json_decode = json.loads(extract_json)
            image_items = json_decode['set']['item']
            if isinstance(image_items, list):
                for items in json_decode['set']['item']:
                    image_urls.append(urljoin('http://hhgregg.scene7.com/is/image/', items['i']['n']))
            else:
                image_urls.append(urljoin('http://hhgregg.scene7.com/is/image/', image_items['i']['n']))
            item['image_urls'] = image_urls

        yield item

    def parse_pagination(self, response):
        if response.xpath('.//*[@class="pages center"]/a[img[@alt="Next"]]'):
            total_products = response.xpath('(.//*[@class="showing_prod"])[1]/text()').extract()
            request_script_text = response.xpath(
                '//script[contains(.,"SearchBasedNavigationDisplayJS.init")]/text()').extract()
            request_link = re.search("SearchBasedNavigationDisplayJS.init\('(.*)'", request_script_text[0]).group(1)
            if total_products:
                total = total_products[0].split()[0]
                pages = int(total) / 12 + (int(total) % 12 != 0)
                for i in range(1, pages):
                    begin_index = i * 12
                    yield FormRequest(url=request_link,
                                      formdata={
                                          'NUMITEMSINCART': 'item(s)',
                                          'beginIndex': str(begin_index),
                                          'contentBeginIndex': '0',
                                          'facet': '',
                                          'isHistory': 'false',
                                          'langId': '-1',
                                          'orderBy': '6',
                                          'productBeginIndex': str(begin_index),
                                          'requesttype': 'ajax',
                                          'resultType': 'products',
                                      },
                    )

    def get_text_from_node(self, node):
        text_array = node.extract()
        if text_array:
            return self.normalize(text_array[0])
        else:
            return ''

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
