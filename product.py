__author__ = 'sayyeda'

import scrapy
import re
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
        product_details = {}
        product_details['spider_name'] = 'asics-us-crawl',
        product_details['retailer'] = 'asics-us',
        product_details['currency'] = response.xpath(
            ".//html/head/meta[@property='og:price:currency']/@content").extract()
        product_details['price'] = response.xpath(
            ".//html/head/meta[@property='og:price:amount']/@content").extract()
        product_details['market'] = 'US'
        current_color = response.xpath(".//*[contains(@class, 'border')]/text()").extract()[0].strip()
        color = re.split(':', current_color)
        if color:
            product_details['Color'] = color[1].strip()


        available_color = response.xpath(".//*[contains(@class, 'colorVariant')]/img/@alt").extract()
        available_colors = []
        for item in available_color:
            item_ = item.strip()
            available_colors.append(item_)

        main_category = response.xpath(".//*[contains(@id, 'breadcrumb')]/ul/li[3]/a/span/text()").extract()
        sub_category = response.xpath(".//*[contains(@id, 'breadcrumb')]/ul/li[5]/a/span/text()").extract()
        all_category = [main_category[0], sub_category[0]]
        product_details['category'] = all_category

        price = response.xpath(".//*[contains(@class, 'price')]/span//text()").extract()[-1].strip()
        if price:
            product_details['price'] = price

        description = response.xpath("//*[contains(@class, 'tabInfoChildContent')]/text()").extract()[3].strip()
        if description:
            product_details['description'] = description

        href = response.url
        product_details['url-original'] = href

        brand = response.xpath(".//*[contains(@class, 'singleProduct')]/meta[1]/@content").extract()[0]
        product_details['brand'] = brand

        first_img_link = response.xpath(".//*[contains(@id, 'product-image-0')]/@data-big").extract()[0]
        sec_img_link = response.xpath(".//*[contains(@id, 'product-image-0')]/@data-rstmb").extract()[0]
        img_src = response.xpath(".//*[contains(@id, 'product-image-0')]/@src").extract()[0]
        imgurls = [first_img_link, sec_img_link, img_src]

        if imgurls:
            product_details['img-urls'] = imgurls

        # product_details['trail'] = ['http://www.asics.com/us/en-us/', href]

        skus = {}
        sku_details = {}
        sel = response.xpath(".//*[contains(@id, 'SelectSizeDropDown')]/li[@class = 'SizeOption inStock']")

        for item in sel:
            if color:
                sku_details['color'] = color[1].strip()
            sku_details['Sku ID'] = item.xpath("meta[1]/@content").extract()[0]
            sku_details['currency'] = item.xpath("meta[3]/@content").extract()
            sku_details['price'] = item.xpath("meta[4]/@content").extract()[0]
            sku_details['size'] = item.xpath("a/text()").extract()[0].strip()[0]
            prev_price =  response.xpath(".//*[contains(@class, 'markdown' )]/del/text()").extract()
            if prev_price:
                sku_details['previous price'] = response.xpath(".//*[contains(@class, 'markdown' )]/del/text()").extract()[0]
            sku_details['Availability'] = 'true'
            skus[sku_details['Sku ID']] = sku_details.copy()

        product_details['sku'] = skus

        name = response.xpath(".//*[contains(@class, 'single-prod-title')]/text()").extract()[-1]
        if name:
            product_details['Name'] = name

        product_details['url'] = href

        for item in all_category:
            if 'men' in item:
                product_details['Gender'] = 'Male'

            if 'women' in item:
                product_details['Gender'] = 'Female'

            if not ('men' in item and 'women' in item):
                product_details['Gender'] = 'Unisex'

            if 'kids' in item:
                product_details['Gender'] = 'Children'


        print(json.dumps(product_details, indent=4))























