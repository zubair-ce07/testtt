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
        color_urls = response.css('.color .swatchanchor.selectable:not(.selected)::attr(href)').extract()
        color_urls.append(response.url)
        requests = [Request(url, callback=self.parse_size) for url in color_urls]
        return requests

    def parse_colors(self, response):
        requests = response.meta['colour_requests']
        product = response.meta["product"]
        product["image_urls"] += self.images(response)
        size_urls = response.css('.size .swatchanchor.selectable::attr(href)').extract()
        requests += [Request(url, callback=self.parse_size) for url in size_urls]
        request = self.process_request(requests, product)
        if request:
            yield request
        else:
            yield product

    def images(self, response):
        raw_images = response.css('.productthumbnail::attr(data-lgimg)').extract()
        image_urls = [url_query_cleaner(json.loads(url)["url"]) for url in raw_images]
        return set(image_urls)

    def parse_size(self, response):
        product = response.meta['product']
        common = self.common_sku(response)
        skus = {}
        size = response.css('.size .swatchanchor.selectable.selected::text').extract_first()
        colour = common['colour']
        sku = common.copy()
        length_urls = response.css('.length .swatchanchor.selectable::attr(href)').extract()
        if length_urls:
            requests = response.meta['colour_requests']
            requests += [Request(url, callback=self.parse_length) for url in length_urls]
            request = self.process_request(requests, product)
            if request:
                yield request
            else:
                yield product
        else:
            sku['size'] = size.strip()
            skus[f'{colour}_{size.strip()}'] = sku
        product['skus'].update(skus)
        request = self.process_request(response.meta["colour_requests"], product)
        if request:
            yield request
        else:
            yield product

    def parse_length(self, response):
        product = response.meta['product']
        common = self.common_sku(response)
        skus = {}
        size = response.css('.size .swatchanchor.selectable.selected::text').extract_first()
        colour = common['colour']
        sku = common.copy()
        lengths = response.css('.length .swatchanchor.selectable::text').extract()
        for length in lengths:
            filtered_size = f'{size.strip()}/{length.strip()}'
            sku['size'] = filtered_size
            skus[f'{colour}_{filtered_size}'] = sku
        product['skus'].update(skus)
        request = self.process_request(response.meta["colour_requests"], product)
        if request:
            yield request
        else:
            yield product

    def common_sku(self, response):
        sku = {}
        colour = response.css('.attribute .label::text').extract_first()
        colour = colour.split(":")[-1].strip()
        sku['colour'] = colour
        sku['currency'] = 'GBP'
        previous_price = response.css('.price-standard::text').extract_first()

        if previous_price:
            sku['previous_price'] = previous_price.replace('£', '').strip()
        sku['price'] = response.css('.price-sales::attr(content)').extract_first()
        return sku

    def process_request(self, requests, product):
        if not requests:
            return
        request = requests.pop()
        request.meta["product"] = product
        request.meta["colour_requests"] = requests
        return request

