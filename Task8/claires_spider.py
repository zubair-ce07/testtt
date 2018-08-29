from scrapy.spiders import Rule, Request
from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean


class MixinUK:
    retailer = 'claires-uk'
    market = 'UK'
    currency = 'GBP'
    lang = 'en'
    default_brand = 'claires'
    unwanted_items = ['tech', 'toys', 'stationery']
    allowed_domains = ['claires.com']
    start_urls = ['https://www.claires.com/?lang=en_GB']


class ParseSpider(BaseParseSpider):
    raw_description_css = '.tab-content *::text'
    price_css = '.product-detail .price-sales::text'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        category = self.product_category(response)

        if not garment or self.is_unwanted_item(category):
            return

        self.boilerplate_normal(garment, response)
        garment['category'] = category
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['merch_info'] = self.merch_info(response)

        size_requests = self.size_requests(response)
        garment['meta'] = {'requests_queue': size_requests}

        garment['skus'] = {} if size_requests else self.one_size_sku(response)

        return self.next_request_or_garment(garment)

    def is_unwanted_item(self, categories):
        for category in categories:
            if any(unwanted_item in category.lower() for unwanted_item in MixinUK.unwanted_items):
                return True

        return False

    def product_id(self, response):
        return response.css('#pid::attr(value)').extract_first()

    def product_name(self, response):
        return response.css('.product-detail h1::text').extract_first()

    def product_category(self, response):
        return response.css('.breadcrumb a::text').extract()[1:]

    def merch_info(self, response):
        return clean(response.css('.product-detail .callout-message::text').extract()[:1])

    def product_gender(self, response):
        return response.meta.get('gender')

    def image_urls(self, response):
        return response.css('.product-thumbnails li a::attr(href)').extract() \
               or response.css('.product-image::attr(href)').extract()

    def is_out_of_stock(self, response):
        stock_availability = response.css('.availability-msg p::text').extract_first().lower()
        return stock_availability == 'out of stock'

    def parse_skus(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def size_requests(self, response):
        sizes = response.css('.swatches a::attr(href)').extract()
        return [Request(size, callback=self.parse_skus) for size in sizes]

    def skus(self, response):
        skus = {}

        sku = self.product_pricing_common(response)
        sku['size'] = clean(response.css('.selected a::text').extract_first())
        sku_id = f'{self.product_id(response)}_{sku["size"]}'

        if self.is_out_of_stock(response):
            sku['out_of_stock'] = True

        skus[sku_id] = sku

        return skus

    def one_size_sku(self, response):
        skus = {}

        sku = self.product_pricing_common(response)
        sku['size'] = 'One_Size'
        sku_id = f'{self.product_id(response)}_{sku["size"]}'

        if self.is_out_of_stock(response):
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
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse_and_add_girls'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )


class ClairesUKParseSpider(ParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class ClairesUKCrawlSpider(CrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = ClairesUKParseSpider()
