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
    start_urls = ['https://www.sears.com/en_us.html']
    base_url = "https://www.sears.com"
    category = None
    headers = {"AuthId": "9bfa4bf184144a0aace5d60bfabb2ec5"}

    #           "scrapy crawl sears -a category=Auto\n"
    #           "The category is case sensitive\n")

    def parse(self, response):
        print("In Parse")
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
                               cookies=settings.cookie,
                               headers=self.headers)
            else:
                if category_name == self.category:
                    yield Request(category_url,
                                  callback=self.parse_main_category,
                                  cookies=settings.cookie,
                                  headers=self.headers)

    def parse_main_category(self, response):
        print("URL: " + response.request.url)
        category_urls, category_names = self.get_main_category_urls_and_names(response)
        if category_urls:
            for (url, name) in zip(category_urls, category_names):
                url = self.modify_url_if_necessary(url)
                # print("Sub category url: " + url)
                yield Request(url, callback=self.parse_main_category,
                              cookies=settings.cookie,
                              headers=self.headers)
        else:
            print("\nProducts list URL:" + response.request.url)
            self.set_request_parameters(response)
            catgroupid_path_url = "https://www.sears.com/browse/services/v1/" \
                                  "hierarchy/fetch-paths-by-id/" + str(self.catgroupid)\
                                  + "?clientId=obusearch&site=sears"
            yield Request(catgroupid_path_url,
                          callback=self.parse_catgroupid_path,
                          cookies=settings.cookie,
                          headers=self.headers)

    def modify_url_if_necessary(self, url):
        if url[:2] == "//":
            url = "https:" + url
        return url

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
        print("")
        # print("here\n")
        json_response = json.loads(response.body_as_unicode())
        if json_response["data"]:
            if json_response["data"][0]["catgroups"]:
                self.levels = json_response["data"][0]["catgroups"][0]["namePath"]
                self.catgroupid_path = json_response["data"][0]["catgroups"][0]["idPath"]
                self.levels = self.levels.replace(" ", "+")
                params = {
                "catgroupId" : self.catgroupid,
                "catalogId" : self.catalogid,
                "catgroupIdPath" : self.catgroupid_path,
                "levels" : self.levels,
                "primaryPath" : self.levels,
                "rmMattressBundle" : "true",
                "searchBy" : "subcategory",
                "storeId" : self.storeid,
                "tabClicked" : "All",
                "visitorId" : "Test"
            }
            # print(params)
            query_url = "https://www.sears.com/service/search" \
                        "/v2/productSearch?" + urlencode(params)
            yield Request(url=query_url,
                          callback=self.parse_products_json,
                          cookies=settings.cookie,
                          headers=self.headers
            )

    def parse_products_json(self, response):
        new_item = items.ProductItem()
        jsonresponse = json.loads(response.body_as_unicode())
        # print("json response\n")
        # print(jsonresponse)
        yield new_item

    def parse_product_item(self, response):
        # print("")
        # print("Product page URL: " + response.request.url)
        new_item = items.ProductItem()
        new_item['product_url'] = response.request.url
        new_item['title'] = self.get_product_title(response)
        new_item['description'] = self.get_description(response)
        self.get_product_info_data(response)
        self.get_breadcrumb_list(response)
        yield new_item
        pass

    def get_title(self, response):
        return response.xpath('//h1[@class="product-title title-2"]').extract_first()

    def get_store_keeping_unit(self, response):
        return response.xpath('(//section[@id="description"]/header//small)[1]').extract_first()

    def get_description(self, response):
        description = response.xpath('//div[@id="productShortDescription"]//li//text()').extract()
        long_description_xpath = '//div[@id="productLongDescription"]//text()'
        description.append(response.xpath(long_description_xpath).extract_first())
        return description

    def get_product_info_data(self, response):
        # print("Product Info")
        json_data = response.css('script:contains("priceCurrency")').extract_first()
        # print(json_data)

    def get_breadcrumb_list(self, response):
        # print("Bread Crumbs")
        json_data = response.css('script:contains("BreadcrumbList")').extract_first()
        # print(json_data)


