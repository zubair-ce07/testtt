import json
import re

import scrapy
from WALMART.items import WalmartLoader
from scrapy.spiders import CrawlSpider


class WalmartSpider(CrawlSpider):
    name = "walmart"
    start_urls = ["https://www.walmart.com"]

    def parse(self, response):
        data = self.parse_script(response, -3)
        clothing_link = data['header']['quimbyData']['global_header_ny']['headerZone1']['configs']['departments'][5][
            'departments'][0]['department']['clickThrough']['value']
        clothing_link = response.urljoin(clothing_link)
        yield scrapy.Request(clothing_link, callback=self.parse_category_links)

    def parse_category_links(self, response):
        data = self.parse_script(response, -1)
        links = []
        for index in range(2, 4):
            links.append("https://www.walmart.com" + data['presoData']['modules']['top'][1]['configs']['navHeaders'][
                index]['subHeaders'][3]['subnavHeader']['clickThrough']['value'])
        links.append("https://www.walmart.com" + data['presoData']['modules']['top'][1]['configs']['navHeaders'][
            4]['subHeaders'][0]['subnavHeader']['clickThrough']['value'])
        for link in links:
            yield scrapy.Request(link, callback=self.parse_products)

    def parse_products(self, response):
        product_links = response.xpath('//a[contains(@class, "product-title-link")]/@href').extract()
        for link in product_links:
            yield scrapy.Request("https://www.walmart.com" + link, callback=self.parse_item)
        data = self.parse_script(response, -3)
        canonical_next = data['preso']['pageMetadata'].get('canonicalNext')
        if canonical_next:
            yield scrapy.Request(canonical_next, callback=self.parse_products)

    def parse_item(self, response):
        data = self.parse_script(response, -3)
        category = self.parse_category(data)
        description = self.parse_description(data)
        brand = self.parse_brand(data)
        retailer_sku = self.parse_retailer_sku(data)
        skus = self.parse_skus(response, data)
        image_urls = self.parse_image_urls(data)

        loader = WalmartLoader(response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("name", '//h1[@class="fashion-brand-wrapper"]/text()')
        loader.add_xpath("name", '//h1[contains(@class, "prod-ProductTitle")]/@content')
        loader.add_value("brand", brand)
        loader.add_value("description", description)
        loader.add_value("retailer_sku", retailer_sku)
        loader.add_value("category", category)
        loader.add_value("image_urls", image_urls)
        loader.add_value("skus", skus)
        return loader.load_item()

    def parse_script(self, response, index_script):
        required_script_xpath = '//script[contains(text(), "window.__WML_REDUX_INITIAL_STATE__")]/text()'
        script = response.xpath(required_script_xpath).extract_first()
        script = script.lstrip('var _setReduxState = function() {window.__WML_REDUX_INITIAL_STATE__ =')
        script = script[:index_script]
        script = "{" + script
        data = json.loads(script)
        return data

    def parse_product_id(self, data):
        return data['productBasicInfo']['selectedProductId']

    def parse_category(self, data):
        product_id = self.parse_product_id(data)
        general_info = data['product']['idmlMap'][product_id]['modules'].get('GeneralInfo')
        if general_info:
            category = general_info['category_path_name']['values'][0]
            return category
        return "Unavailable"

    def parse_description(self, data):
        product_id = self.parse_product_id(data)
        return data['product']['idmlMap'][product_id]['modules']['LongDescription']['product_long_description']['values'][0]

    def parse_brand(self, data):
        product_id = self.parse_product_id(data)
        return data['product']['idmlMap'][product_id]['modules']['GeneralInfo']['brand']['displayValue']

    def parse_retailer_sku(self, data):
        return data['productId']

    def parse_image_urls(self, data):
        images = data['product']['images']
        image_urls = []
        for image in images:
            for value in images[image]['assetSizeUrls'].values():
                image_urls.append(value)
        return image_urls

    def get_size(self, variants):
        size = variants.get('size', variants.get('clothing_size', "generic"))
        if "size" in size:
            size = re.search('-(.*)', size)
            size = size.group(1)
        return size

    def get_color(self, variants):
        color = variants.get('actual_color', "multi-color")
        if "actual" in color:
            color = re.search('-(.*)', color)
            color = color.group(1)
        return color

    def get_variants(self, products, product):
        variants = products[product].get('variants')
        if variants:
            size_cleaned = self.get_size(variants)
            color_cleaned = self.get_color(variants)
            return size_cleaned, color_cleaned
        return "generic", "generic"

    def parse_skus(self, response, data):
        products = data['product']['products']
        price = response.xpath('//span[@class="price-characteristic"]/@content').extract_first()
        currency = response.xpath('//span[@class="price-currency"]/text()').extract_first()
        skus = {}
        for product in products:
            size_cleaned, color_cleaned = self.get_variants(products, product)
            offer = products[product]['offers'][0]
            color_size = "{}_{}".format(color_cleaned, size_cleaned)
            skus[color_size] = {
                "color": color_cleaned,
                "size": size_cleaned,
                "price": price,
                "currency": currency,
                "availability": data['product']['offers'][offer]['productAvailability']['availabilityStatus'],
            }
        return skus
