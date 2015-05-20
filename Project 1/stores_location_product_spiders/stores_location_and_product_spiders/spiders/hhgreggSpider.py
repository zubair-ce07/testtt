import re
from urlparse import urljoin, urlparse
import json

from scrapy import log
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import FormRequest, Request
from scrapinghub.spider import BaseSpider
from stores_location_and_product_spiders.items import HhgreggItem


class HhgreggSpider(BaseSpider):
    name = "hhgregg_spider"
    allowed_domains = ["hhgregg.com",
                       "scene7.com"]
    start_urls = (
        'http://www.hhgregg.com/',
    )

    rules = [

        Rule(LinkExtractor(deny=['/productfinder/'],
                           restrict_xpaths=['.//*[contains( @id,"WC_CachedHeaderDisplay_links")]',
                                            './/*[@class="product_group_name product_info"]']),
             callback='parse_pagination', follow=True, process_request='add_error_handler'),
        Rule(LinkExtractor(restrict_xpaths=['.//*[@class="information"]/h3/a']),
             callback='get_product_detail', process_request='add_error_handler', )
    ]

    def get_product_detail(self, response):
        if self.item_product_id(response):
            if response.xpath('.//*[@class="kitItemList"]'):
                return self.parse_packages(response)
            else:
                item = HhgreggItem()
                self.populate_item(response, item)
                item['description'] = self.item_description(response)
                item['rating'] = self.item_rating(response)
                item['mpn'] = self.item_mpn(response)
                item['upc'] = self.item_upc(response)
                item['features'] = self.item_features(response)
                item['specifications'] = self.item_specification(response)
                item['source_url'] = response.url
                item['primary_image_url'] = self.item_primary_image_url(response)
                return self.image_request(item)
        else:
            self.log('Item Dropped. Item has no Product ID', log.ERROR)

    def parse_packages(self, response):
        item = HhgreggItem()
        self.populate_item(response, item)
        item['description'] = self.item_description(response, True)
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
            product['sku'] = self.item_sku(product['product_id'], response)
            product['mpn'] = self.item_mpn(product_info_div, True)
            product['upc'] = self.item_upc(product_info_div, True)
            product['features'] = self.item_features(product_info_div, True)
            product['current_price'], product['currency'] = self.item_current_price(product_info_div, True)
            product['original_price'] = self.item_original_price(product_info_div, True)
            products.append(product)
        item['items'] = products
        if item.get('items'):
            return self.parse_package_item_ratings(item['items'].pop(0), item)
        return self.image_request(item)

    def populate_item(self, response, item):
        item['title'] = self.item_title(response)
        item['brand'] = self.item_brand(response)
        item['product_id'] = self.item_product_id(response)
        item['sku'] = self.item_sku(item['product_id'], response)
        item['model'] = self.item_model(response)
        item['current_price'], item['currency'] = self.item_current_price(response)
        item['original_price'] = self.item_original_price(response)
        item['trail'] = self.item_trail(response)
        item['available_instore'] = self.item_available_instore(response)
        item['available_online'] = self.item_available_online(response)

    def parse_package_item_ratings(self, product, item):
        products = []
        return self.request_for_package_item_rating(product, item, products)

    def parse_item_rating(self, response):
        package_flag = response.meta['package_flag']
        item = response.meta['item']
        if package_flag:
            product = response.meta['product']
            products = response.meta['products']
            data = response.body.split('=', 1)[1].strip(';')
            try:
                json_data = json.loads(data)
                if json_data.get('rollup'):
                    product['rating'] = self.normalize_rating(json_data['rollup'].get('d'))
            except ValueError:
                product['rating'] = self.normalize_rating(re.search('d:([^,]+)', data).group(1))
            products.append(product)
            return self.next_item_request(item, products)
        else:
            item['rating'] = self.item_rating(response, item['model'])
            return item

    def item_available_online(self, response):
        if response.xpath('.//*[@id="PDP_AddToCart"]'):
            return True
        else:
            return False

    def item_available_instore(self, response):
        if response.xpath('.//form[@id="CheckAvailabilityForm"]') and response.xpath('.//*[@id="check_store_availability" and contains(@style,"display: block")]'):
            return True
        else:
            return False

    def item_title(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(response.xpath('(.//*[@class="bundles_kits_prod_details"]/h1/text())[1]'))
        return self.get_text_from_node(response.xpath(".//*[@id='prod_detail_main']/h1/text()"))

    def item_description(self, response, package_flag=False):
        if package_flag:
            return self.get_text_from_node(response.xpath('//meta[@name="description"]/@content')).strip('<br/>')
        return self.get_text_from_node(response.xpath('//meta[@property="og:description"]/@content')).strip('<br/>')

    def item_sku(self, product_id, response):
        sku_script = response.xpath(".//script[contains(.,'var sku=')]").extract()
        if sku_script:
            sku_match = re.search("var\s*sku=\s*'([^';]+)", sku_script[0])
            sku = sku_match.group(1) if sku_match else None
        else:
            sku= None

        if not sku: return '%s_is' % product_id  # pattern of sku contains product id and keyword '_is'
        else:
            return sku

    def item_product_id(self, response, package_flag=False):
        if package_flag:
            product_id = re.search("hhgregg\/([^_]+)_", response).group(1)
        else:
            script_text = response.xpath(".//script[contains(.,'entity.id')]").extract()
            if script_text:
                product_id = re.search("'entity.id=(.*)'", script_text[0]).group(1).strip()
            else:
                product_id = None
        return product_id

    def item_brand(self, response):
        script_text = response.xpath(".//script[contains(.,'entity.brand')]").extract()
        brand = re.search("'entity.brand=(.*)'", script_text[0])
        if brand:
            return brand.group(1)
        return None

    def normalize_rating(self, rating_in_points):
        return "%.2f" % (float(rating_in_points) * 100 / 5) if rating_in_points else None

    def item_rating(self, response, product_id=None):
        rating = None
        if response.xpath('.//*[@class="pr-rating pr-rounded average"]'):
            rating_in_points = self.get_text_from_node(
                response.xpath('.//*[@class="pr-rating pr-rounded average"]/text()'))
            rating = self.normalize_rating(rating_in_points)
        if product_id:
            data = response.body.split('=', 1)[1].strip(';')
            try:
                json_data = json.loads(data)
            except ValueError:
                json_data = None
            if json_data and json_data['locales'].get('en_US'):
                product_json = json_data['locales']['en_US'].get('p%s' % product_id)
                if product_json and product_json.get('reviews'):
                    rating = self.normalize_rating(product_json['reviews'].get('avg'))
        return rating

    def item_model(self, response):
        model_text = self.get_text_from_node(response.xpath('(.//*[@class="model_no"]/text())[1]')).strip('(').strip(
            ')')
        model = model_text.split(':')[1]
        return model.strip()

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

    def normalize_price(self, price):
        return float(price.replace(',', '').replace('$', '')) if price else None

    def item_currency(self, response, price):
        if not '$' in price:
            price = self.get_text_from_node(
                response.xpath("(.//*[contains(@class,'reg_price')]/span[2]/text())[1]"))
        return '$' if '$' in price else ''

    def item_current_price(self, response, package_flag=False):
        if package_flag:
            price = self.get_text_from_node(
                response.xpath("((.//*[@id='price_details'])[1]//*[@class='price spacing']/text())[1]"))
            if not price:
                price = self.get_text_from_node(
                    response.xpath("((.//*[@id='price_details'])[1]//*[@class='price offerprice bold']/text())[1]"))
        elif response.xpath('.//*[@class="price spacing"]'):
            price = self.get_text_from_node(response.xpath('(.//*[@class="price spacing"]/text())[1]'))
        elif response.xpath(".//*[@id='checkoutModal']"):
            price_script_text = response.xpath(
                ".//script[contains(.,'omnitureProductTag') and contains(.,'prodView')]/text()").extract()
            if price_script_text:
                price = re.search('prodView","([^"]+)', price_script_text[0]).group(1)
            else:
                price = ''
        else:
            price = self.get_text_from_node(response.xpath('(.//*[@class="price offerprice bold"]/text())[1]'))
        currency = self.item_currency(response,price)
        return self.normalize_price(price), currency

    def item_original_price(self, response, package_flag=False):
        if package_flag:
            original_price = self.get_text_from_node(
                response.xpath(
                    "((.//*[@id='price_details'])[1]//*[contains(@class,'reg_price')]/span[2]/text())[1]"))
            return self.normalize_price(original_price)
        if response.xpath(".//*[contains(@class,'reg_price')]/span[2]/text()"):
            original_price = self.get_text_from_node(
                response.xpath("(.//*[contains(@class,'reg_price')]/span[2]/text())[1]"))
            return self.normalize_price(original_price)
        else:
            original_price, currency = self.item_current_price(response)
            return original_price

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
            extract_json = re.search('s7jsonResponse\((.*})', json_response)
            if extract_json:
                json_decode = json.loads(extract_json.group(1))
                image_items = json_decode['set']['item']
                if isinstance(image_items, list):
                    for items in json_decode['set']['item']:
                        image_urls.append(urljoin('http://hhgregg.scene7.com/is/image/', items['i']['n']))
                else:
                    image_urls.append(urljoin('http://hhgregg.scene7.com/is/image/', image_items['i']['n']))

        if not item.get('primary_image_url'):
            for img in image_urls:
                if '_main' in img:
                    item['primary_image_url'] = img
        item['image_urls'] = image_urls
        if item.get('rating'):
            return item
        else:
            return Request(
                'http://www.hhgregg.com/reviews/pwr/content/%s/contents.js' % self.rating_parameters(
                    item['model'].strip()),
                callback=self.parse_item_rating, meta={'package_flag': False, 'item': item}, dont_filter=True,
                errback=self.handle_error)

    def parse_pagination(self, response):
        if response.xpath('.//*[@class="pages center"]/a[img[@alt="Next"]]'):
            next_page_script = response.xpath('.//*[@class="pages center"]/a[img[@alt="Next"]]/@href').extract()[0]
            next_page_size = re.search('pageSize\s*:\s*"([^"]+)', next_page_script).group(1)
            request_script_text = response.xpath(
                '//script[contains(.,"SearchBasedNavigationDisplayJS.init")]/text()').extract()
            request_link = re.search("SearchBasedNavigationDisplayJS.init\('(.*)'", request_script_text[0]).group(1)
            total_products = response.xpath('(.//*[@class="showing_prod"])[1]/text()').extract()
            if total_products:
                total = total_products[0].split()[0]
                pages = int(total) / int(next_page_size) + (int(total) % int(next_page_size) != 0)
                for i in range(1, pages):
                    begin_index = i * int(next_page_size)
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
                                          }, meta={'dont_merge_cookies': True})

    # To get item rating request will be send at contents.js.
    #  Directory for content.js differs with every product depends upon product id.
    #  This method returns the directory path containing content.js depending on the product id.
    #  This method is copied from the source javascript of website which is used to create directory path there.
    def rating_parameters(self, product_id):
        directory_path = 0
        for letter in product_id:
            char_ascii = ord(letter)
            char_ascii = char_ascii * abs(255 - char_ascii)
            directory_path += char_ascii
        directory_path = directory_path % 1023
        directory_path = "{:0>4}".format(directory_path)
        directory_path = "%s/%s" % (directory_path[:2], directory_path[2:])
        return directory_path

    def handle_error(self, failure):
        if failure.request.meta.get('rules'):
            retry = failure.request.meta.get('retry', 0)
            failure.request.meta['retry'] = retry + 1
            failure.request.dont_filter = True
            if retry <= 3:
                self.log('Request Retrying %s time ' % str(retry + 1), log.INFO)
                return failure.request
            else:
                self.log('Item Dropped Due to %s' % failure.value.message, log.WARNING)
        else:
            item = failure.value.response.meta['item']
            package_flag = failure.value.response.meta.get('package_flag')
            if package_flag:
                product = failure.value.response.meta['product']
                products = failure.value.response.meta['products']
                product['rating'] = None
                products.append(product)
                return self.next_item_request(item, products)
            else:
                return item
    def request_for_package_item_rating(self, product, item, products):
        return Request('http://www.hhgregg.com/reviews/pwr/content/%s/%s-en_US-rollup.js' % (
                self.rating_parameters(product['model']), product['model']),
                           meta={'product': product, 'products': products, 'item': item, 'package_flag': True},
                           callback=self.parse_item_rating, errback=self.handle_error, dont_filter=True)

    def next_item_request(self, item, products):
        if item.get('items'):
            product = item['items'].pop(0)
            return self.request_for_package_item_rating(product, item, products)
        else:
            item['items'] = products
            return self.image_request(item)

    def add_error_handler(self, request):
        request.meta["rules"] = True
        request.meta['dont_merge_cookies'] = True
        req = Request(request.url, callback=request.callback, meta=request.meta, dont_filter=request.dont_filter,
                      errback=self.handle_error)
        return req

    def image_request(self, item):
        return Request(
                url='http://hhgregg.scene7.com/is/image//hhgregg/%s?req=set,json,UTF-8' % item['sku'],
                callback=self.item_images, meta={'item': item}, dont_filter=True)
