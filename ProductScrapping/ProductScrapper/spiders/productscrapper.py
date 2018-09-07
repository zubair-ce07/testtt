# -*- coding: utf-8 -*-
import scrapy
import json
from ProductScrapper.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'spider'
    item_counter = 0
    base_url = "https://www.ernstings-family.de:443/wcs/"
    pre_url = "resources/store/10151/productview/bySearchTermDetails/*?"
    post_url = "pageNumber={}&pageSize=24&categoryId={}"
    base_image_path = "//images.ernstings-family.com/product_detail/"

    start_urls = ['https://www.ernstings-family.de/']

    def parse_empty(self, response):
        pass

    def parse(self, response):
        categories_path = ".main-navigation-inner-wrapper li a::attr(href)"
        categories = response.css(categories_path).extract()
        for cat in categories:
            yield scrapy.Request(url=cat, callback=self.parse_main_page)

    def parse_main_page(self, response):
        sub_cat_path = "li[class *= 'item-level1']>a::attr(href)"
        sub_categories = response.css(sub_cat_path).extract()

        special_cat_path = "li[class *= 'special-list-item']>a::attr(href)"
        special_categories = response.css(special_cat_path).extract()

        #  remove duplicate sale links from special categories
        if "sale" not in response.url:
            special_categories = [cat for cat in special_categories if "sale" not in cat]

        #  follow all level 1 and special categories
        for sub_cat in sub_categories:
            yield scrapy.Request(url=sub_cat, callback=self.parse_filter_page)
        for special_cat in special_categories:
            yield scrapy.Request(url=special_cat, callback=self.parse_filter_page)

    '''
    for parse_filter function
     Check total_item_count, get total no of pages to create
     yield that many page requests with new link
    '''
    def parse_filter_page(self, response):
        scripts_path = "script[type *= 'text/javascript']::text"
        scripts = response.css(scripts_path).extract()
        category_id = scripts[3].split('categoryId = "')[1].split('"')[0]
        print("CategoryId: "+category_id)

        # if there are more than one pages,
        # traverse next pages unless finished
        total_items = response.css(".product-count-holder::text").extract_first()
        if total_items:
            total_item_count = int(total_items.split(" ")[0])
            max_page = int(total_item_count/24)+1
            for curr_page in range(1, max_page+1):
                url = self.base_url+self.pre_url+self.post_url
                url = url.format(curr_page, int(category_id))
                yield scrapy.Request(url=url, callback=self.parse_items_from_json)

    def parse_items_from_json(self, response):
        self.item_counter += 1
        # json object containing per page items
        data = json.loads(response.body)
        # it will be parsed to obtain all fields of an Item
        items = data['CatalogEntryView']
        for item in items:
            product = ProductItem()
            product['name'] = item['name']
            product['url'] = item['resourceId']

            labels = []
            if item['xcatentry_issale'] == '1':
                labels.append("sale")
            if item['xcatentry_isnew'] == '1':
                labels.append("neu")
            product["labels"] = labels

            images = []
            for val in range(0, len(item['Attachments'])):
                image_name = item['Attachments'][val]['path']
                images.append(self.base_image_path + image_name)
            product['image_urls'] = images

            sku_count = item['numberOfSKUs']
            skus = []
            for var in range(0, int(sku_count)):
                sku_id = item['SKUs'][var]['SKUUniqueID']
                sku_size = item['SKUs'][var]['Attributes'][0]['Values'][0]['values']
                sku_price = item['SKUs'][var]['Price'][0]['SKUPriceValue']
                skus.append({'id': sku_id, 'size': sku_size, 'price': sku_price})
            product['skus'] = skus

            attributes = item['Attributes']
            for attribute in attributes:
                if attribute['identifier'] == 'details':
                    description = attribute['Values'][0]['values']
                    detail = description.split("</p>")[0].split("<p>")[1] + "\n"
                    points = description.split("</p>")[1].split("<li>")
                    for point in points[1:]:
                        detail += point.replace("</li>\n", "")
                    product['detail'] = detail

                if attribute['identifier'] == 'material':
                    description = attribute['Values'][0]['values']
                    materials = description.split("</ul>")[0].split("<li>")
                    material_string = ""
                    for mat in materials[1:]:
                        material_string += mat.replace("</li>\n", "")
                    product['material'] = material_string

                if attribute['identifier'] == 'search_color':
                    colors = []
                    color_list = attribute['Values']
                    for val in range(0, len(color_list)):
                        color = color_list[val]['values']
                        colors.append(color)
                    product['colors'] = colors
            yield product
