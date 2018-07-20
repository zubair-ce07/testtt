# -*- coding: utf-8 -*-
import json
import re
import scrapy
from scrapy.http.request import Request

from .. import items
from .. import constants


class ToryburchSpider(scrapy.Spider):
    name = 'toryburch'
    start_urls = ['https://www.toryburch.com/']

    def parse(self, response):
        category_menu = response.xpath('//ul[@class="nav-primary"]/li')

        for index in range(1, len(category_menu)):
            url = category_menu[index].xpath('a/@href').extract_first()
            print("Category: " +url)
            yield Request(url, self.parse_main_category)

    def parse_main_category(self, response):
        for sub_category in response.xpath('//div[@class="subcategory__button"]//a[@href]/@href'):
            print("Sub-Category: " + sub_category.extract())
            yield Request(sub_category.extract(), self.parse_sub_category)
        pass

    def parse_sub_category(self, response):
        product_links = response.xpath('//a[@class="product-tile__thumb"]/@href')
        for product_url in product_links:
            #print("Product: " +product_url.extract())
            yield Request(product_url.extract(), callback=self.parse_product)

    def parse_product(self, response):
        product_item = items.ProductItem()
        product_item['product_url'] = response.request.url
        product_item['title'] = response.xpath('//div[@class="product-name"]/h1//text()').extract_first().strip()
        class_id = "v-offset-top-m body-copy--s body-copy product-description__content"
        product_item['description'] = self.parse_description(response.xpath('//div[@class="{}"]'.format(class_id)))
        product_item['variations'] = self.parse_variation_item(response)
        # response.xpath('//div[@class="v-offset-top-m body-copy--s body-copy product-description__content"]/p//text()').extract_first()
        yield product_item
        # pass

    def parse_product_item(self):
        pass

    def parse_description(self, description_html):
        description = []
        description.append(description_html.xpath('p//text()').extract_first().strip())
        traits = description_html.xpath('div[@id="longDescription"]/ul/li//text()').extract()

        for trait in traits:
            description.append(trait.strip())
        return description

    # Parse variation items
    def parse_variation_item(self, html):
        variation_items = []
        for variation in html.xpath('//ul[@id="swatchesselect"]/li'):
            variation_item = items.VariationItem()
            variation_item['display_color_name'] = variation.xpath('a/@title').extract_first()
            variation_item['image_urls'] = self.get_image_urls(html, variation)
            # variation_item['sizes'] = self.parse_size_items(html)
            variation_items.append(variation_item)
        return variation_items

    def get_image_urls(self, html, variation):
        image_urls = []
        image_url_suffixes = ['','_A', '_B', '_C', '_D', '_E', '_F', '_G']
        variation_template_url = variation.xpath('a/img/@src').extract_first()
        variation_template_url = re.search(r'https://s7.toryburch.com/is/image/ToryBurchNA/(\w+_\w+_\w+_)', variation_template_url).group()
        variation_template_url = variation_template_url[:-1]
        for image_index in range(len(html.xpath('//div[@class="product-image-gallery__column"]//img/@src').extract())):
            image_urls.append(variation_template_url + image_url_suffixes[image_index])
        return image_urls

    def parse_size_items(self, html):
        size_items = []
        json_data = html.xpath('//div[@id="main"]//div[@class="page-container"]/script[2]//text()').extract_first()
        try:
            with open(constants.json_file_name, 'w') as f:
                f.write(json_data)
            with open(constants.json_file_name, 'r') as f:
                data = json.load(f)
                data["variations"]["attributes"][2]["vals"]

        except FileNotFoundError as err:
            print(format(err))

        return size_items
