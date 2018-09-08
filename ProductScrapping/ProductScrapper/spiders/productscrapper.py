# -*- coding: utf-8 -*-
import scrapy
import json
from ProductScrapper.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'spider'

    start_urls = ['https://www.ernstings-family.de/']

    def parse(self, response):
        """
        This callback scraps the categories links and yields
        callbacks to them.
        :param response: the response object from start_ul
        :return: Yields callbacks for all categories
        """
        categories_path = ".main-navigation-inner-wrapper li a::attr(href)"
        categories = response.css(categories_path).extract()
        for cat in categories:
            yield scrapy.Request(url=cat, callback=self.parse_main_page)

    def parse_main_page(self, response):
        """
        This callback scraps the sub-categories from each
        category page and yields callback for all of them.
        :param response: response object received from hitting
        category link
        :return: yields callbacks for all sub-categories
        """
        sub_cat_path = "li[class *= 'item-level1']>a::attr(href)"
        sub_categories = response.css(sub_cat_path).extract()

        special_cat_path = "li[class *= 'special-list-item']>a::attr(href)"
        special_categories = response.css(special_cat_path).extract()

        #  remove duplicate sale links from special categories
        if "sale" not in response.url:
            special_categories = [cat for cat in special_categories
                                  if "sale" not in cat]

        for cat in sub_categories:
            yield scrapy.Request(url=cat, callback=self.parse_filter_page)
        for cat in special_categories:
            yield scrapy.Request(url=cat, callback=self.parse_filter_page)

    def parse_filter_page(self, response):
        """
        Check total_item_count, get total no of pages to parse
        and follows that many yield requests.
        :param response: response object received from
        hitting sub-category link
        :return: Yields callback requests for all pages of
         current sub-category
        """
        base_url = "https://www.ernstings-family.de:443/wcs/"
        pre_url = "resources/store/10151/productview/bySearchTermDetails/*?"
        post_url = "pageNumber={}&pageSize=24&categoryId={}"
        scripts_path = "script[type *= 'text/javascript']::text"
        product_count_path = ".product-count-holder::text"
        scripts = response.css(scripts_path).extract()
        category_id = scripts[3].split('categoryId = "')[1].split('"')[0]

        # if there are more than one pages,
        # traverse next pages unless finished
        total_items = response.css(product_count_path).extract_first()
        if total_items:
            total_item_count = int(total_items.split(" ")[0])
            max_page = int(total_item_count / 24) + 1
            for curr_page in range(1, max_page + 1):
                full_url = base_url + pre_url + post_url
                next_page_url = full_url.format(curr_page, int(category_id))
                yield scrapy.Request(url=next_page_url,
                                     callback=self.parse_items_from_json)

    def parse_items_from_json(self, response):
        """
        parse json object received in callback to retrieve
        products per page.
        :param response: response object containing products per page
        :return: Yields product Items
        """
        base_image_path = "//images.ernstings-family.com/product_detail/"
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
                images.append(base_image_path + image_name)
            product['image_urls'] = images

            sku_count = item['numberOfSKUs']
            skus = []
            for var in range(0, int(sku_count)):
                current_sku = item['SKUs'][var]
                sku_id = current_sku['SKUUniqueID']
                sku_size = current_sku['Attributes'][0]['Values'][0]['values']
                sku_price = current_sku['Price'][0]['SKUPriceValue']
                skus.append({'id': sku_id,
                             'size': sku_size,
                             'price': sku_price})
            product['skus'] = skus

            attributes = item['Attributes']
            for attribute in attributes:
                if attribute['identifier'] == 'details':
                    description = attribute['Values'][0]['values']
                    detail = description.split("</p>")[0].split("<p>")[1]
                    detail += "\n"
                    points_string = description.split("</ul>")[0]
                    points_string = points_string.split("<p>")[1]
                    points_string = points_string.split("</p>")[1]
                    points = points_string.split("<li>")
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
