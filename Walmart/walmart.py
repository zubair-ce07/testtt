import json

import scrapy
from WALMART.items import WalmartLoader
from scrapy.spiders import CrawlSpider


class WalmartSpider(CrawlSpider):
    name = "walmart"
    start_urls = ["https://www.walmart.com"]

    def parse(self, response):
        data = self.parse_script(response)
        clothing_link = data['header']['quimbyData']['global_header_ny']['headerZone1']['configs']['departments'][6][
            'departments'][0]['department']['clickThrough']['value']
        clothing_link = response.urljoin(clothing_link)
        yield scrapy.Request(clothing_link, callback=self.parse_category_links)

    def parse_category_links(self, response):
        required_script_xpath = '//script[contains(text(), "window.__WML_REDUX_INITIAL_STATE__")]/text()'
        script = response.xpath(required_script_xpath).extract_first()
        script = script.lstrip('var _setReduxState = function() {window.__WML_REDUX_INITIAL_STATE__ =')
        script = script[:-1]
        script = "{" + script
        data = json.loads(script)
        for index in range(6, 9):
            yield scrapy.Request(data['header']['quimbyData']['global_header_ny']['headerZone1']['configs'][
                                     'departments'][1]['departments'][index]['department']['clickThrough']['value'],
                                 callback=self.parse_products)

    def parse_products(self, response):
        product_links = response.xpath('//a[contains(@class, "product-title-link")]/@href').extract()
        for link in product_links:
            yield scrapy.Request("https://www.walmart.com"+link, callback=self.parse_item)
        data = self.parse_script(response)
        canonical_next = data['preso']['pageMetadata'].get('canonicalNext')
        if canonical_next:
            yield scrapy.Request(canonical_next, callback=self.parse_pages)

    def parse_script(self, response):
        required_script_xpath = '//script[contains(text(), "window.__WML_REDUX_INITIAL_STATE__")]/text()'
        script = response.xpath(required_script_xpath).extract_first()
        script = script.lstrip('var _setReduxState = function() {window.__WML_REDUX_INITIAL_STATE__ =')
        script = script[:-3]
        script = "{" + script
        data = json.loads(script)
        return data

    def parse_product_id(self, data):
        product_id = data['productBasicInfo']['selectedProductId']
        return product_id

    def parse_category(self, data):
        product_id = self.parse_product_id(data)
        general_info = data['product']['idmlMap'][product_id]['modules'].get('GeneralInfo')
        if general_info:
            category = general_info['category_path_name']['values'][0]
            return category
        else:
            return "Unavailable"

    def parse_description(self, data):
        product_id = self.parse_product_id(data)
        description = data['product']['idmlMap'][product_id]['modules']['LongDescription']['product_long_description']['values'][0]
        return description

    def parse_brand(self, data):
        product_id = self.parse_product_id(data)
        brand = data['product']['idmlMap'][product_id]['modules']['GeneralInfo']['brand']['displayValue']
        return brand

    def parse_retailer_sku(self, data):
        retailer_sku = data['productId']
        return retailer_sku

    def parse_image_urls(self, data):
        images = data['product']['images']
        image_urls = []
        for image in images:
            for value in images[image]['assetSizeUrls'].values():
                image_urls.append(value)
        return image_urls

    def get_size(self, variants):
        size = variants.get('size')
        if size:
            size_cleaned = size.replace('size-', '')
        else:
            size = variants.get('clothing_size')
            if size:
                size_cleaned = size.replace('clothing_size-', '')
            else:
                size_cleaned = "generic"
        return size_cleaned

    def get_color(self, variants):
        color = variants.get('actual_color')
        if color:
            color_cleaned = color.replace('actual_color-', '')
        else:
            color_cleaned = "multi-color"
        return color_cleaned

    def get_variants(self, products, product):
        variants = products[product].get('variants')
        if variants:
            size_cleaned = self.get_size(variants)
            color_cleaned = self.get_color(variants)
            return size_cleaned, color_cleaned
        else:
            size_cleaned = "generic"
            color_cleaned = "generic"
            return size_cleaned, color_cleaned

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

    def parse_item(self, response):
        data = self.parse_script(response)
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

