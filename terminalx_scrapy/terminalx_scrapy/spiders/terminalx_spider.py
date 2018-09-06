from json import loads as json_loads
from urllib.parse import urlencode
import itertools

from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor

from .terminalX_item import Garment


class TerminalXParseSpider(Spider):
    name = "terminalx-parse"
    gender_map = {
        "גברים": "men",
        "נשים": "women",
        "בנות": "girls",
        "בנים": "boys"
    }

    def parse(self, response):
        product = Garment()
        raw_product = self.get_raw_product(response)

        product["retailer_sku"] = raw_product['jsonConfig']['productId']
        product["name"] = self.get_name(response)
        product["image_urls"] = []
        product["lang"] = "he"
        product["gender"] = self.get_gender(response)
        product["category"] = self.get_categories(response)
        product["brand"] = self.get_brand(response)
        product["url"] = response.url
        product["market"] = 'IL'
        product["trail"] = response.meta.get("trail", [])
        product["retailer"] = "terminalx"
        product["url_original"] = response.url
        product["description"] = self.get_description(response)
        product["care"] = self.get_care(response)
        product["skus"] = self.get_skus(response, raw_product)
        if self.is_out_of_stock(product):
            product['out_of_stock'] = True
        response.meta["request_queue"] = self.images_requests(response, raw_product)
        response.meta["product"] = product
        return self.item_or_request(response)

    def parse_images(self, response):
        response.meta["product"]["image_urls"] += self.image_urls(response)
        return self.item_or_request(response)

    @staticmethod
    def item_or_request(response):
        if not response.meta["request_queue"]:
            return response.meta["product"]

        next_color_req = response.meta["request_queue"].pop()
        next_color_req.meta["product"] = response.meta["product"]
        next_color_req.meta["request_queue"] = response.meta["request_queue"]
        return next_color_req

    def get_skus(self, response, product_config):
        skus = {}
        common_sku = self.get_common_sku(response, product_config)
        raw_skus = self.get_raw_skus(product_config)
        available_skus = product_config['jsonConfig']['index']

        for color, size in raw_skus:
            sku = common_sku.copy()
            sku['colour'] = color[1]['label']
            sku['size'] = size[1]['label'] if size[1]['label'] is not "OneSize" else "One Size"

            if not self.is_available(color, size, available_skus):
                sku['out_of_stock'] = True

            skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus

    def get_common_sku(self, response, product_config):
        common_sku = {}
        old_price = float(product_config['jsonConfig']['prices']['oldPrice']['amount'])
        common_sku["price"] = float(product_config['jsonConfig']['prices']['finalPrice']['amount'])
        common_sku["price"] = self.cents_conversion(common_sku["price"])
        common_sku["currency"] = self.get_currency(response)

        if old_price != common_sku["price"]:
            common_sku["previous_prices"] = [self.cents_conversion(old_price)]

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

        if not raw_gender:
            return "unisex-adults"

        for key, value in self.gender_map.items():
            if key in raw_gender:
                return value

        return "unisex-adults"

    @staticmethod
    def get_brand(response):
        return response.css('.product-item-brand::text').extract_first().strip()

    @staticmethod
    def get_categories(response):
        breadcrumbs = response.css('.breadcrumbs .item>a::text').extract()
        return [item.strip() for item in breadcrumbs[1:-2]]

    @staticmethod
    def get_care(response):
        care = response.css('#technical:not(p:last-of-type) ::text').extract()
        return [line.strip() for line in care if line.strip()]

    @staticmethod
    def get_raw_product(response):
        raw_config = response.css('script:contains("swatch-options")::text').extract_first()
        return json_loads(raw_config)['[data-role=swatch-options]']['IdusClass_ProductList/js/swatch-renderer']

    @staticmethod
    def get_currency(response):
        if response.css('span.price:contains("₪")'):
            return 'ILS'

    def images_requests(self, response, product_config):
        url = 'https://www.terminalx.com/swatches/ajax/media/'
        params = {
            'product_id': product_config['jsonConfig']['productId'],
        }

        media_reqs = []
        for colour_code in product_config['jsonSwatchConfig']['93'].keys():
            params['attributes[color]'] = colour_code
            media_reqs.append(response.follow(f'{url}?{urlencode(params)}', callback=self.parse_images))

        return media_reqs

    @staticmethod
    def is_available(color, size, available_skus):
        if not available_skus:
            return False

        for sku in available_skus.values():
            if sku['93'] == color[0] and sku['149'] == size[0]:
                return True

        return False

    @staticmethod
    def image_urls(response):
        images = json_loads(response.body)['gallery']
        return [image['large'] for image in images.values()]

    @staticmethod
    def get_description(response):
        return response.css('.description p ::text').extract()

    def cents_conversion(self, param):
        return 100 * param

    def is_out_of_stock(self, product):
        return all(sku.get('out_of_stock', False) for sku in product['skus'].items())


class TerminalXCrawlSpider(CrawlSpider):
    name = "terminalx-crawl"
    parser = TerminalXParseSpider()
    start_urls = [
        'https://www.terminalx.com/'
    ]
    allowed_domains = [
        'terminalx.com'
    ]

    product_css = ['.product-items']
    listing_css = ['.level2', '.pages-item-next']
    rules = (Rule(LinkExtractor(restrict_css=product_css), callback="parse_product"),
             Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             )

    def parse(self, response):
        for request in super(TerminalXCrawlSpider, self).parse(response):
            request.meta["trail"] = self.add_trail(response)
            yield request

    def parse_product(self, response):
        return self.parser.parse(response)

    def add_trail(self, response):
        trail_part = [response.url]
        return response.meta.get('trail', []) + trail_part
