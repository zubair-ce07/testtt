# -*- coding: utf-8 -*-
import re
from urlparse import urljoin, urlparse
import json
from scrapy import log
import os
import os.path
from shutil import rmtree
from hhgregg import settings
from scrapy.utils.request import request_fingerprint

from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import FormRequest, Request
from scrapinghub.spider import BaseSpider

from hhgregg.items import HhgreggItem


class HhgreggspiderSpider(BaseSpider):
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
        if 'RFG%20H2O%20KIT' not in response.url and response.url!= 'http://www.hhgregg.com/':
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
                item['current_price'] = self.item_current_price(response)
                item['original_price'] = self.item_original_price(response)
                item['currency'] = self.item_currency(response)
                item['source_url'] = response.url
                item['primary_image_url'] = self.item_primary_image_url(response)
                if response.xpath(".//*[@class='available_soon_text2'][contains(.,'DISCONTINUED')]"):
                    item['available_instore'] = False
                    item['available_online'] = False
                    return Request(
                        url='http://hhgregg.scene7.com/is/image//hhgregg/%s?req=set,json,UTF-8' % self.item_sku(
                            item['product_id']),
                        callback=self.item_images, meta={'item': item})
                else:
                    return self.parse_item_availability(response, item)

    def parse_packages(self, response):
        item = HhgreggItem()
        item['description'] = self.item_description(response, True)
        item['title'] = self.item_title(response)
        item['brand'] = self.item_brand(response)
        item['product_id'] = self.item_product_id(response)
        item['sku'] = self.item_sku(item['product_id'])
        item['model'] = self.item_model(response)
        item['source_url'] = response.url
        item['current_price'] = self.item_current_price(response)
        item['original_price'] = self.item_original_price(response)
        item['currency'] = self.item_currency(response)
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
            product['current_price'] = self.item_current_price(product_info_div, True)
            product['original_price'] = self.item_original_price(product_info_div, True)
            products.append(product)
        item['items'] = products
        if response.xpath(".//*[@class='available_soon_text2'][contains(.,'DISCONTINUED')]"):
            item['available_instore'] = False
            item['available_online'] = False
            if item.get('items'):
                return self.parse_package_item_ratings(item['items'].pop(0), item)
            return Request(
                url='http://hhgregg.scene7.com/is/image//hhgregg/%s?req=set,json,UTF-8' % self.item_sku(
                    item['product_id']),
                callback=self.item_images, meta={'item': item})
        else:
            return self.parse_item_availability(response, item, True)

    def parse_item_availability(self, response, item, package_flag=False):
        ParamJS_script_text = response.xpath('(.//script[contains(.,"WCParamJS")])[1]').extract()
        if ParamJS_script_text:
            langId = re.search("WCParamJS\[\"langId\"\]='(.*)'", ParamJS_script_text[0]).group(1)
            storeid = re.search("WCParamJS\[\"storeId\"\]='(.*)'", ParamJS_script_text[0]).group(1)
            catalogid = re.search("WCParamJS\[\"catalogId\"\]='(.*)'", ParamJS_script_text[0]).group(1)
        productid = self.get_text_from_node(response.xpath(".//*[contains(@id,'productId')]/text()"))
        form_data = {
                'catalogId': str(catalogid),
                'langId': str(langId),
                'quantity': '1',
                'requesttype': 'ajax',
                'storeId': str(storeid),
                'zipCode': '10001'
            }
        if package_flag:
            form_data['partnum'] = str(item.get('model').strip())
            form_data['productType'] = 'Kit'
            return FormRequest(
                url='http://www.hhgregg.com/webapp/wcs/stores/servlet/AjaxCheckProductAvailabilityService',
                formdata=form_data, callback=self.check_item_availability, meta={'productid': productid, 'item': item, 'arg_data': form_data}, priority=10)
        else:
            partnum_script_text = response.xpath('(.//script[contains(.,"partNumber")])[1]').extract()
            if partnum_script_text:
                part_num_match = re.search('partNumber\s*=\s*"([^"]+)', partnum_script_text[0], re.IGNORECASE)
                if part_num_match:
                    part_num = part_num_match.group(1).strip()
            else:
                    part_num = response.xpath('(.//*[contains(@id,"productIdForPartNum")])[1]/@id').extract()[0].split('_')[0]
            form_data['partnum'] = (part_num)
            content_type = {'Content-Type': 'application/x-www-form-urlencoded;'}
            return FormRequest(
                url='http://www.hhgregg.com/webapp/wcs/stores/servlet/AjaxCheckProductAvailabilityService',
                formdata=form_data, headers=content_type, callback=self.check_item_availability,
                meta={'productid': productid, 'item': item , 'arg_data': form_data}, priority=10)

    def check_item_availability(self, response):
        item = response.meta['item']
        form_data = response.meta['arg_data']
        productid = response.meta['productid']
        if response.body and not response.xpath(".//h1[contains(.,'Generic System Error ')]"):
            json_data = json.loads(response.body.strip().strip('*/').strip('/*'))
        else:
            req = FormRequest(
                url='http://www.hhgregg.com/webapp/wcs/stores/servlet/AjaxCheckProductAvailabilityService',
                formdata=form_data, callback=self.check_item_availability,
                meta={'productid': productid, 'item': item , 'arg_data': form_data}, priority=1000, dont_filter=True)
            self.delete_cached_page(req)
            return req

        if json_data.get('errorMessageKey') or not json_data.get('catEntryId0'):
            item['available_instore'] = False
            item['available_online'] = False
            if item.get('items'):
                return self.parse_package_item_ratings(item['items'].pop(0), item)
            return Request(
                url='http://hhgregg.scene7.com/is/image//hhgregg/%s?req=set,json,UTF-8' % self.item_sku(
                    item['product_id']),
                callback=self.item_images, meta={'item': item})
        else:
            form_data = {
                'catEntryId_0': str(json_data[u'catEntryId0']),
                'catalogId': str(json_data[u'catalogId'][0]),
                'deliveryAvailable': str(json_data[u'deliveryAvailable_0']),
                'inStoreOnly': 'false',
                'langId': str(json_data[u'langId'][0]),
                'numAvailableLocations': '0',
                'objectId': '',
                'partnum_0': str(json_data[u'partnum_0']),
                'pickupAvailable': str(json_data.get(u'pickupAvailable_0')),
                'productId_0': productid,
                'requesttype': 'ajax',
                'shippingAvailable': str(json_data.get(u'shippingAvailable_0')),
                'storeId': str(json_data[u'storeId'][0]),
                'zipCode': '10001'

            }
            return FormRequest(url='http://www.hhgregg.com/webapp/wcs/stores/servlet/AjaxCheckAvailabilityDisplay',
                               formdata=form_data, callback=self.item_availability, meta={'item': item}, priority=10)

    def item_availability(self, response):
        item = response.meta['item']
        if response.xpath(".//div[contains(.,'Available in')]"):
            item['available_instore'] = True
            item['available_online'] = True
        if item.get('items'):
            return self.parse_package_item_ratings(item['items'].pop(0), item)
        return Request(
            url='http://hhgregg.scene7.com/is/image//hhgregg/%s?req=set,json,UTF-8' % self.item_sku(
                item['product_id']),
            callback=self.item_images, meta={'item': item})

    def parse_package_item_ratings(self, product , item):
        products = []
        return Request('http://www.hhgregg.com/a/item/%s' % product['model'].strip(), meta={'product':product, 'products':products, 'item':item}, callback=self.package_item_rating)

    def package_item_rating(self,respons):
        product = respons.meta['product']
        products = respons.meta['products']
        item = respons.meta['item']
        product['rating'] = self.item_rating(respons)
        products.append(product)
        if item.get('items'):
            product = item['items'].pop(0)
            return Request('http://www.hhgregg.com/a/item/%s' % product['model'].strip(), meta={'product':product, 'products':products, 'item':item}, callback=self.package_item_rating)
        else:
            item['items'] = products
            return Request(
            url='http://hhgregg.scene7.com/is/image//hhgregg/%s?req=set,json,UTF-8' % self.item_sku(
                item['product_id']),
            callback=self.item_images, meta={'item': item})

    def item_title(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(response.xpath('(.//*[@class="bundles_kits_prod_details"]/h1/text())[1]'))
        return self.get_text_from_node(response.xpath(".//*[@id='prod_detail_main']/h1/text()"))

    def item_description(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(response.xpath('//meta[@name="description"]/@content')).strip('<br/>')
        return self.get_text_from_node(response.xpath('//meta[@property="og:description"]/@content')).strip('<br/>')

    def item_sku(self, product_id):
        return '%s_is' % product_id

    def item_product_id(self, response, package_flag=False):
        if package_flag:
            product_id = re.search("hhgregg\/([^_]+)_", response).group(1)
        else:
            script_text = response.xpath(".//script[contains(.,'entity.id')]").extract()
            product_id = re.search("'entity.id=(.*)'", script_text[0]).group(1)
        return product_id

    def item_brand(self, response):
        script_text = response.xpath(".//script[contains(.,'entity.brand')]").extract()
        brand = re.search("'entity.brand=(.*)'", script_text[0])
        if brand:
            return brand.group(1)
        return None

    def item_rating(self, response):
        if response.xpath('.//*[@class="pr-rating pr-rounded average"]'):
            rating_in_points = self.get_text_from_node(
                response.xpath('.//*[@class="pr-rating pr-rounded average"]/text()'))
            rating = "%.2f" % (float(rating_in_points) * 100 / 5)
        else:
            rating = None
        return rating

    def item_model(self, response):
        model_text = self.get_text_from_node(response.xpath('(.//*[@class="model_no"]/text())[1]')).strip('(').strip(
            ')')
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

    def item_current_price(self, response, package_flag=False):
        if package_flag:
            price = self.get_text_from_node(
                response.xpath("((.//*[@id='price_details'])[1]//*[@class='price spacing']/text())[1]"))
        elif response.xpath('.//*[@class="price spacing"]'):
            price = self.get_text_from_node(response.xpath('(.//*[@class="price spacing"]/text())[1]'))
        elif response.xpath(".//*[@id='checkoutModal']"):
            price_script_text = response.xpath(
                ".//script[contains(.,'omnitureProductTag') and contains(.,'prodView')]/text()").extract()
            if price_script_text:
                price = re.search('prodView","([^"]+)', price_script_text[0]).group(1)
        else:
            price = self.get_text_from_node(response.xpath('(.//*[@class="price offerprice bold"]/text())[1]'))
        return float(price.replace(',','').replace('$', '')) if price else None

    def item_original_price(self, response, package_flag=False):
        if package_flag:
            orignal_price = self.get_text_from_node(
                response.xpath(
                    "((.//*[@id='price_details'])[1]//*[contains(@class,'reg_price')]/span[2]/text())[1]")).replace(',',
                                                                                                                    '').replace(
                '$', '')
            return float(orignal_price) if orignal_price else None
        if response.xpath(".//*[contains(@class,'reg_price')]/span[2]/text()"):
            orignal_price = self.get_text_from_node(
                response.xpath("(.//*[contains(@class,'reg_price')]/span[2]/text())[1]")).replace('$', '').replace(',',
                                                                                                                   '')
            return float(orignal_price) if orignal_price else None
        else:
            return self.item_current_price(response)

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
                response.xpath('(//*[span[contains(text(),"Product UPC")]]/'
                               'following-sibling::*[1]/text())[1]'))

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
                property_name = self.get_text_from_node(sub_specs.xpath(
                    './*[@class="specdesc"]//text() | ./*[@class="nospecdesc"]//text()'))
                property_value = self.get_text_from_node(
                    sub_specs.xpath(
                        './*[@class="specdesc_right"]//text() | ./*[@class="nospecdesc_right"]//text()'))
                detail_specs.append({property_name: property_value})
            specification[self.get_text_from_node(specs.xpath('./*[@class="specHeader"]//text()'))] = detail_specs
        return specification

    def item_currency(self, response):
        if response.xpath('.//*[@class="price spacing"]'):
            data = self.get_text_from_node(response.xpath('(.//*[@class="price spacing"]/text())[1]'))
        elif response.xpath(".//*[contains(@class,'reg_price')]/span[2]/text()"):
            data = self.get_text_from_node(response.xpath("(.//*[contains(@class,'reg_price')]/span[2]/text())[1]"))
        else:
            data = self.get_text_from_node(response.xpath('(.//*[@class="price offerprice bold"]/text())[1]'))

        return '$' if '$' in data else ''

    def item_primary_image_url(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(
                response.xpath('(.//*[@class="prod_left"])[1]//*[@class="static_img"]/@src')).strip('//')
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

    def delete_cached_page(self, request):
        ''' Delete a cached request from FilesystemCacheStorage. Returns True if successful. '''
        if not settings.HTTPCACHE_ENABLED or not 'httpcache.FilesystemCacheStorage' in settings.HTTPCACHE_STORAGE:
            self.log('HTTPCACHE is disabled or HTTPCACHE_STORAGE is not FilesystemCacheStorage.', log.WARNING)
            return False
        if not request and not isinstance(request, 'scrapy.http.request.Request'):
            raise TypeError('Invalid argument "request"')
        req_fp = request_fingerprint(request)
        req_dir = os.path.join(settings.HTTPCACHE_DIR, self.name, req_fp[:2], req_fp)
        if not os.path.exists(req_dir):
            local_dir = os.path.join(os.getcwd(), '.scrapy',
                                     settings.HTTPCACHE_DIR, self.name, req_fp[:2], req_fp)
            # local_dir = os.path.join(os.getcwd(), '.scrapy', settings.HTTPCACHE_DIR, self.name, req_fp[:2], req_fp)
            if not os.path.exists(local_dir):
                self.log('Error deleting cached page. Path does not exist or permission denied %s' % req_dir, log.DEBUG)
                return False
            req_dir = local_dir
        try:
            rmtree(req_dir)
            self.log('Deleted cached page %s, url %s' % (req_dir, request.url), log.DEBUG)
            return True
        except Exception as e:
            self.log('Error deleting cached page %s, %s' % (req_dir, e), log.DEBUG)
            return False
    def get_parent_dir(self, directory):
        return os.path.dirname(directory)