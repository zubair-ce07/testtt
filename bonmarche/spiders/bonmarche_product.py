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
        product['currency'] = self.product_currency(response)
        product['gender'] = "women"
        product['retailer_sku'] = self.product_id(response)
        product['trail'] = self.product_trail(response)
        product['category'] = self.product_category(response)
        product['url'] = response.url
        product['name'] = self.product_name(response)
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['image_urls'] = self.image_urls(response)
        selector = response.css('.size .swatchanchor.selected')
        product['skus'] = self.generated_skus(response) if selector else {}
        product['spider_name'] = self.name
        product['requests'] = self.size_requests(response)

        product['requests'] += self.color_requests(response)
        yield self.next_request(product)

    def parse_colors(self, response):
        product = response.meta["product"]

        if response.css('.size .swatchanchor.selected'):
            product['skus'].update(self.generated_skus(response))
        product["image_urls"] += self.image_urls(response)
        product['requests'] += self.size_requests(response)
        yield self.next_request(product)

    def parse_size(self, response):
        product = response.meta['product']

        if response.css('.swatches.length'):
            if response.css('.length .swatchanchor.selected'):
                product['skus'].update(self.generated_skus(response))
            product['requests'] += self.length_requests(response)

        else:
            product['skus'].update(self.generated_skus(response))

        yield self.next_request(product)

    def parse_length(self, response):
        product = response.meta['product']
        product['skus'].update(self.generated_skus(response))
        yield self.next_request(product)

    def product_currency(self, response):
        css = '[itemprop=priceCurrency]::attr(content)'
        return response.css(css).extract_first()

    def product_id(self, response):
        return response.css('::attr(data-masterid)').extract_first()

    def product_trail(self, response):
        return response.meta.get('trail', [])

    def product_category(self, response):
        css = '.breadcrumb-element [itemprop=name]::text'
        categories = response.css(css).extract()
        return [category.strip() for category in categories if category][1:-1]

    def product_name(self, response):
        return response.css('.xlt-pdpName::text').extract_first()

    def product_description(self, response):
        css = '.product-description::text, .feature-value::text'
        description = response.css(css).extract()
        return [desc.strip() for desc in description if desc][:-1]

    def product_care(self, response):
        css = '.product-description::text, .feature-value::text'
        return response.css(css).extract()[-1:]

    def color_requests(self, response):
        requests = []
        css = '.color .swatchanchor.selectable:not(.selected)::attr(href)'
        color_urls = response.css(css).extract()

        for url in color_urls:
            request = response.follow(url, callback=self.parse_colors)
            requests.append(request)
        return requests

    def image_urls(self, response):
        css = '.product-image-container .productthumbnail::attr(data-lgimg)'
        raw_image_urls = response.css(css).extract()
        return [url_clean(json.loads(url)["url"]) for url in raw_image_urls]

    def size_requests(self, response):
        requests = []

        if response.css('.size .swatchanchor.selected'):
            if response.css('.swatches.length'):
                requests += self.length_requests(response)

        css = '.size .swatchanchor.selectable:not(.selected)::attr(href)'
        size_urls = response.css(css).extract()

        for url in size_urls:
            request = response.follow(url, callback=self.parse_size)
            requests.append(request)
        return requests

    def length_requests(self, response):
        requests = []

        css = '.length .swatchanchor.selectable:not(.selected)::attr(href)'
        length_urls = response.css(css).extract()

        for url in length_urls:
            request = response.follow(url, callback=self.parse_length)
            requests.append(request)
        return requests

    def generated_skus(self, response):
        sku = {}

        css = '.size .swatchanchor.selected::text'
        sku['size'] = response.css(css).extract_first().strip()

        colour = response.css('.attribute .label::text').extract_first()
        sku['colour'] = colour.split(":")[-1].strip()

        sku['currency'] = 'GBP'
        previous_prices = response.css('.xlt-pdpContent .price-standard::text').extract()
        if previous_prices:
            sku['previous_prices'] = self.filter_prices(previous_prices)
        price = response.css('.price-sales::attr(content)').extract_first()
        sku['price'] = int(100 * float(price))

        if response.css('.swatches.length'):
            css = '.length .swatchanchor.selected::text'
            selected_length = response.css(css).extract_first()
            if not selected_length:
                return {}
            sku['size'] = f'{sku["size"]}/{selected_length.strip()}'

        return {f'{sku["colour"]}_{sku["size"]}': sku}

    def filter_prices(self, previous_prices):
        prices = []

        for price in previous_prices:
            price = price.replace('£', '').strip()
            if price:
                price = int(100*float(price))
                prices.append(price)
        return prices

    def next_request(self, product):
        if not product['requests']:
            del product['requests']
            return product

        request = product['requests'].pop()
        request.meta['product'] = product
        return request
