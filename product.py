__author__ = 'sayyeda'

import scrapy
import json
import re
from productspider.items import ProductSpiderItem

from scrapy.selector import Selector
from scrapy.http import FormRequest


class ProductDetails(scrapy.Spider):
    name = 'product_details'
    allowed_domain = "asics.com"
    start_urls = ["http://www.asics.com/us/en-us/"]

    def parse(self, response):  # getting links for all categories
        links = response.xpath(
            ".//*[@id='main-menu']//li/div/div/div/ul[contains(@class, 'childLeafNode')]/div//li[contains(@class,"
            " 'yCmsComponent')]/a/@href").extract()
        all_categories = []
        for item in links:
            if not ('http' in item):
                sub_link = "http://www.asics.com" + item
                all_categories.append(sub_link)

        for items in all_categories:
            request = scrapy.Request(items, callback=self.parse_product_link)
            yield request

        for items in all_categories:
            request = scrapy.Request(items, callback=self.pagination)
            yield request

    def pagination(self, response): # getting links for next pages of same category
            next_pages = response.xpath(".//*[contains(@class, 'nm center')]/a/@href").extract()
            next_page_links = []
            for item in next_pages:
                item_ = "http://www.asics.com" + item
                next_page_links.append(item_)

            for item_ in next_page_links:
                next_page_request = scrapy.Request(item_, callback=self.parse_product_link)
                yield next_page_request



    def parse_product_link(self, response):  # getting links of product pages
        links = response.xpath(".//*[contains(@class, 'product-list')]/div/div/a/@href").extract()
        product_links = []
        for item in links:
            product_link = "http://www.asics.com" + item
            product_links.append(product_link)

        for items in product_links:
            request = scrapy.Request(items, callback=self.parse_product_details)
            yield request

    def parse_product_details(self, response):  # Retrieving required product details.

        item_obj = ProductSpiderItem()

        item_obj['spider_name'] = 'asics-us-crawl',
        item_obj['retailer'] = 'asics-us',
        item_obj['currency'] = response.xpath(
            ".//html/head/meta[@property='og:price:currency']/@content").extract()
        item_obj['price'] = response.xpath(".//*[contains(@class, 'price')]/span//text()").extract()[-1].strip()
        item_obj['market'] = 'US'
        current_color = response.xpath(".//*[contains(@class, 'border')]/text()").extract()[0].strip()
        color = re.split(':', current_color)
        if color:
            item_obj['color'] = color[1].strip()


        main_category = response.xpath(".//*[contains(@id, 'breadcrumb')]/ul/li[3]/a/span/text()").extract()
        sub_category = response.xpath(".//*[contains(@id, 'breadcrumb')]/ul/li[5]/a/span/text()").extract()
        all_category = [main_category[0], sub_category[0]]
        item_obj['category'] = all_category

        description = response.xpath("//*[contains(@class, 'tabInfoChildContent')]/text()").extract()[3].strip()
        if description:
            item_obj['description'] = description

        href = response.url
        item_obj['url_original'] = href

        brand = response.xpath(".//*[contains(@class, 'singleProduct')]/meta[1]/@content").extract()[0]
        item_obj['brand'] = brand

        first_img_link = response.xpath(".//*[contains(@id, 'product-image-0')]/@data-big").extract()[0]
        sec_img_link = response.xpath(".//*[contains(@id, 'product-image-0')]/@data-rstmb").extract()[0]
        img_src = response.xpath(".//*[contains(@id, 'product-image-0')]/@src").extract()[0]
        imgurls = [first_img_link, sec_img_link, img_src]

        if imgurls:
            item_obj['img_urls'] = imgurls

        skus = {}

        sel = response.xpath(".//*[contains(@id, 'SelectSizeDropDown')]/li[@class = 'SizeOption inStock']")

        for item in sel:
            sku_details = {}
            if color:
                sku_details['color'] = color[1].strip()
            sku_details['Sku ID'] = item.xpath("meta[1]/@content").extract()[0]
            sku_details['currency'] = item.xpath("meta[3]/@content").extract()
            sku_details['price'] = item.xpath("meta[4]/@content").extract()[0]
            size_ = item.xpath("a/text()").extract()[0]
            size = ' '.join(size_.split())
            sku_details['size'] = size

            prev_price =  response.xpath(".//*[contains(@class, 'markdown' )]/del/text()").extract()
            if prev_price:
                sku_details['previous price'] = response.xpath(".//*[contains(@class, 'markdown' )]/del/text()").extract()[0]
            sku_details['Availability'] = 'true'
            skus[sku_details['Sku ID']] = sku_details

        item_obj['skus'] = skus


        name = response.xpath(".//*[contains(@class, 'single-prod-title')]/text()").extract()[-1]
        if name:
            item_obj['name'] = name

        item_obj['url'] = href

        for item in all_category:
            if 'men' in item:
                item_obj['gender'] = 'Male'

            if 'women' in item:
                item_obj['gender'] = 'Female'

            if not ('men' in item and 'women' in item):
                item_obj['gender'] = 'Unisex'

            if 'kids' in item:
                item_obj['gender'] = 'Children'

        available_color = response.xpath(".//*[contains(@class, 'colorVariant')]/img/@alt").extract()
        available_colors = []
        for item in available_color:
            item_ = item.strip()
            available_colors.append(item_)
        item_obj['available_colors'] = available_colors



        yield item_obj






















