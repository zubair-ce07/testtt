"""
This module scrapes products data from Farfetch website
"""
import json
import re
import urlparse

import scrapy

class FarfetchSpider(scrapy.Spider):
    name = 'farfetch'
    base_url = 'https://www.farfetch.com/pk{}'
    allowed_domains = ['farfetch.com']
    start_urls = [base_url.format('/shopping/men/clothing-2/items.aspx'),
                  base_url.format('/shopping/women/clothing-1/items.aspx'),
                  base_url.format('/shopping/kids/baby-girl-clothing-6/items.aspx')
                 ]
    def parse(self, response):
        """
        This default parse method is used to capture major categories
        like men, women and kids
        :param response:
        :return:
        """
        yield scrapy.Request(url=response.url, method='GET', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept-Language': 'en-US,en;q=0.5'},
                             callback=self.parse_urls)


    def parse_urls(self, response):
        """
        This method is uesd to capture further sub categories of
        major categories.CrawlSpider (rules) can't be uesd in this
        scenario because of its certain limitations and not being able to
        send headers with its default parse method
        :param response:
        :return:
        """
        urls = response.css('._095029 a::attr(href)').extract()
        for url in urls:
            url = urlparse.urljoin(self.base_url, url)
            yield scrapy.Request(url=url, method='GET', headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
                'Accept-Language': 'en-US,en;q=0.5'}, callback=self.parse_product)
        next_page = response.css('.e69df0 a::attr(href)').extract_first()
        if next_page:
            next_page = urlparse.urljoin(response.url, next_page)
            yield scrapy.Request(url=next_page, method='GET', headers={
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
                'Accept-Language': 'en-US,en;q=0.5'},
                                 callback=self.parse_urls)


    def parse_product(self, response):
        product = {}
        raw_data = self.retrieve_data(response)
        if raw_data:
            product['name'] = raw_data.get('productViewModel').get(
                'details').get('shortDescription')
            product['description'] = raw_data.get('productViewModel').get('details').get(
                'description')
            product['gender'] = raw_data.get('productViewModel').get('details').get(
                'genderName')
            product['currency'] = raw_data.get('productViewModel').get('priceInfo').get(
                'default').get('currencyCode')
            product['composition'] = self.composition(raw_data)
            product['care'] = self.care(raw_data)
            product['bread-crumb'] = self.bread_crumb(raw_data)
            product['product_url'] = response.url
            product['brand'] = raw_data.get('productViewModel').get('designerDetails').get('name')
            product['image_urls'] = self.capture_image_urls(raw_data)
            product['skus'] = self.skus_formation(response, raw_data)
            return product


    def retrieve_data(self, response):
        """
        This method extracts data in raw json format from script tag. Data is then to be
        purified by regex and hence load it into pure json format
        :param response:
        :return:
        """
        script = response.css('script::text').extract()[9]
        raw_json_list = re.findall(r"({\"config\".*}})", script)
        if raw_json_list:
            raw_json = raw_json_list[0]
            pure_json = json.loads(raw_json)
            return pure_json
        else:
            return None


    def capture_image_urls(self, raw_data):
        urls = []
        url_list = raw_data.get('productViewModel').get('images').get('main')
        for url in url_list:
            urls.append(url.get('thumbnail'))
        return urls


    def bread_crumb(self, raw_data):
        bread_crumbs = []
        bread_crumb_list = raw_data.get('productViewModel').get('breadcrumb')
        for bread_crumb in bread_crumb_list:
            bread_crumbs.append(bread_crumb.get('text'))
        return bread_crumbs


    def composition(self, raw_data):
        composition = []
        composition_list = raw_data.get('productViewModel').get('composition')
        for item in composition_list:
            composition.append(item.get('value'))
        return composition


    def care(self, raw_data):
        care = []
        care_list = raw_data.get('productViewModel').get('care')
        for item in care_list:
            care.append(item.get('value'))
        return care


    def skus_formation(self, response, raw_data):
        dict_list = []
        size_ids = response.css('#dropdown option::attr(value)').extract()
        del size_ids[0]
        for size_id in size_ids:
            temp_dict = {
                'size': raw_data.get('productViewModel').get('sizes').get('available').get(
                    size_id).get('description'),
                'color': raw_data.get('productViewModel').get('details').get('colors'),
                'price': self.skus_formation_price(size_id, raw_data)
            }
            dict_list.append(temp_dict)
        return dict_list


    def skus_formation_price(self, size_id, raw_data):
        try:
            price = raw_data.get('productViewModel').get('priceInfo').get(size_id).get('finalPrice')
            return price
        except ValueError:
            return raw_data.get('productViewModel').get('priceInfo').get('default').get(
                'finalPrice')

