# -*- coding: utf-8 -*-
# from captchaMiddleware.middleware import RETRY_KEY
import scrapy
from scrapy.http.request import Request
import random
import json
import re
from urllib import urlencode

from .. import items
from .. import settings

 #Request("https://www.sears.com/appliances-bundles-kitchen-suites/b-1237492439", cookie={"IntnlShip":"US%7CUSD"})


class SearsSpider(scrapy.Spider):
    name = 'sears'
    base_url = "https://www.sears.com"
    category = None

    cookies = {"IntnlShip": "US|USD"}
    headers = {"AuthId": "aA0NvvAIrVJY0vXTc99mQQ=="}
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; '
                      'Intel Mac OS X 10.13; '
                      'rv:62.0) Gecko/20100101 Firefox/62.0'
    }

    def start_requests(self):
        yield Request(
            'https://www.sears.com/en_us.html',
            callback=self.parse,
            cookies=self.cookies,
            headers=self.headers
        )

    def parse(self, response):
        category_urls = response.xpath('//ul[@class="gnf_clr "]//a/@href').extract()
        category_names = response.xpath('//ul[@class="gnf_clr "]//a//text()').extract()
        for (category_url, category_name) in zip(category_urls, category_names):
            category_url = self.base_url + category_url
            meta_data = {
                'main_category_name' : [category_name],
                #'dont_redirect': True,
                #'handle_httpstatus_list': [ 500]
            }
            if self.category is None:
                 yield Request(category_url,
                               callback=self.parse_main_category,
                               meta=meta_data,
                               cookies=self.cookies,
                               headers=self.headers)
            else:
                if category_name == self.category:
                    yield Request(category_url,
                                  callback=self.parse_main_category,
                                  cookies=self.cookies,
                                  headers=self.headers)

    def parse_main_category(self, response):
        print("URL: " + response.request.url)
        category_urls, category_names = self.get_main_category_urls_and_names(response)
        if category_urls:
            for (url, name) in zip(category_urls, category_names):
                url = response.urljoin(url)
                yield Request(url, callback=self.parse_main_category,
                              cookies=self.cookies,
                              headers=self.headers)
        else:
            print("\nProducts list URL:" + response.request.url)
            self.set_request_parameters(response)
            catgroupid_path_url = "https://www.sears.com/browse/services/v1/" \
                                  "hierarchy/fetch-paths-by-id/" + str(self.catgroupid)\
                                  + "?clientId=obusearch&site=sears"
            yield Request(catgroupid_path_url,
                          callback=self.parse_catgroupid_path,
                          cookies=self.cookies,
                          headers=self.headers)

    def get_main_category_urls_and_names(self, response):
        urls = response.xpath('(//div[@class="leftNav '
                              'parbase section"])[1]//a/@href').extract()
        names = response.xpath('(//div[@class="leftNav '
                               'parbase section"])[1]//a//text()').extract()
        return (urls, names)

    def get_main_category_metadata(self, response, name):
        breadcrumbs = response.meta['main_category_name']
        breadcrumbs.append(name)
        return {
            'main_category_name' : breadcrumbs,
        }

    def set_request_parameters(self, response):
        self.catgroupid = re.search(r'b-[0-9]+', response.request.url).group()[2:]
        js_data = self.get_js_data(response)
        self.storeid = js_data["storeId"]
        self.catalogid = js_data["catalogId"]

    def get_js_data(self, response):
        js_data = response.css('script:contains("shc = $.extend(shc, {")').extract_first()
        js_data = js_data[js_data.find('{'):js_data.find('}')+1]
        js_data = js_data.replace(':','\":')
        js_data = js_data.replace(",\r\n ", ",\r\n \"")
        js_data = js_data.replace("{\r\n ", "{\r\n\"")
        js_data = js_data.replace('\'', '\"')
        return json.loads(js_data)

    def parse_catgroupid_path(self, response):
        json_response = json.loads(response.body_as_unicode())
        if json_response["data"]:
            if json_response["data"][0]["catgroups"]:
                self.levels = json_response["data"][0]["catgroups"][0]["namePath"]
                self.catgroupid_path = json_response["data"][0]["catgroups"][0]["idPath"]
                self.levels = self.levels.replace(" ", "+")
                params = {
                    "catgroupId": self.catgroupid,
                    "catalogId": self.catalogid,
                    "catgroupIdPath": self.catgroupid_path,
                    "levels": self.levels,
                    "primaryPath": self.levels,
                    "rmMattressBundle": "true",
                    "searchBy": "subcategory",
                    "storeId": self.storeid,
                    "tabClicked": "All",
                    "visitorId": "Test"
                }
                query_url = "https://www.sears.com/service/search" \
                            "/v2/productSearch?" + urlencode(params)
                yield Request(url=query_url,
                              callback=self.parse_products_json,
                              cookies=self.cookies,
                              headers=self.headers
                )

    def parse_products_json(self, response):
        json_response = json.loads(response.body_as_unicode())
        for product in json_response["data"]["products"]:
            yield Request(response.urljoin(product["url"]),
                          callback=self.parse_product_item,
                          cookies=self.cookies,
                          headers=self.headers
            )

    def parse_product_item(self, response):
        print(response.request.url)
        self.item = items.ProductItem()
        self.item['product_url'] = response.request.url
        # self.item['title'] = self.get_product_title(response)
        # self.item['description'] = self.get_description(response)
        self.product_id = re.search(r'p-\w+', response.request.url).group()[2:]
        url = "https://www.sears.com/content/pdp/config/products/v1/products/" \
              + self.product_id + "?site=sears"
        yield Request(url, callback=self.parse_product_info)


    def parse_product_info(self, response):
        print("")
        print("In Product Info Request")
        json_response = json.loads(response.body_as_unicode())

        breadcrumbs = json_response["data"]["productmapping"]["primaryWebPath"]
        if breadcrumbs:
            self.item["breadcrumbs"] = []
            for breadcrumb in breadcrumbs:
                self.item["breadcrumbs"].append(breadcrumb["name"])

        self.item["store_keeping_unit"] = json_response["data"]["product"]["id"]
        self.item["title"] = json_response["data"]["product"]["seo"]["title"]
        self.item["description"] = []

        descriptions = json_response["data"]["product"]["desc"]
        if descriptions:
            for description in descriptions:
                self.item["description"].append(description["val"])
        try:
            self.item["brand"] = json_response["data"]["product"]["brand"]["name"]
        except KeyError as err:
            self.item["brand"] = self.base_url
        self.item['variations'] = []
        if json_response["data"].get("attributes", False):
            variations = json_response["data"]["attributes"]["variants"]
            if variations:
                variation_no = 0
                for variation in variations:
                    print("")
                    print("In variations\n")
                    should_yield = True if variation_no == len(variations) -1 else False
                    for item in self.process_and_add_variation(variation, should_yield):
                        pass
        else:
            new_variation_item = items.VariationItem()
            # new_variation_item['display_color_name"]
            self.item["variations"].append(self.get_self_variation(json_response))
            url = "https://www.sears.com/content/pdp/products/pricing/v2/get/" \
              "price/display/json?offer=" + self.product_id + "&site=SEARS"
            print("")
            print("In self variations\n")
            header = self.headers
            header["X-Requested-With"] = "XMLHttpRequest"
            yield Request(url,
                          callback=self.parse_size_item,
                          headers=self.headers,
                          cookies=self.cookies,
                          meta= self.get_meta_data_from_variation(None, True))

    def get_self_variation(self, product_info):
        new_variation_item = items.VariationItem()
        new_variation_item["display_color_name"] = "Self"
        images = product_info['data']['product']['assets']['imgs']
        new_variation_item["image_urls"] = []
        if images:
            for image in images[0]["vals"]:
                new_variation_item["image_urls"].append(image['src'])
        return new_variation_item

    def process_and_add_variation(self, variation, should_yield):  # Parse Variation Item
        """
        The data contains a new variation for each size item.
        Hence, before creating a new variation item, it is checked
        if it already exists.
        The variation name is passed to the size item as meta data,
        so that the size item will be appended in its own variation.
        """
        self.add_variation_if_does_not_exist(variation)
        url = "https://www.sears.com/content/pdp/products/pricing/v2/get/" \
                      "price/display/json?offer=" + variation["offerId"] + \
                      "&priceMatch=Y&memberType=G&urgencyDeal=Y&site=SEARS"
        header = self.headers
        header["X-Requested-With"] = "XMLHttpRequest"
        yield Request(url,
                      callback=self.parse_size_item,
                      headers=self.headers,
                      cookies=self.cookies,
                      meta=self.get_meta_data_from_variation(variation, should_yield))

    def add_variation_if_does_not_exist(self, variation):
        variation_name = self.get_colour_name(variation)
        if not self.does_variation_exist(variation_name):
            new_variation_item = items.VariationItem()
            new_variation_item['display_color_name'] = variation_name
            new_variation_item['image_urls'] = self.get_image_urls(variation)
            self.item["variations"].append(new_variation_item)

    def does_variation_exist(self, name):
        for variation in self.item['variations']:
            if variation['display_color_name'] == name:
                return True
        return False

    def get_colour_name(self, variation):
        attributes = variation.get('attributes', [])
        for attribute in attributes:
            isColor = re.search(r'(?i)color', attribute['name'])
            if isColor is not None:
                return attribute['value']
        return "No name"

    def get_image_urls(self, variation):
        image_urls = []
        images = variation["featuredImages"]
        for image in images:
            image_urls.append(image["src"])
        return image_urls

    def get_meta_data_from_variation(self, variation, should_yield):
        return {
            "size" : self.get_size(variation) if variation is not None else None,
            "is_available" : variation["isAvailable"] if variation is not None else None,
            "variation_name" : self.get_colour_name(variation) if variation is not None else None,
            "should_yield" : should_yield
        }

    def parse_size_item(self, response): #  Parse Size Item
        """

        """
        print(response.meta)
        json_response = json.loads(response.body_as_unicode())
        new_size_item = items.SizeItem()
        new_size_item["price"], \
        new_size_item["discounted_price"], \
        new_size_item["is_discounted"] = \
            self.get_price_discountedprice_isdiscounted(json_response)
        new_size_item["size_name"] = response.meta["size"]
        new_size_item["is_available"] = response.meta["is_available"]
        self.append_size_item_in_respective_variation(new_size_item, response.meta["variation_name"])
        if response.meta["should_yield"]:
            yield self.item

    def get_size(self, variation):
        attributes = variation['attributes']
        for attribute in attributes:
            isSize = re.search(r'(?i)size', attribute['name'])
            if isSize is not None:
                return attribute['value']
        return None

    def get_price_discountedprice_isdiscounted(self, size_data):
        detailed_size_data = size_data["priceDisplay"]["response"]
        if detailed_size_data:
            old_price = detailed_size_data[0]["oldPrice"]["numeric"]
            new_price = detailed_size_data[0]["finalPrice"]["numeric"]
            if str(old_price) == "0": #  Not discounted
                return (str(new_price), "None", False)
            else:
                return (str(old_price), str(new_price), True)
        return ("None", "None", False)

    def append_size_item_in_respective_variation(self, size_item, variation_name):
        for variation in self.item.get('variations', []):
            if variation['display_color_name'] == variation_name:
                variation["sizes"].append(size_item)

# class ProductItem(scrapy.Item):
#     product_url = scrapy.Field()
#     store_keeping_unit = scrapy.Field()
#     title = scrapy.Field()
#     brand = scrapy.Field()
#     description = scrapy.Field()
#     locale = scrapy.Field()
#     currency = scrapy.Field()
#     variations = scrapy.Field()
#     breadcrumbs = scrapy.Field()
#
#
# class VariationItem(scrapy.Item):
#     display_color_name = scrapy.Field()
#     image_urls = scrapy.Field()
#     sizes = scrapy.Field()
#
#
# class SizeItem(scrapy.Item):
#     size_name = scrapy.Field()
#     is_available = scrapy.Field()
#     price = scrapy.Field()
#     is_discounted = scrapy.Field()
#     discounted_price = scrapy.Field()