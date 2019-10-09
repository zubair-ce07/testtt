import scrapy

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from snkrs.items import SnkrsItem


class SnkrsParseSpider():
    ONE_SIZE = 'oneSize'
     
    def get_retailer_sku(self, response):
        return response.css('span[itemprop="sku"]::text').extract_first()

    def get_brand(self, response):
        return response.css('meta[itemprop="brand"]::attr(content)').extract_first()

    def get_category(self, response):
        return response.css('span.category::text').extract_first().split('/')

    def get_gender(self, response):
        category = self.get_category(response) 
        
        return category.split(' ')[0] if 'men' in category[0].lower() else 'Unisex adult'     

    def get_url(self, response):
        return response.request.url

    def get_description(self, response):        
        return response.css('div#short_description_content p::text').extract()

    def get_name(self, response):
        return response.css('h1[itemprop="name"]::text').extract_first().split(' - ')[0]

    def get_image_urls(self, response):
        return response.css('div#carrousel_frame li a::attr(href)').extract()

    def get_skus(self, response):
        colour = response.css('h1[itemprop="name"]::text').extract_first().split(' - ')[1]
        size_css = 'span.units_container span.size_EU::text, li:not(.hidden) span.units_container::text'
        sizes = [size for size in response.css(size_css).extract() if size != ' '] or [self.ONE_SIZE]         
        skus = {}

        for size in sizes:
            availability = response.css('span.availability::text').extract_first()            
            skus[f'{colour}_{size}'] = {
                'price': float(response.css('span[itemprop="price"]::attr(content)').extract_first()),
                'currency': response.css('meta[itemprop="priceCurrency"]::attr(content)').extract_first(),
                'out_of_stock': 'False' if availability == 'InStock' else 'True',
                'size': size,
                'colour': colour
            }
       
        return skus

    def parse_product(self, response):
        product = SnkrsItem()

        product['retailer_sku'] = self.get_retailer_sku(response)
        product['gender'] = self.get_gender(response)
        product['category'] = [self.get_category(response)]
        product['brand'] = self.get_brand(response)
        product['url'] = self.get_url(response)
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['care'] = []
        product['skus'] = self.get_skus(response)
        product['image_urls'] = self.get_image_urls(response)

        yield product    


class CrawlSpider(CrawlSpider):
    product_parser = SnkrsParseSpider()
    name = 'snkrs_spider'
    allowed_domains = ['snkrs.com']
    start_urls = ['http://www.snkrs.com/en/']
    listings_css = 'ul.sf-menu'
    product_css = 'div.product-container'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback=product_parser.parse_product)
    )
