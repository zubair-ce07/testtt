from json import loads as json_loads
from urllib.parse import urlencode
import itertools

from scrapy import Spider


class Parser(Spider):
    name = "parser"
    possible_genders = {
        "גברים": "men",
        "נשים": "women",
        "בנות": "girls",
        "בייבי בנות": "girls",
        "בנים": "boys",
        'בייבי בנים': "boys"
    }

    def parse(self, response):
        product = {}
        product_config = self.get_product_config(response)
        product_data = self.get_product_data(response)

        product["retailer_sku"] = product_config['jsonConfig']['productId']
        product["name"] = self.get_name(response)
        product["image_urls"] = []
        product["lang"] = "he"
        product["gender"] = self.get_gender(response)
        product["category"] = self.get_categories(response)
        product["industry"] = None
        product["brand"] = self.get_brand(response)
        product["url"] = response.url
        product["market"] = 'IL'
        product["trail"] = response.meta["trail"]
        product["retailer"] = "terminalx"
        product["url_original"] = response.url
        product["description"] = product_data['description']
        product["care"] = self.get_care(response)
        product["skus"] = self.get_skus(response, product_config)
        response.meta["pending_media_reqs"] = self.media_requests(response, product_config)
        response.meta["product"] = product
        return self.item_or_request(response)

    def parse_images(self, response):
        gallery = json_loads(response.body)['gallery']
        response.meta["product"]["image_urls"] += [image['large'] for image in gallery.values()]
        return self.item_or_request(response)

    @staticmethod
    def item_or_request(response):

        if not response.meta["pending_media_reqs"]:
            return response.meta["product"].copy()

        next_color_req = response.meta["pending_media_reqs"].pop()
        next_color_req.meta["product"] = response.meta["product"].copy()
        next_color_req.meta["pending_media_reqs"] = response.meta["pending_media_reqs"].copy()
        return next_color_req

    def get_skus(self, response, product_config):
        skus = {}
        sku_prefix = product_config['jsonConfig']['productId']
        common_sku = self.get_common_sku(response, product_config)
        raw_skus = self.get_raw_skus(product_config)
        available_skus = product_config['jsonConfig']['index']

        for raw_sku in raw_skus:
            sku = common_sku.copy()
            sku['colour'] = raw_sku[0][1]['label']
            sku['size'] = raw_sku[1][1]['label'] if raw_sku[1][1]['label'] is not "OneSize" else "One Size"

            availablity = self.is_available(raw_sku, available_skus)
            if not availablity:
                sku['out_of_stock'] = True

            skus[f'{sku_prefix}_{sku["colour"]}_{sku["size"]}'] = sku

        return skus

    def get_common_sku(self, response, product_config):
        common_sku = {}
        old_price = product_config['jsonConfig']['prices']['oldPrice']['amount']

        common_sku["price"] = product_config['jsonConfig']['prices']['finalPrice']['amount']
        common_sku["currency"] = self.get_product_data(response)['offers']['priceCurrency']

        if old_price is not common_sku["price"]:
            common_sku["previous_prices"] = [old_price]

        return common_sku

    @staticmethod
    def get_raw_skus(product_config):
        colors_variants = product_config['jsonSwatchConfig']['93'].items()
        size_variants = product_config['jsonSwatchConfig']['149'].items()
        return itertools.product(colors_variants, size_variants)

    @staticmethod
    def get_name(response):
        return response.css('.attribute_name::text').extract_first().strip()

    def get_gender(self, response):
        raw_gender = response.css('.product-sizechart-wrapper>a::attr(title)').extract_first()
        return self.possible_genders[raw_gender.split('/').pop().strip()] if raw_gender else "unisex-adults"

    @staticmethod
    def get_brand(response):
        return response.css('.product-item-brand::text').extract_first().strip()

    @staticmethod
    def get_categories(response):
        breadcrumbs = response.css('.breadcrumbs >.item:not(.product)::text').extract()
        return [item.strip() for item in breadcrumbs if 'דף הבית' not in item]

    @staticmethod
    def get_care(response):
        care = response.css('#technical:not(p:last-of-type) ::text').extract()
        return [line.strip() for line in care if line.strip()]

    @staticmethod
    def get_product_config(response):
        raw_config = response.css('script[type="text/x-magento-init"]:contains("swatch-options")::text').extract_first()
        return json_loads(raw_config)['[data-role=swatch-options]']['IdusClass_ProductList/js/swatch-renderer']

    @staticmethod
    def get_product_data(response):
        return json_loads(response.css('script[type="application/ld+json"]::text').extract_first())

    def media_requests(self, response, product_config):
        url = product_config['mediaCallback']
        params = {
            'product_id': product_config['jsonConfig']['productId'],
            'isAjax': True
        }

        media_reqs = []
        for colour_code in product_config['jsonSwatchConfig']['93'].keys():
            params['attributes[color]'] = colour_code
            media_reqs.append(response.follow(f'{url}?{urlencode(params)}', callback=self.parse_images))

        return media_reqs

    @staticmethod
    def is_available(raw_sku, available_skus):
        if not available_skus:
            return False

        for sku in available_skus.values():
            if sku['93'] == raw_sku[0][0] and sku['149'] == raw_sku[1][0]:
                return True

        return False
