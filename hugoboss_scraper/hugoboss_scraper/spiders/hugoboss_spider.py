import json

from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner

from .hugoboss_item import Garment


class HugobossParseSpider(Spider):
    name = "hugoboss-parser"
    scraped_ids = set()

    def parse(self, response):
        product = Garment()
        raw_product = self.get_raw_product(response)

        if self.id_exists(raw_product["id"]):
            return

        product["retailer_sku"] = raw_product["id"]
        product["name"] = raw_product["name"] or ""
        product["image_urls"] = self.get_image_urls(response)
        product["lang"] = "en"
        product["gender"] = raw_product["gender"]
        product["category"] = self.get_categories(response)
        product["brand"] = raw_product["brand"]
        product["url"] = response.url
        product["market"] = "US"
        product["trail"] = response.meta["trail"]
        product["retailer"] = "hugoboss"
        product["url_original"] = response.url
        product["description"] = self.get_description(response)
        product["care"] = self.get_care(response)
        product["skus"] = self.get_skus(response)
        response.meta["request_queue"] = self.colour_requests(response)
        response.meta["product"] = product
        return self.item_or_request(response)

    def parse_colour(self, response):
        response.meta["product"]["skus"].update(self.get_skus(response))
        response.meta["product"]["image_urls"] += self.get_image_urls(response)
        return self.item_or_request(response)

    def item_or_request(self, response):

        if not response.meta["request_queue"]:
            product = response.meta["product"]
            if self.is_out_of_stock(product):
                product['out_of_stock'] = True
            return product

        next_color_req = response.meta["request_queue"].pop()
        next_color_req.meta["product"] = response.meta["product"]
        next_color_req.meta["request_queue"] = response.meta["request_queue"]
        return next_color_req

    def get_skus(self, response):
        skus = {}
        product_data = self.get_raw_product(response)
        sku_variant = product_data["variant"]
        sizes_s = response.css('.swatch-list__size')
        common_sku = self.get_common_sku(response, product_data)

        if not sizes_s:
            skus[f"{sku_variant}_One Size"] = common_sku
            skus[f"{sku_variant}_One Size"]["size"] = "One Size"
            return skus

        for size in sizes_s:
            sku = common_sku.copy()
            sku["size"] = size.css('::text').extract_first().strip()
            if size.css('[class*="unselectable"]'):
                sku["out_of_stock"] = True
            skus[f'{sku_variant}_{sku["size"]}'] = sku

        return skus

    def get_common_sku(self, response, product_data):
        common_sku = {}

        discount = product_data["metric3"]
        if discount:
            common_sku["previous_prices"] = [self.cents_conversion(product_data["price"] + discount)]

        common_sku["price"] = self.cents_conversion(product_data["price"])
        common_sku["currency"] = self.get_currency(response)
        common_sku["colour"] = self.get_colour(response)
        return common_sku

    @staticmethod
    def get_currency(response):
        return response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first()

    @staticmethod
    def get_colour(response):
        variation = response.css('.product-variations::attr(data-current)').extract_first()
        return json.loads(variation)["color"]["displayValue"]

    @staticmethod
    def get_categories(response):
        unique_breadcrumbs = set(response.css('.breadcrumb__link::attr(title)').extract())
        return list(unique_breadcrumbs)[1:]

    @staticmethod
    def get_image_urls(response):
        image_urls = response.css('img.slider-item__image::attr(src)').extract()
        return [url_query_cleaner(url) for url in image_urls]

    @staticmethod
    def get_description(response):
        description = response.css('div.product-container__text__description::text').extract_first(default='')
        return [line.strip() for line in description.strip().split('.\n')]

    @staticmethod
    def get_care(response):
        material_care = response.css('.materialCare>.product-container__text::text').extract_first()
        material_care = material_care.strip().split(", ") if material_care else []
        return material_care + response.css('.accordion__care-icon__text::text').extract()

    @staticmethod
    def get_raw_product(response):
        raw_product = response.css('div[data-as-product]::attr(data-as-product)').extract_first()
        raw_product.replace('&quot;', '"')
        return json.loads(raw_product)

    def colour_requests(self, response):
        colour_urls = response.css('.swatch-list__button--is-empty>a::attr(href)').extract()

        colour_reqs = [response.follow(url_query_cleaner(url), callback=self.parse_colour, dont_filter=True)
                       for url in colour_urls]

        return colour_reqs

    def id_exists(self, product_id):
        if product_id in self.scraped_ids:
            return True
        self.scraped_ids.add(product_id)
        return False

    def is_out_of_stock(self, product):
        return all(sku.get('out_of_stock', False) for sku in product['skus'].values())

    def cents_conversion(self, param):
        return 100 * param


class HugobossCrawlSpider(CrawlSpider):
    name = "hugoboss-crawl"
    parser = HugobossParseSpider()

    start_urls = [
        'https://www.hugoboss.com/us/'
    ]

    allowed_domains = [
        'hugoboss.com'
    ]

    product_css = ['.swatch-list__image']
    listing_css = ['.nav-list--third-level', '.pagingbar__item']

    rules = (Rule(LinkExtractor(restrict_css=product_css, process_value=url_query_cleaner),
                  callback="parse_product"),
             Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             )

    def parse(self, response):
        for request in super(HugobossCrawlSpider, self).parse(response):
            request.meta["trail"] = self.add_trail(response)
            yield request

    def parse_product(self, response):
        return self.parser.parse(response)

    def add_trail(self, response):
        trail_part = [response.url]
        return response.meta.get('trail', []) + trail_part
