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

        yield from (response.follow(u, self.parse_listing) for u in
                    response.css(listing_css).extract()[1:])

    def parse_listing(self, response):
        raw_listing = self.get_raw_listing(response)

        yield from (response.follow(f"/{listing['url_key']}", self.parse_product) for listing in
                    raw_listing.values())

        next_page = response.css('#pager-next-page::attr(href)').extract_first()
        if next_page:
            return response.follow(next_page, self.parse_listing)

    @staticmethod
    def get_raw_listing(response):
        script = response.xpath('//script[contains(text(),"tkd_product_list")]').re(r'{.*}')[0]
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
        return self.fetch_next_item(variants, sku)

    def parse_product_variant(self, response):
        sku = response.meta['sku']
        variants = response.meta['variants']
        raw_product = self.get_raw_product(response)

        sku['image_urls'].extend(self.get_product_images(response))
        sku['skus'].extend(self.get_product_skus(response, raw_product))

        return self.fetch_next_item(variants, sku)

    def prepare_product_variant_request(self, variants, sku):
        request = scrapy.Request(variants.pop(), self.parse_product_variant)
        request.meta['sku'] = sku
        request.meta['variants'] = variants
        return request

    def fetch_next_item(self, variants, sku):
        if variants:
            return self.prepare_product_variant_request(variants, sku)

        return sku

    def get_product_skus(self, response, raw_product):
        skus = []

        size_drop_down = response.css('.select__menu.select__menu--pdp .select__option')
        color = self.get_product_color(response)
        currency = self.get_product_currency(response)

        if not size_drop_down:
            sku = {
                'sku_id': raw_product['product']['sku'],
                'size': 'One Size',
                'is_in_stock': bool(raw_product['product']['qty']),
                'currency': currency,
                'color': color,
                'price': int(raw_product['product']['price'] * 100)
            }

            if raw_product['product']['price'] != raw_product['product']['price_original']:
                sku['previous_price'] = [int(raw_product['product']['price_original'] * 100)]

            skus.append(sku)
            return skus

        for size_sel in size_drop_down:
            availability_xpath = './/*[contains(text(), "Ausverkauft")]'

            sku = {
                'sku_id': size_sel.css('li::attr(data-value)').extract_first(),
                'size': size_sel.css('.l-space::text').extract_first(),
                'is_in_stock': not size_sel.xpath(availability_xpath).extract(),
                'currency': currency,
                'color': color
            }

            sku.update(self.get_product_price(size_sel))
            skus.append(sku)

        return skus

    @staticmethod
    def get_product_currency(response):
        return response.css('.pdp-price strong::text').re(r'[A-Z]+')[0]

    def get_product_price(self, size_sel):
        product_price = {}

        prices = size_sel.css('li::attr(data-specialprice), li::attr(data-price)').extract()
        prices = [p.strip() for p in prices if p.strip()]

        if len(prices) > 1:
            product_price['price'] = self.get_price_from_string(prices.pop(-1))
            product_price['previous_price'] = [self.get_price_from_string(p) for p in prices]
        else:
            product_price['price'] = self.get_price_from_string(prices[0])

        return product_price

    @staticmethod
    def get_product_variants_urls(response):
        return response.css('.alternatives-list-item a::attr(href)').extract()

    def get_product_images(self, response):
        raw_images = self.get_raw_product_images(response)
        return raw_images['images']['list']

    def get_product_color(self, response):
        color = re.findall(r'in ([a-z]+)', self.get_product_name(response))

        if color:
            return color[0]

    @staticmethod
    def get_product_categories(response):
        categories = response.css('.breadcrumb__li a::text').extract()
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
        description_css = '.pdp-description-container--description p::text'
        description = response.css(description_css).extract_first()
        return [d.strip() for d in re.split(r'[.,]', description) if d.strip()]

    @staticmethod
    def get_raw_product_images(response):
        script = response.xpath('//script[contains(text(), "tkd_product")]').re(r'{.*}')[0]
        return json.loads(script)

    @staticmethod
    def get_product_care(response):
        care = response.css('.pdp-description-container--fabric_and_care li::text').extract()
        return [c for c in care[:-1] if 'Herstellerartikelnummer' not in c]

    @staticmethod
    def get_raw_product(response):
        script = response.xpath('//script[contains(text(), "master_sku")]').re(r'{.*}')[0]
        return json.loads(script)
