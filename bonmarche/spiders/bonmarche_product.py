import json
from scrapy import Spider, Request
from w3lib.url import url_query_cleaner
from bonmarche.items import ProductItem


class ProductParser(Spider):
    name = "bonmarche-parse"

    def parse(self, response):
        product = ProductItem(brand="bonmarche", market="UK", retailer="bonmarche-uk", currency="GBP", gender="women")
        product['retailer_sku'] = self.product_id(response)
        product['trail'] = self.product_trail(response)
        product['category'] = self.product_category(response)
        product['url'] = response.url
        product['name'] = self.product_name(response)
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['image_urls'] = []
        product['skus'] = {}
        product['spider_name'] = self.name

        color_urls = self.color_requests(response)
        request = self.process_request(color_urls, product)
        yield request

    def product_id(self, response):
        return response.css('::attr(data-masterid)').extract_first()

    def product_trail(self, response):
        trail_urls = response.meta.get('trail', [])
        return [[url.split("/")[-2].split(".")[0], url] for url in trail_urls]

    def product_category(self, response):
        categories = response.css('.breadcrumb-element [itemprop=name]::text').extract()
        return [category.strip() for category in categories if category][1:-1]

    def product_name(self, response):
        return response.css('.xlt-pdpName::text').extract_first()

    def product_description(self, response):
        description = response.css('.product-description::text, .feature-value::text').extract()
        return [desc.strip() for desc in description if desc][:-1]

    def product_care(self, response):
        return response.css('.product-description::text, .feature-value::text').extract()[-1:]

    def color_requests(self, response):
        requests = []
        color_urls = response.css('.color .swatchanchor.selectable:not(.selected)::attr(href)').extract()
        color_urls.append(response.url)
        for url in color_urls:
            request = Request(url, callback=self.parse_colors, dont_filter=True)
            requests.append(request)
        return requests

    def parse_colors(self, response):
        product = response.meta["product"]
        product["image_urls"].extend(self.parse_images(response))
        product['skus'].update(self.generate_skus(response))
        request = self.process_request(response.meta["colour_requests"], product)
        if request:
            yield request
        else:
            yield product

    def parse_images(self, response):
        raw_images = response.css('.productthumbnail::attr(data-lgimg)').extract()
        image_urls = [json.loads(url)["url"] for url in raw_images]
        image_urls = [url_query_cleaner(url) for url in image_urls]
        return set(image_urls)

    def generate_skus(self, response):
        common_sku = self.product_sku(response)
        skus = {}
        sizes = response.css('.size .swatchanchor.selectable::text').extract()
        colour = common_sku['colour']
        for size in sizes:
            sku = common_sku.copy()
            sku['size'] = size.strip()
            skus[colour + '_' + size.strip()] = sku
        return skus

    def product_sku(self, response):
        pricing = {}
        colour = response.css('.attribute .label::text').extract_first()
        colour = colour.split(":")[-1].strip()
        pricing['colour'] = colour
        pricing['currency'] = 'GBP'
        previous_price = response.css('.price-standard::text').extract_first()
        if previous_price:
            pricing['previous_price'] = previous_price.replace('£', '').strip()
        pricing['price'] = response.css('.price-sales::attr(content)').extract_first()
        return pricing

    def process_request(self, requests, product):
        if requests:
            request = requests.pop()
            request.meta["product"] = product
            request.meta["colour_requests"] = requests
            return request
        else:
            return
