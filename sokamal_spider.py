"""
This module extracts product detail from so kamal website
"""
import json
import re

import scrapy


class SoKamalSpider(scrapy.Spider):
    """
    Main class of module
    """
    name = 'sokamal'
    allowed_domains = ['sokamal.com']
    collection_ids = [
        {
            "id": "5430CB18-2D1C-49BF-93D1-F4D69F080DA2",
            "collectionUrl": "fall-18-unstitched"
        },
        {
            "id": "276538CC-F029-4B6B-82EB-E438A6BE7B15",
            "collectionUrl": "fall-18-pret"
        },
        {
            "id": "3CAB40C7-4408-4C84-8E49-9E59ED87017C",
            "collectionUrl": "eid-festive-18-unstitched"
        },
        {
            "id": "CC10E2AF-2576-4E2E-AB9B-50A63B4F314C",
            "collectionUrl": "eid-festive-18-stitched"
        }]
    start_urls = ['https://sokamal.com/collections/fall-18-unstitched?'
                  'varient_fabric=cotton&page=1',
                  'https://sokamal.com/collections/fall-18-unstitched?'
                  'varient_fabric=cotton-satin&page=1',
                  'https://sokamal.com/collections/fall-18-unstitched?page=1&varient_fabric=dobby',
                  'https://sokamal.com/collections/fall-18-pret?page=1&varient_fabric=cotton',
                  'https://sokamal.com/collections/fall-18-pret?varient_fabric=cotton-satin&page=1',
                  'https://sokamal.com/collections/fall-18-pret?page=1&varient_fabric=dobby',
                  'https://sokamal.com/collections/eid-festive-18-unstitched?'
                  'varient_fabric=chiffon&page=1',
                  'https://sokamal.com/collections/eid-festive-18-unstitched?'
                  'page=1&varient_fabric=gip-silk',
                  'https://sokamal.com/collections/eid-festive-18-stitched?'
                  'varient_fabric=lawn&page=1']
    form_data = {
        'cache_id': '',
        'collection_id[]': '',
        'collection_inclusion': 'true',
        'created_max': '',
        'created_min': '',
        'hasVarients': '',
        'location_id': '',
        'order_by': '__createdAt',
        'order_by_seq': 'desc',
        'out_of_stock': '',
        'price_max': '',
        'price_min': '',
        'page': '1',
        'product_url': '',
        'related_product_id': '',
        'skip': '0',
        'status': 'true',
        'storeID': '',
        'take': '48',
        'type': '',
        'type_inclusion': '',
        'varient_fabric': '',
        'varients':	'["fabric:cotton"]',
        'varients_inclusion': 'true',
        'vendor': '',
        'vendor_inclusion': ''
    }

    def parse(self, response):
        """
        this method extracts necessary data to form a request for products
        :param response:
        :return:
        """
        collection_id = self.get_collection_id(response)
        api_url = 'https://fishry-api-live.azurewebsites.net/collection_request'
        raw_script = response.css('script::text')[1].extract()
        store_id = re.findall(r"StoreID = '(.{36})", raw_script)[0]
        cache_id = re.findall(r"cacheVersion = '(.{6})", raw_script)[0]
        varient_fabric = response.css('meta[property="og:url"]::attr(content)').extract_first()
        varient_fabric = re.findall(r"fabric=(.*)&|fabric=(.*)", varient_fabric)[0]
        varient_fabric = ''.join(varient_fabric).strip()
        currency = re.findall(r"currencies_format\":\"(.{3})", raw_script)[0]
        if store_id and cache_id and collection_id:
            self.form_data['cache_id'] = cache_id.encode('UTF-8')
            self.form_data['storeID'] = store_id.encode('UTF-8')
            self.form_data['collection_id[]'] = collection_id
            self.form_data['varient_fabric'] = varient_fabric
            self.form_data['varients'] = '["fabric:{}"]'.format(varient_fabric)
            yield scrapy.FormRequest(
                url=api_url, method='POST', meta={'currency':currency}, dont_filter=True,
                formdata=self.form_data,
                callback=self.parse_product)

    def get_collection_id(self, response):
        """
        This method returns a collection id used in request parameter
        :param response:
        :return:
        """
        collection_url = response.css('meta[property="og:url"]::attr(content)').extract_first()
        collection_url = re.findall(r"collections/(.*)\?", collection_url)[0]
        for item in self.collection_ids:
            if item['collectionUrl'] == collection_url:
                return item['id']
        return None

    def parse_product(self, response):
        """
        This method is used to extracts details about product
        :param response:
        :return:
        """
        product = {}
        json_data = json.loads(response.text)
        if json_data:
            for item in json_data:
                product['name'] = item.get('productName')
                product['description'] = item.get('productDescription')
                product['weight'] = item.get('productWeight')
                product['currency'] = response.meta['currency']
                product['febric'] = self.get_febric(item)
                product['pieces'] = self.get_pieces(item)
                product['publish_date'] = item.get('productPublishDate')
                product['qualtity_left'] = item.get('inventoryQuantity')
                product['skus'] = self.skus_formation(item)
                product['bread-crumb'] = self.get_bread_crumb(item)
                product['product_url'] = item.get('productUrl')
                product['image_urls'] = self.capture_image_urls(item)
                yield product

    @staticmethod
    def retrieve_json_data(json_data):
        """
        This method is used to get specific data from json
        :param json_data:
        :return:
        """
        product_varients = json_data.get('productVarients')
        new_json_data = json.loads(product_varients)
        return new_json_data

    def get_febric(self, json_data):
        """
        returns febric detail
        :param json_data:
        :return:
        """
        febric = self.retrieve_json_data(json_data)[0].get('name')[0]
        return febric

    def get_pieces(self, json_data):
        """
        returns pieces detail
        :param json_data:
        :return:
        """
        pieces = self.retrieve_json_data(json_data)[0].get('name')[1]
        return pieces

    def skus_formation(self, json_data):
        """
        This method forms skus
        :param json_data:
        :return:
        """
        sku_list = []
        product_varients = self.retrieve_json_data(json_data)
        for item in product_varients:
            temp_dict = {
                'price': item.get('price'),
                'size': item.get('name')[2],
                'color': item.get('name')[3]
            }
            sku_list.append(temp_dict)
        return sku_list

    @staticmethod
    def get_bread_crumb(json_data):
        """
        retuens bread crumbs detail
        :param json_data:
        :return:
        """
        bread_crumb_list = []
        product_collection_string = json_data.get('productCollectionsList')
        product_collection_list = product_collection_string.split(',')
        for item in product_collection_list:
            data = json.loads(json_data.get('productCollections'))
            bread_crumb_list.append(data.get(item).get('name'))
        return bread_crumb_list

    @staticmethod
    def capture_image_urls(json_data):
        """
        return images urls
        :param json_data:
        :return:
        """
        url_list = []
        images_url_dict = json.loads(json_data.get('productImage'))
        keys_list = images_url_dict.keys()
        for item in keys_list:
            url_list.append(images_url_dict[item]['Image'])
        return url_list

