from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import Product
from ..utils import map_gender, format_price


class MixinFR():
    name = 'snkrs_fr'
    allowed_domains = ['snkrs.com']
    start_urls = ['https://www.snkrs.com/fr/']


class MixinUS():
    name = 'snkrs_us'
    allowed_domains = ['snkrs.com']
    start_urls = ['https://www.snkrs.com/en/']


class SnkrsParseSpider():
    ONE_SIZE = 'oneSize'
    ONE_COLOUR = 'oneColour'    

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

        return product 
     
    def get_retailer_sku(self, response):
        return response.css('[itemprop="sku"]::text').get()

    def get_brand(self, response):
        return response.css('[itemprop="brand"]::attr(content)').get()

    def get_gender(self, response):
        title_text = response.css('title::text').get()
        category = self.get_category(response)
        description = self.get_description(response) 

        gender_soup = ' '.join(category + description) + title_text
        return map_gender(gender_soup)    

    def get_category(self, response):
        return response.css('span.category::text').get().split('/')
    
    def get_url(self, response):
        return response.url

    def get_description(self, response):        
        return response.css('#short_description_content p::text').getall()

    def get_name(self, response):
        return response.css('[itemprop="name"]::text').get()

    def get_image_urls(self, response):
        return response.css('#carrousel_frame li a::attr(href)').getall()

    def get_price(self, response):
        current_price = response.css('[itemprop="price"]::attr(content)').get()
        previous_price = response.css('#old_price_display .price::text').re_first(r"\d+")
        
        price = format_price(current_price, previous_price)
        price['currency'] = response.css('[itemprop="priceCurrency"]::attr(content)').get()

        return price

    def get_colour(self, response):
        colour = self.get_name(response)
        return colour.split(' - ')[1] if ' - ' in colour else self.ONE_COLOUR 

    def get_skus(self, response):
        skus = {}
        
        common_sku = {
            'colour': self.get_colour(response),            
            'out_of_stock': False
        }
        common_sku.update(self.get_price(response))

        size_css = 'span.size_EU::text, li:not(.hidden) span.units_container::text'                
        sizes = [size for size in response.css(size_css).getall() if size != ' '] or [self.ONE_SIZE]         

        for size in sizes:
            sku_attributes = {**common_sku}                       
            sku_attributes['size'] = size                    
            skus[f"{common_sku['colour']}_{size}"] = sku_attributes
       
        return skus


class SnkrsCrawlSpider(CrawlSpider):       
    listings_css = '#menu li'
    product_css = 'div.product-container'
    
    product_parser = SnkrsParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse_item(self, response):
        return self.product_parser.parse(response)


class FrCrawlSpider(SnkrsCrawlSpider, MixinFR):
    name = f'{MixinFR.name}_crawler'


class UsCrawlSpider(SnkrsCrawlSpider, MixinUS):
    name = f'{MixinUS.name}_crawler'    


class FrParseSpider(SnkrsParseSpider, MixinFR):
    name = f'{MixinFR.name}_parser'    


class UsParseSpider(SnkrsParseSpider, MixinUS):
    name = f'{MixinUS.name}_parser'    
