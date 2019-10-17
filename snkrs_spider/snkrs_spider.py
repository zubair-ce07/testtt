from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from snkrs.items import SnkrsItem
from snkrs.utils import parse_gender


class SnkrsParseSpider():
    ONE_SIZE = 'oneSize'

    def parse_product(self, response):
        product = SnkrsItem()

        product['retailer_sku'] = self.get_retailer_sku(response)
        product['gender'] = self.get_gender(response)
        product['category'] = self.get_category(response)
        product['brand'] = self.get_brand(response)
        product['url'] = self.get_url(response)
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['care'] = []
        product['skus'] = self.get_skus(response)
        product['image_urls'] = self.get_image_urls(response)

        yield product 
     
    def get_retailer_sku(self, response):
        return response.css('span[itemprop="sku"]::text').get()

    def get_brand(self, response):
        return response.css('meta[itemprop="brand"]::attr(content)').get()

    def get_category(self, response):
        return response.css('span.category::text').get().split('/')

    def get_gender(self, response):        
        return parse_gender(response)

    def get_url(self, response):
        return response.url

    def get_description(self, response):        
        return response.css('div#short_description_content p::text').getall()

    def get_name(self, response):
        return response.css('h1[itemprop="name"]::text').get().split(' - ')[0]

    def get_image_urls(self, response):
        return response.css('div#carrousel_frame li a::attr(href)').getall()

    def get_skus(self, response):
        skus = {}

        colour = response.css('h1[itemprop="name"]::text').get().split(' - ')[1]
        size_css = 'span.size_EU::text, li:not(.hidden) span.units_container::text'
        price_css = 'span[itemprop="price"]::attr(content)'

        sizes = [size for size in response.css(size_css).getall() if size != ' '] or [self.ONE_SIZE]         

        for size in sizes:
            sku_attributes = {}
            availability = response.css('span.availability::text').get()            
            
            sku_attributes['previous_price'] = int(float(response.css(price_css).get())*100)
            sku_attributes['currency'] = response.css('meta[itemprop="priceCurrency"]::attr(content)').get()
            sku_attributes['out_of_stock'] = True if availability != 'InStock' else False
            sku_attributes['size'] = size
            sku_attributes['colour'] = colour
        
            skus[f'{colour}_{size}'] = sku_attributes
       
        return skus


class CrawlSpider(CrawlSpider):
    name = 'snkrs_spider'
    allowed_domains = ['snkrs.com']
    start_urls = ['http://www.snkrs.com/en/']

    listings_css = 'ul.sf-menu'
    product_css = 'div.product-container'
    
    product_parser = SnkrsParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        return self.product_parser.parse_product(response)

    def parse_start_url(self, response):
        return self.product_parser.parse_product(response)
