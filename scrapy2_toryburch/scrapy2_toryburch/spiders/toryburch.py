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

        category_menu = category_menu[1:]
        for category in category_menu:
            category_name = self.get_category_name(category)
            url = category.xpath('a/@href').extract_first()
            # print("Category: " +url)
            yield Request(url, self.parse_main_category, meta={'category_name' : category_name})

    def get_category_name(self, category):
        for name in category.xpath('a//text()').extract():
            if re.search(r"\w+", name):
                return name

    def parse_main_category(self, response):
        """
        Parses urls of main categories
        """
        sub_categories = response.xpath('//div[@class="subcategory__button"]//a/@href')
        sub_category_names = response.xpath('//div[@class="subcategory__button"]//a//text()')
        for (sub_category, sub_category_name) in zip(sub_categories, sub_category_names):
            meta_data = {
                'category_name' : response.meta['category_name'],
                'sub_category_name' : self.get_sub_category_name(sub_category_name.extract())
            }
            yield Request(sub_category.extract(), self.parse_sub_category, meta=meta_data)

    def get_sub_category_name(self, raw_name):
        raw_name = raw_name.replace("View All ", "")
        return raw_name[:-5]

    def parse_sub_category(self, response):
        """
        Parses urls of sub categories
        """
        product_links = response.xpath('//a[@class="product-tile__thumb"]/@href')
        for product_url in product_links:
            #print("Product: " +product_url.extract())
            yield Request(product_url.extract(), callback=self.parse_product, meta=response.meta)

    def parse_product(self, response):
        """
        Parse product details from the product page
        """
        product_item = items.ProductItem()
        data = json.loads(self.get_json_data(response))
        product_item['product_url'] = response.request.url
        product_item['title'] = self.get_title(response)
        product_item['currency'] = self.get_currency(response)
        product_item['brand'] = data["brand"]
        product_item['store_keeping_unit'] = data["ID"]
        product_item['breadcrumbs'] = self.get_breadcrumbs(response.meta)
        # class_id = "v-offset-top-m body-copy--s body-copy product-description__content"
        # product_item['description'] = self.parse_description(response.xpath('//div[@class="{}"]'.format(class_id)))
        product_item['description'] = self.parse_description(response.css('div.product-description__content'))
        product_item['variations'] = self.parse_variation_item(response)
        yield product_item

    def get_title(self, response):
        return response.xpath('//div[@class="product-name"]/h1//text()').extract_first().strip()

    def get_currency(self, response):
        return response.xpath('//span[@itemprop="priceCurrency"]//text()').extract_first()

    def get_breadcrumbs(self, category_names):
        return [category_names['category_name'], category_names['sub_category_name']]

    def parse_description(self, description_response):
        """
        Helper method
        """
        description = []
        description.append(description_response.xpath('p//text()').extract_first().strip())
        traits = description_response.xpath('div[@id="longDescription"]/ul/li//text()').extract()
        for trait in traits:
            description.append(trait.strip())
        return description

    # Parse variation items
    def parse_variation_item(self, response):
        """
        Parses all variation items for a product and returns the list
        """
        variation_items = []
        for variation in response.xpath('//ul[@id="swatchesselect"]/li'):
            variation_item = items.VariationItem()
            variation_item['display_color_name'] = variation.xpath('a/@title').extract_first()
            variation_item['image_urls'] = self.get_image_urls(response, variation)
            variation_item['sizes'] = self.parse_size_items(response)
            variation_items.append(variation_item)
        return variation_items

    def get_image_urls(self, response, variation):
        """
        Helper method. Returns image urls for a variation item
        """
        image_urls = []
        image_url_suffixes = ['','_A', '_B', '_C', '_D', '_E', '_F', '_G']
        variation_template_url = self.get_image_template(variation)
        for image_index in range(len(response.xpath('//div[@class="product-image-gallery__column"]//img/@src').extract())):
            image_urls.append(variation_template_url + image_url_suffixes[image_index])
        return image_urls

    def get_image_template(self, variation):
        """
        Returns a template string to construct variation image urls
        """
        variation_template_url = variation.xpath('a/img/@src').extract_first()
        variation_template_url = re.search(r'https://s7.toryburch.com/is/image/ToryBurchNA/(\w+_\w+_\w+_)', variation_template_url).group()
        return variation_template_url[:-1]

    def parse_size_items(self, response):
        """
        Parses all size items for the product
        """
        size_items = []
        data = json.loads(self.get_json_data(response))
        standard_price, is_discounted = self.get_standard_price_and_is_discounted(response)
        discounted_price = self.get_discounted_price(response) if is_discounted else "NA"
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

    def get_json_data(self, response):
        """
        Parses and returns json object from html containing product details
        """
        # json_data = response.xpath('//div[@id="main"]//div[@class="page-container"]/script[2]//text()').extract_first()
        json_data = response.css('script:contains("scene7foldername")').extract_first()
        json_data = json_data[json_data.find("{\n\"source\""):]
        json_data = json_data[:-23]
        # braces_index = json_data.find('{', json_data.find('{', json_data.find('{') + 1) + 1)
        # json_data = json_data[braces_index:]
        json_data = json_data.replace(")", "")
        json_data = json_data.replace(";", "")
        json_data = json_data.replace("'", "\"")
        # json_data = json_data[:-10]  # Remove invalid braces to validate json
        return json_data

    def get_standard_price_and_is_discounted(self, response):
        """
        Returns a tuple in the following format:
            ($65.0, True)
        Generally,
            (standard price, is product discounted)
        is_discounted tells us if a discounted price exists.
        standard price can also be in form of a range.
        """
        print("urL: " + response.request.url)
        standard_price = response.xpath('//span[@class="price--standard notonsale"]//text()').extract_first()
        if standard_price is not None: return (standard_price.strip(), False)
        standard_price = response.xpath('//span[@class="minPrice"]//text()').extract_first()
        if standard_price is not None:
            standard_price = standard_price + "-" + response.xpath('//span[@class="maxPrice"]//text()').extract_first()
            return (standard_price, False)
        standard_price = response.xpath('//span[@class="price--standard strikethrough onsale"]//text()').extract_first()
        return (standard_price.strip(), True)

    def get_discounted_price(self, response):
        """
        Helper method
        """
        return response.xpath('//span[@class="price--sale onsale"]//text()').extract_first().strip()
