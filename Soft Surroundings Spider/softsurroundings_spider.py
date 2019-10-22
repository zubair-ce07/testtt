from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Spider

from softsurroundings.items import SoftsurroundingsItem 
from softsurroundings.utils import *


class ParseSpider(Spider):
    name = 'parse_spider'
    start_urls = ['https://www.softsurroundings.com/p/brinley-top/']
    
    def parse(self, response):
        return self.parse_product(response)    

    def parse_product(self, response):                   
        product = SoftsurroundingsItem()

        product['retailer_sku'] = self.get_retailer_sku(response)
        product['gender'] = get_gender(response)
        product['category'] = self.get_category(response)
        product['brand'] = self.get_brand(response)
        product['url'] = self.get_url(response)
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['care'] = self.get_care(response)
        product['skus'] = {}
        product['image_urls'] = self.get_image_urls(response)        
        product['requests'] = self.availability_requests(response) + self.skus_requests(response) 
        
        return self.request_or_product(product)

    def parse_skus(self, response):              
        product = response.meta['product']
        skus = self.get_skus(response)                   
        product['skus'].update(skus)

        return self.request_or_product(product)

    def parse_availability(self, response):        
        product = response.meta['product']
        availability = response.css('.stockStatus .basesize::text').get()
        sku_id = response.url.split('/')[-2]
             
        if sku_id in list(product['skus'].keys()):                        
            product['skus'][sku_id]['out_of_stock'] = True if availability != 'In Stock' else False
            
        return self.request_or_product(product)

    def get_retailer_sku(self, response):
        return response.css('input[name^=sku_]::attr(value)').get()
               
    def get_brand(self, response):
        css = 'meta[property="og:site_name"]::attr(content)'
        return response.css(css).get()

    def get_care(self, response):                
        return response.css('#careAndContentInfo::text').getall()    

    def get_category(self, response):                
        return response.css('.pagingBreadCrumb a::text').getall()

    def get_description(self, response):
        css = 'span[itemprop="description"] p::text, span[itemprop="description"]::text'        
        return response.css(css).getall()

    def get_url(self, response):
        return response.url

    def get_name(self, response):        
        return response.css('span[itemprop="name"]::text').get()

    def get_image_urls(self, response):        
        return response.css('#detailAltImgs > li a::attr(href)').getall()

    def get_skus(self, response):
        skus = {}

        currency_css = 'span[itemprop="priceCurrency"]::attr(content)'
        price_css = 'span[itemprop="price"]::text'
        color_css = '.swatchlink .color::attr(data-value)'        
                                
        sizes = response.css('a.box.size::attr(id)').getall()
        color_ids = response.css(color_css).getall()

        size_ids = [size.split('_')[1] for size in sizes]

        for color_id in color_ids:
            for size_id in size_ids:
                sku_attributes = {}

                sku_attributes['previous_price'] = int(float(response.css(price_css).get())*100)
                sku_attributes['currency'] = response.css(currency_css).get()
                sku_attributes['colour'] = get_color(response, color_id)
                sku_attributes['size'] = get_size(response, size_id)               

                skus[f'{color_id}{size_id}'] = sku_attributes
                               
        return skus   

    def skus_requests(self, response):
        size_cat = response.css('#sizecat > a::attr(id)').getall()
        sizes = [size.split('_')[1] for size in size_cat]        
            
        return [response.follow(f'/p/{id.lower()}', callback=self.parse_skus, dont_filter=True) for id in sizes]

    def availability_requests(self, response):            
        product_id = response.css('#item::text').get()
        color_css = '.swatchlink .color::attr(data-value)'

        color_ids = response.css(color_css).getall()
        sizes = response.css('a.box.size::attr(id)').getall()

        size_ids = [size.split('_')[1] for size in sizes]
        
        return [response.follow(f'/p/{product_id.lower()}/{color_id}{size_id}', method='POST', \
         callback=self.parse_availability, dont_filter=True) \
         for color_id in color_ids for size_id in size_ids]
         
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
    start_urls = ['https://www.softsurroundings.com/']

    listings_css = 'ul#menubar'
    product_css = 'div.product'        

    softsurroundings_parser = ParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )
    
    def parse_item(self, response):        
        return self.softsurroundings_parser.parse_product(response)
