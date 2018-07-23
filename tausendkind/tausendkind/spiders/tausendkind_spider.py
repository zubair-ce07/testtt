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

        # ax = scrapy.Request(
        #     'https://www.tausendkind.de/zoolaboo-t-shirt-hai-gestreift-in-blau-weiss-89772001000',
        #     self.parse_product)
        ax = scrapy.Request(
            'https://www.tausendkind.de/finkid-feinstrick-beanie-kokko-in-freesia-poseidon-91764754000',
            self.parse_product)
        # ax = scrapy.Request(
        #     'https://www.tausendkind.de/zoolaboo-t-shirt-big-shark-in-dunkelblau-91811121000',
        #     self.parse_product)
        yield ax

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
            'skus': self.get_product_skus(response),
            'image_urls': self.get_product_images(response)
        }

        variants = self.get_product_variants_urls(response)

        if variants:
            request = scrapy.Request(variants.pop(), self.parse_product_variant)
            request.meta['sku'] = sku
            request.meta['variants'] = variants
            yield request
        else:
            yield sku

    def parse_product_variant(self, response):
        sku = response.meta['sku']
        variants = response.meta['variants']

        sku['image_urls'].extend(self.get_product_images(response))
        sku['skus'].extend(self.get_product_skus(response))

        if variants:
            request = scrapy.Request(variants.pop(), self.parse_product_variant)
            request.meta['sku'] = sku
            request.meta['variants'] = variants
            yield request
        else:
            yield sku

    def get_product_skus(self, response):
        skus = []

        size_drop_down = response.css('div.select__menu.select__menu--pdp li.select__option')
        color = self.get_product_name(response).split(' in ')[-1].split('/')[0]

        for row in size_drop_down:
            sku = {
                'sku_id': row.css('li::attr(data-value)').extract_first(),
                'size': row.css('div.l-space::text').extract_first(),
                'is_in_stock': not row.xpath('.//div[contains(text(), "Ausverkauft")]').extract(),
                'currency': 'EUR',
                'color': color
            }

            special_price = row.css('li::attr(data-specialprice)').extract_first()
            price = row.css('li::attr(data-price)').extract_first()

            if special_price:
                sku['price'] = self.get_price_from_string(special_price)
                sku['previous_price'] = self.get_price_from_string(price)
            else:
                sku['price'] = self.get_price_from_string(price)

            skus.append(sku)

        return skus

    @staticmethod
    def get_product_variants_urls(response):
        return response.css('div.alternatives-list-item a::attr(href)').extract()

    def get_product_images(self, response):
        raw_images = self.get_raw_product_images(response)
        return raw_images['images']['list']

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
        script = response.xpath('//script[contains(text(), "tkd_product")]').extract_first()
        raw_images = script.split('tkd_product\', ')[1].split(');')[0]
        return json.loads(raw_images)

    @staticmethod
    def get_product_care(response):
        care = response.css('div.pdp-description-container--fabric_and_care li::text').extract()
        return [c for c in care[:-1] if 'Herstellerartikelnummer' not in c]

    @staticmethod
    def get_raw_product(response):
        script = response.xpath('//script[contains(text(), "master_sku")]').extract_first()
        raw_product = script.split('= [')[1].split('];')[0]
        return json.loads(raw_product)
