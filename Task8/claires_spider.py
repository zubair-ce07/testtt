from scrapy.spiders import Rule, Request
from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class MixinUK:
    retailer = 'claires-uk'
    market = 'UK'
    default_brand = 'claires'
    gender = 'girls'
    unwanted_categories = ['tech', 'toys', 'stationery']
    allowed_domains = ['claires.com']
    start_urls = ['https://www.claires.com/?lang=en_GB']


class ParseSpider(BaseParseSpider):
    raw_description_css = '.tab-content *::text'
    price_css = '.product-detail .product-price *::text'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        category = self.product_category(response)

        if not garment or self.is_unwanted_item(category):
            return

        self.boilerplate_normal(garment, response)
        garment['category'] = category
        garment['image_urls'] = self.image_urls(response)

        size_requests = self.size_requests(response)
        garment['meta'] = {'requests_queue': size_requests}

        garment['skus'] = {} if size_requests else self.skus(response)

        return self.next_request_or_garment(garment)

    def is_unwanted_item(self, categories):
        for category in categories:
            if any(unwanted_item in category.lower() for unwanted_item in MixinUK.unwanted_categories):
                return True

        return False

    def parse_skus(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def size_requests(self, response):
        sizes = response.css('.swatches a::attr(href)').extract()
        return [Request(size, callback=self.parse_skus) for size in sizes]

    def product_id(self, response):
        return response.css('#pid::attr(value)').extract_first()

    def product_name(self, response):
        return response.css('.product-detail h1::text').extract_first()

    def product_category(self, response):
        return response.css('.breadcrumb a::text').extract()[1:]

    def image_urls(self, response):
        css = '.product-thumbnails li a::attr(href), .product-image::attr(href)'
        return response.css(css).extract()

    def skus(self, response):
        skus = {}

        sku = self.product_pricing_common(response)

        size = response.css('.size .selected a::text').extract_first()
        sku['size'] = clean(size) if size else "One_Size"

        sku_id = f'{self.product_id(response)}_{sku["size"]}'

        stock_availability = response.css('.availability-msg p::text').extract_first()

        if stock_availability.lower() == "out of stock":
            sku['out_of_stock'] = True

        skus[sku_id] = sku

        return skus


class CrawlSpider(BaseCrawlSpider, MixinUK):
    listings_css = ['a.has-sub-menu',
                    '.clp-shopby-categories',
                    '.page-next'
    ]

    product_css = ['.name-link']
    deny = ['/whats-hot', '/all']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )


class ClairesUKParseSpider(ParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class ClairesUKCrawlSpider(CrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = ClairesUKParseSpider()
