from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from softsurroundings.items import SoftsurroundingsItem 
from softsurroundings.utils import parse_gender


class ParseSpider():    

    def parse_product(self, response):
        product = SoftsurroundingsItem()

        product['retailer_sku'] = self.get_retailer_sku(response)
        product['gender'] = self.get_gender(response)
        product['category'] = self.get_category(response)
        product['brand'] = self.get_brand(response)
        product['url'] = self.get_url(response)
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['care'] = self.get_care(response)
        product['skus'] = self.get_skus(response)
        product['image_urls'] = self.get_image_urls(response)
        product['requests'] = self.skus_requests(response)

        return self.request_or_product(product)

    def parse_skus(self, response):
        product = response.meta['product']
        skus = self.get_skus(response)        
        product['skus'] = skus

        return self.request_or_product(product)    

    def get_retailer_sku(self, response):
        return response.css('input[name^=sku_]::attr(value)').get()

    def get_gender(self, response):                
        return parse_gender(response)            

    def get_brand(self, response):
        css = 'meta[property="og:site_name"]::attr(content)'
        return response.css(css).get()

    def get_care(self, response):                
        return response.css('#careAndContentInfo::text').getall()    

    def get_category(self, response):                
        return response.css('.pagingBreadCrumb a::text').getall()

    def get_description(self, response):        
        return response.css('span[itemprop="description"] p::text').getall()

    def get_url(self, response):
        return response.url

    def get_name(self, response):        
        return response.css('span[itemprop="name"]::text').get()

    def get_image_urls(self, response):        
        return response.css('#detailAltImgs > li a::attr(href)').getall()

    def get_skus(self, response):
        skus = {}
        sku_attributes = {}

        colours_css = '.swatchHover > span::text, .basesize::text'
        currency_css = 'span[itemprop="priceCurrency"]::attr(content)'
        
        sizes = response.css('.box.size::text').getall()
        availability = response.css('.stockStatus b.basesize::text').get()
        colours = response.css(colours_css).getall()

        for size in sizes:
            for colour in colours:
                sku_attributes['previous_price'] = float(response.css('span[itemprop="price"]::text').get())
                sku_attributes['currency'] = response.css(currency_css).get()
                sku_attributes['colour'] = colour
                sku_attributes['size'] = size
                sku_attributes['out_of_stock'] = True if availability != 'In Stock' else False

                skus[f'{colour}_{size}'] = sku_attributes
                               
        return skus

    def skus_requests(self, response):
        sizes = response.css('#sizecat > a::attr(id)').getall()
        size_ids = [size.split('_')[1] for size in sizes]
        
        return [response.follow(f'/p/{id.lower()}', callback=self.parse_skus) for id in size_ids]

    def request_or_product(self, product):
        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request                        
        else:
            del product['requests']

        return product   


class CrawlSpider(CrawlSpider):
    name = 'softsurroundings_spider'    
    allowed_domains = ['softsurroundings.com']
    start_urls = ['https://www.softsurroundings.com/p/the-ultimate-leggings/']

    listings_css = 'ul#menubar'
    product_css = 'div.product'

    softsurroundings_parser = ParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )
    
    def parse_item(self, response):
        return self.softsurroundings_parser.parse_product(response)

    def parse_start_url(self, response):
        return self.softsurroundings_parser.parse_product(response)
