from scrapy import Spider

from ..items import ProductItem


class ProductParser(Spider):

    name = "lodenfrey-parse"

    def parse(self, response):
        if response.css('.alert-success'):
            return
        product = ProductItem()
        product['brand'] = self.product_brand(response)
        product['market'] = "GER"
        product['retailer'] = "lodenfrey-ger"
        product['currency'] = "EUR"
        product['retailer_sku'] = self.product_id(response)
        product['trail'] = self.product_trail(response)
        product['category'] = self.product_category(response)
        product['url'] = response.url
        product['name'] = self.product_name(response)
        product['description'] = self.product_description(response)
        product['care'] = self.product_care(response)
        product['gender'] = self.product_gender(response)
        product['image_urls'] = self.image_urls(response)
        product['skus'] = self.generated_skus(response)
        product['spider_name'] = self.name
        product['requests'] = self.color_requests(response)

        yield self.next_request(product)

    def parse_colors(self, response):
        product = response.meta["product"]
        product["image_urls"] += self.image_urls(response)
        product['skus'].update(self.generated_skus(response))
        yield self.next_request(product)

    def product_brand(self, response):
        return response.css('[class*=bymanu] a::text').extract_first()

    def product_id(self, response):
        p_id = response.css('#productArtnum::text').extract_first()
        return p_id.split(":")[1].strip() if p_id else None

    def product_trail(self, response):
        trail = response.meta.get('trail', [])
        return list(set(trail))

    def product_category(self, response):
        categories = response.css('.breadcrumb a::text').extract()
        return [category.strip() for category in categories if category]

    def product_name(self, response):
        return response.css('.z-product-title span::text').extract_first()

    def product_description(self, response):
        css = '.nrdetailsdesc::text, .bulletpointslist *::text, ' \
              '.nrdetailsattr *:not(#attrTitle_1):not(#attrValue_1)::text'
        description = response.css(css).extract()
        return [desc.strip() for desc in description if desc.strip()]

    def product_care(self, response):
        return response.css('#attrValue_1::text').extract()

    def product_gender(self, response):
        gender_map = ['Women', 'Men', 'Girls', 'Boys']
        soup = response.css('.breadcrumb a::text').extract()
        for gender in gender_map:
            if gender in soup:
                return gender
        return 'unisex-kids'

    def color_requests(self, response):
        requests = []
        css = '.nrColVariant a:not(.selected)::attr(href)'
        color_urls = response.css(css).extract()

        for url in color_urls:
            request = response.follow(url, callback=self.parse_colors)
            requests.append(request)
        return requests

    def image_urls(self, response):
        css = '.visible-md [class^=morePics]::attr(src)'
        return response.css(css).extract()

    def common_sku(self, response):
        sku = {}
        sku['currency'] = 'EUR'
        previous_prices = response.css('.z-oldprice del::text').extract()

        if previous_prices:
            sku['previous_prices'] = [self.filter_price(prev_price)
                                      for prev_price in previous_prices]

        price = response.css('.z-productprice ::text').extract()[-1]
        sku['price'] = self.filter_price(price)

        return sku

    def generated_skus(self, response):
        skus = {}

        css = '[class*=StdSize] a::attr(title)'
        sizes = response.css(css).extract()
        common = self.common_sku(response)

        for size in sizes:
            sku = common.copy()
            sku['size'] = size

            css = '.nrActiveColor a::attr(title)'
            sku['colour'] = response.css(css).extract_first()

            skus[f"{sku['colour']}_{size}"] = sku

        return skus

    def filter_price(self, price):
        price = price.replace('€', '').replace('.', '')
        price = price.replace(',', '.').strip()
        if price:
            price = int(100 * float(price))
        return price

    def next_request(self, product):
        if not product['requests']:
            del product['requests']
            return product

        request = product['requests'].pop()
        request.meta['product'] = product
        return request
