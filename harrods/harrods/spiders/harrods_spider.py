import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity


class Product(scrapy.Item):
    url = scrapy.Field()
    code = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    previous_price = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    availability = scrapy.Field()
    image_urls = scrapy.Field()
    website_name = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    @staticmethod
    def sanitize_currency(currency):
        return currency[0].strip()

    @staticmethod
    def fetch_categories(categories):
        return categories[1:]

    @staticmethod
    def fetch_images(image_urls):
        return [f'https://{url}' for url in image_urls]

    @staticmethod
    def fetch_price(prices):
        return min(prices)

    currency_in = sanitize_currency
    categories_in = fetch_categories
    image_urls_in = fetch_images
    price_in = fetch_price

    categories_out = Identity()
    image_urls_out = Identity()


class HarrodsParser(scrapy.Spider):
    name = "harrods_parser"

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        product_loader = ProductLoader(item=Product(), response=response)

        product_loader.add_css('code', '.js-buying-control-prodID::text', re=r'\d+')
        product_loader.add_css('brand', '[itemprop="brand"] span::text')
        product_loader.add_css('name', '.buying-controls_name::text')
        product_loader.add_css('price', '.js-buying-controls_price .price_group--was'
                                        ' .price_amount::text, .price_amount::text')
        product_loader.add_css('currency', '.price_currency::text')
        product_loader.add_css('description', '[itemprop="description"] p::text')
        product_loader.add_css('categories', '.breadcrumb_link [itemprop="name"]::text')
        product_loader.add_css('image_urls',
                               '.pdp_images-image--primary::attr(src)', re=r'//(.*)\?')
        product_loader.add_css('previous_price',
                               '.js-buying-controls_price .price_group--was .price_amount::text')
        product_loader.add_value('website_name', 'Harrods')
        product_loader.add_value('url', response.url)
        product_loader.add_value('availability',
                                 bool(response.css('.buying-controls_label--quantity')))

        return product_loader.load_item()


class HarrodsCrawler(CrawlSpider):
    name = "harrods"
    product_parser = HarrodsParser()

    rules = (
        Rule(LinkExtractor(restrict_css=['.nav_sub-menu-item', '.control_paging-item--next'])),
        Rule(LinkExtractor(restrict_css=['.js-product-card']), callback='parse_product'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    allowed_domains = [
        'harrods.com'
    ]

    start_urls = [
        'https://www.harrods.com/en-gb'
    ]

    def start_requests(self):
        form_data = {
            'CountryCode': 'SG',
            'ddlItemCheckboxddlm0l9': '55',
            'CurrencyCode': 'SGD',
            'ddlItemCheckboxddlm2o0': '55'
        }

        yield scrapy.FormRequest('https://www.harrods.com/en-gb/countrycurrencyselector',
                                 formdata=form_data, callback=self.parse_cookies)

    def parse_cookies(self, response):
        yield from super().start_requests()

    def parse_product(self, response):
        return self.product_parser.parse(response)
