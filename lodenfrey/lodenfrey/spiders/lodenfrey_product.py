from scrapy import Spider

from ..items import ProductItem


class ProductParser(Spider):

    name = "lodenfrey-parse"

    def parse(self, response):
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
        product['image_urls'] = self.images(response)
        product['skus'] = self.generated_skus(response)
        product['spider_name'] = self.name
        product['requests'] = self.color_requests(response)

        yield self.next_request(product)

    def parse_colors(self, response):
        product = response.meta["product"]
        product["image_urls"] += self.images(response)
        product['skus'].update(self.generated_skus(response))
        yield self.next_request(product)

    def product_brand(self, response):
        return response.css('[class*=bymanu] a::text').extract_first()

    def product_id(self, response):
        p_id = response.css('#productArtnum::text').extract_first()
        return p_id.split(":")[1].strip() if p_id else None

    def product_trail(self, response):
        return response.meta.get('trail', [])

    def product_category(self, response):
        categories = response.css('.breadcrumb a::text').extract()
        return [category.strip() for category in categories if category]

    def product_name(self, response):
        return response.css('.z-product-title span::text').extract_first()

    def product_description(self, response):
        desc_selector = '.nrdetailsdesc::text, .bulletpointslist *::text, ' \
                        '.nrdetailsattr *:not(#attrTitle_1):not(#attrValue_1)::text'
        description = response.css(desc_selector).extract()
        return [desc.strip() for desc in description if desc.strip()]

    def product_care(self, response):
        care_selector = '#attrValue_1::text'
        return response.css(care_selector).extract()

    def product_gender(self, response):
        gender_map = ['Women', 'Men', 'Girls', 'Boys']
        soup = response.css('.breadcrumb a::text').extract()
        for gender in gender_map:
            if gender in soup:
                return gender
        return 'unisex-kids'

    def color_requests(self, response):
        requests = []
        color_selector = '.nrColVariant a:not(.selected)::attr(href)'
        color_urls = response.css(color_selector).extract()

        for url in color_urls:
            request = response.follow(url, callback=self.parse_colors)
            requests.append(request)
        return requests

    def images(self, response):
        images_selector = '.visible-md [class^=morePics]::attr(src)'
        return response.css(images_selector).extract()

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

        size_selector = '[class*=StdSize] a::attr(title)'
        sizes = response.css(size_selector).extract()
        common = self.common_sku(response)

        for size in sizes:
            sku = common.copy()
            sku['size'] = size

            colour_selector = '.nrActiveColor a::attr(title)'
            colour = response.css(colour_selector).extract_first()
            sku['colour'] = colour

            skus[f'{colour}_{size}'] = sku

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
