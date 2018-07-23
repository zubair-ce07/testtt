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
            # print("Category: " +url)
            yield Request(url, self.parse_main_category)

    def parse_main_category(self, response):
        """
        Parses urls of main categories
        """
        for sub_category in response.xpath('//div[@class="subcategory__button"]//a[@href]/@href'):
            # print("Sub-Category: " + sub_category.extract())
            yield Request(sub_category.extract(), self.parse_sub_category)

    def parse_sub_category(self, response):
        """
        Parses urls of sub categories
        """
        product_links = response.xpath('//a[@class="product-tile__thumb"]/@href')
        for product_url in product_links:
            #print("Product: " +product_url.extract())
            yield Request(product_url.extract(), callback=self.parse_product)

    def parse_product(self, response):
        """
        Parse product details from the product page
        """
        product_item = items.ProductItem()
        data = json.loads(self.get_json_data(response))
        product_item['product_url'] = response.request.url
        product_item['title'] = response.xpath('//div[@class="product-name"]/h1//text()').extract_first().strip()
        product_item['currency'] = response.xpath('//span[@itemprop="priceCurrency"]//text()').extract_first()
        product_item['brand'] = data["brand"]
        product_item['store_keeping_unit'] = data["ID"]
        class_id = "v-offset-top-m body-copy--s body-copy product-description__content"
        product_item['description'] = self.parse_description(response.xpath('//div[@class="{}"]'.format(class_id)))
        product_item['variations'] = self.parse_variation_item(response)
        yield product_item

    def parse_description(self, description_html):
        """
        Helper method
        """
        description = []
        description.append(description_html.xpath('p//text()').extract_first().strip())
        traits = description_html.xpath('div[@id="longDescription"]/ul/li//text()').extract()
        for trait in traits:
            description.append(trait.strip())
        return description

    # Parse variation items
    def parse_variation_item(self, html):
        """
        Parses all variation items for a product and returns the list
        """
        variation_items = []
        for variation in html.xpath('//ul[@id="swatchesselect"]/li'):
            variation_item = items.VariationItem()
            variation_item['display_color_name'] = variation.xpath('a/@title').extract_first()
            variation_item['image_urls'] = self.get_image_urls(html, variation)
            variation_item['sizes'] = self.parse_size_items(html)
            variation_items.append(variation_item)
        return variation_items

    def get_image_urls(self, html, variation):
        """
        Helper method. Returns image urls for a variation item
        """
        image_urls = []
        image_url_suffixes = ['','_A', '_B', '_C', '_D', '_E', '_F', '_G']
        variation_template_url = variation.xpath('a/img/@src').extract_first()
        variation_template_url = re.search(r'https://s7.toryburch.com/is/image/ToryBurchNA/(\w+_\w+_\w+_)', variation_template_url).group()
        variation_template_url = variation_template_url[:-1]
        for image_index in range(len(html.xpath('//div[@class="product-image-gallery__column"]//img/@src').extract())):
            image_urls.append(variation_template_url + image_url_suffixes[image_index])
        return image_urls

    def parse_size_items(self, html):
        """
        Parses all size items for the product
        """
        size_items = []
        # json_string = self.get_json_data(html)
        data = json.loads(self.get_json_data(html))
        standard_price, is_discounted = self.get_standard_price_and_is_discounted(html)
        discounted_price = self.get_discounted_price(html) if is_discounted else "NA"
        for size_entry in data["variations"]["attributes"][1]["vals"]:
            new_size_item = items.SizeItem()
            new_size_item['size_name'] = size_entry["val"]
            if new_size_item['size_name'] == 'OS': return []
            new_size_item['is_available'] = data["inStock"]
            new_size_item['price'] = standard_price
            new_size_item['is_discounted'] = is_discounted
            new_size_item['discounted_price'] = discounted_price
            size_items.append(new_size_item)
        return size_items

    def get_json_data(self, html):
        """
        Parses and returns json object from html containing product details
        """
        json_data = html.xpath('//div[@id="main"]//div[@class="page-container"]/script[2]//text()').extract_first()
        braces_index = json_data.find('{', json_data.find('{', json_data.find('{') + 1) + 1)
        json_data = json_data[braces_index:]
        json_data = json_data.replace(")", "")
        json_data = json_data.replace(";", "")
        json_data = json_data.replace("'", "\"")
        json_data = json_data[:-10]  # Remove invalid braces to validate json
        return json_data

    def get_standard_price_and_is_discounted(self, html):
        """
        Returns a tuple in the following format:
            ($65.0, True)
        Generally,
            (standard price, is product discounted)
        is_discounted tells us if a discounted price exists.
        standard price can also be in form of a range.
        """
        print("urL: " + html.request.url)
        standard_price = html.xpath('//span[@class="price--standard notonsale"]//text()').extract_first()
        if standard_price is not None: return (standard_price.strip(), False)
        standard_price = html.xpath('//span[@class="minPrice"]//text()').extract_first()
        if standard_price is not None:
            standard_price = standard_price + "-" + html.xpath('//span[@class="maxPrice"]//text()').extract_first()
            return (standard_price, False)
        standard_price = html.xpath('//span[@class="price--standard strikethrough onsale"]//text()').extract_first()
        return (standard_price.strip(), True)

    def get_discounted_price(self, html):
        """
        Helper method
        """
        return html.xpath('//span[@class="price--sale onsale"]//text()').extract_first().strip()
