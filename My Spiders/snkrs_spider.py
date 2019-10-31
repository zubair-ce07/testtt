from scrapy.spiders import Rule, CrawlSpider, Spider
from scrapy.linkextractors import LinkExtractor

from ..items import Product
from ..utils import map_gender, format_price


class SnkrsParseSpider(Spider):
    name = 'parse_spider'

    ONE_SIZE = 'oneSize'    

    def parse(self, response):       
        product = Product()
              
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
        return response.css('[itemprop="sku"]::text').get()

    def get_brand(self, response):
        return response.css('[itemprop="brand"]::attr(content)').get()

    def get_gender(self, response):
        title_text = response.css('title::text').get()
        category = self.get_category(response)
        description = self.get_description(response) 

        gender_text = f"{title_text} {' '.join(category)} {' '.join(description)}"

        return map_gender(gender_text)    

    def get_category(self, response):
        return response.css('span.category::text').get().split('/')
    
    def get_url(self, response):
        return response.url

    def get_description(self, response):        
        return response.css('#short_description_content p::text').getall()

    def get_name(self, response):
        return response.css('[itemprop="name"]::text').get().split(' - ')[0]

    def get_image_urls(self, response):
        return response.css('#carrousel_frame li a::attr(href)').getall()

    def get_price(self, response):
        current_price = response.css('[itemprop="price"]::attr(content)').get()
        previous_price = response.css('.list_price::text').get()

        return format_price(previous_price, current_price)

    def get_skus(self, response):
        skus = {}

        size_css = 'span.size_EU::text, li:not(.hidden) span.units_container::text'        
        colour = response.css('[itemprop="name"]::text').get().split(' - ')[1]
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()
        
        color_currency = {
            'colour': colour,
            'currency': currency
        }
        
        sizes = [size for size in response.css(size_css).getall() if size != ' '] or [self.ONE_SIZE]         

        for size in sizes:
            sku_attributes = {}
            availability = response.css('span.availability::text').get()            
            
            sku_attributes.update(self.get_price(response))
            sku_attributes.update(color_currency)
            sku_attributes['out_of_stock'] = availability != 'InStock'
            sku_attributes['size'] = size
                    
            skus[f'{colour}_{size}'] = sku_attributes
       
        return skus


class SnkrsCrawlSpider(CrawlSpider):       
    listings_css = 'ul.sf-menu'
    product_css = 'div.product-container'
    
    product_parser = SnkrsParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        return self.product_parser.parse(response)


class FrRegion():
    name = 'snkrs_fr'
    allowed_domains = ['snkrs.com']
    start_urls = ['https://www.snkrs.com/fr/']


class UsRegion():
    name = 'snkrs_us'
    allowed_domains = ['snkrs.com']
    start_urls = ['https://www.snkrs.com/en/']


class FrCrawlSpider(SnkrsCrawlSpider, FrRegion):
    name = f'{FrRegion.name}_crawler'


class UsCrawlSpider(SnkrsCrawlSpider, UsRegion):
    name = f'{UsRegion.name}_crawler'    


class FrParseSpider(SnkrsParseSpider, FrRegion):
    name = f'{FrRegion.name}_parser'    


class UsParseSpider(SnkrsParseSpider, UsRegion):
    name = f'{UsRegion.name}_parser'    
