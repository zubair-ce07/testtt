import json
from scrapy import Spider
from w3lib.url import url_query_cleaner as url_clean

from bonmarche.items import ProductItem


class ProductParser(Spider):

    name = "bonmarche-parse"

    def parse(self, response):
        product = ProductItem()
        product['brand'] = "bonmarche"
        product['market'] = "UK"
        product['retailer'] = "bonmarche-uk"
        product['currency'] = "GBP"
        product['gender'] = "women"
        product['retailer_sku'] = self.product_id(response)
        product['trail'] = self.product_trail(response)
        product['category'] = self.product_category(response)
        product['url'] = response.url
        product['name'] = self.product_name(response)
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['image_urls'] = self.images(response)
        product['skus'] = {}
        product['spider_name'] = self.name
        product['requests'] = self.size_requests(response)

        product['requests'] += self.color_requests(response)
        yield self.process_request(product)

    def parse_colors(self, response):
        product = response.meta["product"]
        product["image_urls"] += self.images(response)
        product['requests'] += self.size_requests(response)
        yield self.process_request(product)

    def parse_size(self, response):
        product = response.meta['product']

        if response.css('.swatches.length'):
            product['requests'] += self.length_requests(response)
            yield self.process_request(product)
        else:
            product['skus'].update(self.generate_skus(response, False))
            yield self.process_request(product)

    def parse_length(self, response):
        product = response.meta['product']
        product['skus'].update(self.generate_skus(response, True))
        yield self.process_request(product)

    def product_id(self, response):
        return response.css('::attr(data-masterid)').extract_first()

    def product_trail(self, response):
        trail_urls = response.meta.get('trail', [])
        return [[url.split("/")[-2].split(".")[0], url] for url in trail_urls]

    def product_category(self, response):
        category_css = '.breadcrumb-element [itemprop=name]::text'
        categories = response.css(category_css).extract()
        return [category.strip() for category in categories if category][1:-1]

    def product_name(self, response):
        return response.css('.xlt-pdpName::text').extract_first()

    def product_description(self, response):
        desc_css = '.product-description::text, .feature-value::text'
        description = response.css(desc_css).extract()
        return [desc.strip() for desc in description if desc][:-1]

    def product_care(self, response):
        care_css = '.product-description::text, .feature-value::text'
        return response.css(care_css).extract()[-1:]

    def parse_selected_color(self, response, product):
        product["image_urls"] += self.images(response)
        product['requests'] += self.size_requests(response)
        yield self.process_request(product)

    def color_requests(self, response):
        requests = []
        color_css = '.color .swatchanchor.selectable:not(.selected)::attr(href)'
        color_urls = response.css(color_css).extract()
        for url in color_urls:
            request = response.follow(url, callback=self.parse_colors)
            requests.append(request)
        return requests

    def images(self, response):
        images_css = '.product-image-container .productthumbnail::attr(data-lgimg)'
        raw_images = response.css(images_css).extract()
        image_urls = [url_clean(json.loads(url)["url"]) for url in raw_images]
        return image_urls

    def size_requests(self, response):
        requests = []
        size_css = '.size .swatchanchor.selectable::attr(href)'
        size_urls = response.css(size_css).extract()
        for url in size_urls:
            request = response.follow(url, callback=self.parse_size)
            requests.append(request)
        return requests

    def length_requests(self, response):
        requests = []
        length_css = '.length .swatchanchor.selectable::attr(href)'
        length_urls = response.css(length_css).extract()
        for url in length_urls:
            request = response.follow(url, callback=self.parse_length)
            requests.append(request)
        return requests

    def common_sku(self, response):
        sku = {}
        size_css = '.size .swatchanchor.selected::text'
        size = response.css(size_css).extract_first()
        sku['size'] = size.strip()
        colour = response.css('.attribute .label::text').extract_first()
        colour = colour.split(":")[-1].strip()
        sku['colour'] = colour
        sku['currency'] = 'GBP'
        previous_prices = response.css('.price-standard::text').extract()

        if previous_prices:
            sku['previous_prices'] = self.filter_prices(previous_prices)
        price = response.css('.price-sales::attr(content)').extract_first()
        sku['price'] = int(100*float(price))
        return sku

    def filter_prices(self, previous_prices):
        prices = []
        for price in previous_prices:
            price = price.replace('£', '').strip()
            if price:
                price = int(100*float(price))
                prices.append(price)
        return prices

    def generate_skus(self, response, length):
        common = self.common_sku(response)
        size = common['size']
        colour = common['colour']

        if length:
            length_css = '.length .swatchanchor.selected::text'
            length = response.css(length_css).extract_first()
            size = f'{size}/{length.strip()}'
            common['size'] = size
        return {f'{colour}_{size}': common}

    def process_request(self, product):
        if not product['requests']:
            del product['requests']
            return product
        request = product['requests'].pop()
        request.meta['product'] = product
        return request
