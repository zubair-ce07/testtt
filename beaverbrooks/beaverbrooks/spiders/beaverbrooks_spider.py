from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from beaverbrooks.itemloaders import ProductLoader
from beaverbrooks.items import Product


class BeaverbrooksSpider(CrawlSpider):
    """
    BeaverbrooksSpider crawls the provided urls to get all the available
    products and their details
    """

    name = 'beaverbrooks'
    start_urls = [
        'https://www.beaverbrooks.co.uk'
    ]
    css_rules = [
        '.list-pagination__nav-arrow',
        '.main-nav__item--has-children'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css='.product-list__item'), callback='parse_product'),
        Rule(LinkExtractor(restrict_css=css_rules)),
    )

    def parse_product(self, response):
        product_loader = ProductLoader(item=Product(), response=response)
        product_loader.add_css('product_image', '.product-image img::attr("src")')
        product_loader.add_css('product_title', '#productName::text')
        product_loader.add_css('product_offer_price', '.product-offer__price::text')
        product_loader.add_css('product_offer_per_month', '.product-panel__finance-cta-section-container strong::text')
        product_loader.add_css('product_specification', '.product-specification tr')
        product_loader.add_css('product_code', '[itemprop="sku"]::attr("content")')
        yield product_loader.load_item()
