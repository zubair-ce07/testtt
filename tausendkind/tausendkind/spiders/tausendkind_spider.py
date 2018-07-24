import re
import json

import scrapy


class TausendkindSpider(scrapy.Spider):
    name = "tausendkind"
    start_urls = [
        'https://www.tausendkind.de/'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    allowed_domains = [
        'tausendkind.de'
    ]

    def parse(self, response):
        listing_css = '#main-menu a::attr(href)'

        for url in response.css(listing_css).extract()[1:]:
            yield response.follow(url, self.parse_listing)

    def parse_listing(self, response):
        raw_listing = self.get_raw_listing(response)

        for listing in raw_listing.values():
            yield response.follow(f"/{listing['url_key']}", self.parse_product)

        next_page = response.css('#pager-next-page::attr(href)').extract_first()
        if next_page:
            return response.follow(next_page, self.parse_listing)

    @staticmethod
    def get_raw_listing(response):
        script = response.xpath('//div/script[contains(text(),"DOMContentLoaded")]').re(r'{.*}')[0]
        return json.loads(script)['list']

    def parse_product(self, response):
        raw_product = self.get_raw_product(response)

        sku = {
            'retailer_sku': self.get_product_retailer_sku(raw_product),
            'name': self.get_product_name(response),
            'brand': self.get_product_brand(raw_product),
            'gender': self.get_product_gender(raw_product),
            'category': self.get_product_categories(response),
            'url': response.url,
            'description': self.get_product_description(response),
            'care': self.get_product_care(response),
            'skus': self.get_product_skus(response, raw_product),
            'image_urls': self.get_product_images(response)
        }

        variants = self.get_product_variants_urls(response)

        if variants:
            return self.prepare_product_variant_request(variants, sku)

        return sku

    def parse_product_variant(self, response):
        sku = response.meta['sku']
        variants = response.meta['variants']
        raw_product = self.get_raw_product(response)

        sku['image_urls'].extend(self.get_product_images(response))
        sku['skus'].extend(self.get_product_skus(response, raw_product))

        if variants:
            return self.prepare_product_variant_request(variants, sku)

        return sku

    def prepare_product_variant_request(self, variants, sku):
        request = scrapy.Request(variants.pop(), self.parse_product_variant)
        request.meta['sku'] = sku
        request.meta['variants'] = variants
        return request

    def get_product_skus(self, response, raw_product):
        skus = []

        size_drop_down = response.css('div.select__menu.select__menu--pdp li.select__option')
        color = self.get_product_color(response)

        if not size_drop_down:
            sku = {
                'sku_id': raw_product['product']['sku'],
                'size': 'One Size',
                'is_in_stock': bool(raw_product['product']['qty']),
                'currency': 'EUR',
                'color': color,
                'price': raw_product['product']['price'] * 100
            }

            skus.append(sku)
            return skus

        for row in size_drop_down:
            sku = {
                'sku_id': row.css('li::attr(data-value)').extract_first(),
                'size': row.css('div.l-space::text').extract_first(),
                'is_in_stock': not row.xpath('.//div[contains(text(), "Ausverkauft")]').extract(),
                'currency': 'EUR',
                'color': color
            }

            sku.update(self.get_product_price(row))
            skus.append(sku)

        return skus

    def get_product_price(self, row):
        product_price = {}

        special_price = row.css('li::attr(data-specialprice)').extract_first()
        price = row.css('li::attr(data-price)').extract_first()

        if special_price:
            product_price['price'] = self.get_price_from_string(special_price)
            product_price['previous_price'] = self.get_price_from_string(price)
        else:
            product_price['price'] = self.get_price_from_string(price)

        return product_price

    @staticmethod
    def get_product_variants_urls(response):
        return response.css('div.alternatives-list-item a::attr(href)').extract()

    def get_product_images(self, response):
        raw_images = self.get_raw_product_images(response)
        return raw_images['images']['list']

    def get_product_color(self, response):
        color = re.search(r'(in )([a-z]+)', self.get_product_name(response))

        if color:
            return color.group(2)

    @staticmethod
    def get_product_categories(response):
        categories = response.css('li.breadcrumb__li a::text').extract()
        return {c.strip() for c in categories[1:] if c.strip()}

    @staticmethod
    def get_product_retailer_sku(raw_product):
        return raw_product['product']['master_sku']

    @staticmethod
    def get_product_gender(raw_product):
        gender_map = {'junge': 'boys', 'maedchen': 'girls'}
        gender = raw_product['product']['filter_gender']
        if all(g in gender for g in gender_map.keys()):
            return 'unisex'
        return gender_map.get(gender)

    @staticmethod
    def get_product_brand(raw_product):
        return raw_product['product']['manufacturer_name']

    @staticmethod
    def get_product_name(response):
        return response.css('#product-name::text').extract_first()

    @staticmethod
    def get_price_from_string(string):
        price = re.findall(r'\d+,?\d+', string)[0]
        return int(float(price.replace(',', '.')) * 100)

    @staticmethod
    def get_product_description(response):
        description = response.css(
            'div.pdp-description-container--description p::text').extract_first()
        return [d.strip() for d in re.split(r'[.,]', description) if d.strip()]

    @staticmethod
    def get_raw_product_images(response):
        script = response.xpath('//script[contains(text(), "tkd_product")]').re(r'{.*}')[0]
        return json.loads(script)

    @staticmethod
    def get_product_care(response):
        care = response.css('div.pdp-description-container--fabric_and_care li::text').extract()
        return [c for c in care[:-1] if 'Herstellerartikelnummer' not in c]

    @staticmethod
    def get_raw_product(response):
        script = response.xpath('//script[contains(text(), "master_sku")]').re(r'{.*}')[0]
        return json.loads(script)
