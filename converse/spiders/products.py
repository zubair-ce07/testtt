# -*- coding: utf-8 -*-
import math

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from converse.items import ProductData


def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]

PRODUCTS_ON_PAGE = 24


class ProductsSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['www.converse.ca']
    start_urls = ["https://www.converse.ca/"]

    allowed_categories = ['/women/sneakers', '/men/sneakers/', '/women/collection/', '/men/collections/']

    rules = (
        # This rule extracts links for men & women sneakers, only exclusion is all-sneakers category
        Rule(
            LinkExtractor(restrict_css='#nav .level2', allow=allowed_categories, deny=('/all-sneakers/', )),
            callback='parse_product'
        ),
        # This rule check if there is a next page and crawls to it
        # Rule(LinkExtractor(restrict_css='link[rel="next"]'), callback='parse_product'),
    )

    def parse_product(self, response):
        for product in response.css('.category-products .item.last'):
            result = ProductData()
            result['product_cat'] = self.product_cat(product)
            result['gender'], result['category'], result['sub_category'] = self.product_info(product)
            result['brand'] = self.product_brand(product)
            result['name'] = self.product_name(product)
            result['product_id'] = self.product_id(product)
            result['product_url'] = self.product_url(product)
            result['data_id'] = self.data_id(product)
            result['price'], result['currency'] = self.price_info(product)
            result['image_urls'] = self.image_urls(product)
            result['item_info'] = self.item_info(product)
            # Go to item page to fetch additional information
            if result['item_info']:
                request = scrapy.Request(url=result['product_url'], callback=self.parse_item)
                request.meta['result'] = result
            yield result
        # Calculate number of pages based on total products count
        total_pages = self.page_count(response)
        # If number of pages are greater than 1 iteratively go to next page and collect data
        if total_pages >= 2:
            for page_num in range(2, total_pages + 1):
                # Construct url of next page using info like category id and page num etc.
                page_url = self.next_page_url(response, page_num)
                yield scrapy.Request(url=page_url, callback=self.parse_product)

    def parse_item(self, response):
        """
        Fetch results from individual item page
        """
        result = response.meta['result']
        for item in response.css('.cloneItem>img'):
            result['item_info'].append(
                {
                    'color_detail': item.css('img::attr(title)').extract_first()
                }
            )
        yield result

    def product_cat(self, product):
        """
        Get product category by combining gender, category and sub category
        :param product:
        :return: product cat
        """
        product_info = product.css('.product-image::attr(data-category)').extract_first()
        return str(product_info).replace('/', '_')

    def product_info(self, product):
        """
        Get product Information like gender, category and sub category
        :param product:
        :return: gender, category and sub category
        """
        info = str(product.css('.product-image::attr(data-category)').extract_first()).split('/')
        gender = info[0]
        category = info[1]
        sub_category = info[2]
        return gender, category, sub_category

    def product_brand(self, product):
        """
        Get product brand
        """
        return product.css('.product-image::attr(data-brand)').extract_first()

    def product_name(self, product):
        """
        get product name
        """
        return product.css('.product-name>a::text').extract_first()

    def product_url(self, product):
        """
        Get product url
        """
        return product.css('.product-name>a::attr(href)').extract_first()

    def product_id(self, product):
        """
        Get product ID
        """
        img_product_id = product.css('.product-image>img::attr(id)').extract_first()
        return img_product_id.split('-')[-1]

    def data_id(self, product):
        """
        Get data ID
        """
        return product.css('.product-image::attr(data-id)').extract_first()

    def price_info(self, product):
        """
        Get price and currency information
        :param product:
        :return: price, currency
        """
        price = product.css('.price::text').re(r'[0-9\.]+')[0]
        currency = product.css('.price::text').re(r'([a-zA-Z]+)')[0]
        return price, currency

    def image_urls(self, product):
        """
        Get image urls
        """
        img_url = product.css('.product-image>img::attr(src)').extract_first()
        if not img_url.startswith("http"):
            img_url = "https:" + img_url
        return [img_url]

    def item_info(self, product):
        """
        Get item info like iten id and item color
        :param product:
        :return: item id, item color
        """
        info = []
        for item in product.css('ul>li'):
            info.append(
                {
                    'item_id': item.css('li::attr(data-option-label)').extract_first(),
                    'basic_color': item.css('li::attr(data-basic-color)').extract_first()
                }
            )
        return info

    def products_count(self, response):
        """
        Get number of total products in category
        """
        product_count = response.css('.bread_count>strong')
        if product_count:
            return int(product_count.re(r'[0-9]+')[0])

    def page_count(self, response):
        """
        Calculate number of pages based on product count
        """
        if self.products_count(response):
            pages = self.products_count(response)/float(PRODUCTS_ON_PAGE)
            return int(math.ceil(pages))

    def next_page_url(self, response, page_num):
        """
        Construct next page url using page number, category id
        """
        base_url = response.url
        category_id = response.css('.breadcrumbs ul>li::attr(class)').re('\d+')[-1]
        partial_string = "/ajax/infinite-scrolling/catalog/category/view/id/{}/order/position/page/{}/limit/{}/" \
                         "requested-url".format(category_id, page_num, PRODUCTS_ON_PAGE)
        return insert_str(base_url, partial_string, 23)
