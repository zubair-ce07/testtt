from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Product 
from ..utils import parse_gender, parse_price


class ParseSpider():
    
    def parse_product(self, response):                   
        product = Product()
        
        product['retailer_sku'] = self.get_retailer_sku(response)
        product['gender'] = self.get_gender(response)
        product['category'] = self.get_category(response)
        product['brand'] = self.get_brand(response)
        product['url'] = self.get_url(response)
        product['name'] = self.get_name(response)
        product['description'] = self.get_description(response)
        product['care'] = self.get_care(response)
        product['skus'] = {}
        product['image_urls'] = self.get_image_urls(response)    

        requests = self.availability_requests(response) + self.skus_requests(response) 
        
        return self.request_or_product(product, requests)

    def parse_skus(self, response):              
        product = response.meta['product']
        requests = response.meta['requests']

        skus = self.get_skus(response)                   
        product['skus'].update(skus)

        return self.request_or_product(product, requests)

    def parse_availability(self, response):        
        product = response.meta['product']
        requests = response.meta['requests']

        availability = response.css('.stockStatus .basesize::text').get()
        sku_id = response.url.split('/')[-2]
             
        if sku_id in product['skus']:                        
            product['skus'][sku_id]['out_of_stock'] = availability != 'In Stock.'
            
        return self.request_or_product(product, requests)

    def get_retailer_sku(self, response):
        return response.css('#item::text').get()
               
    def get_brand(self, response):
        css = '[property="og:site_name"]::attr(content)'
        return response.css(css).get()

    def get_gender(self, response):
        title_text = response.css('title::text').get()
        size_categories = response.css('#sizecat a::text').getall()
        description = self.get_description(response)

        raw_gender = f"{title_text} {' '.join(size_categories + description)}"

        return parse_gender(raw_gender)

    def get_care(self, response):                
        return response.css('#careAndContentInfo::text').getall()    

    def get_category(self, response):                
        return response.css('.pagingBreadCrumb a::text').getall()

    def get_description(self, response):
        css = '[itemprop="description"] p::text, [itemprop="description"]::text'        
        return response.css(css).getall()

    def get_url(self, response):
        return response.url

    def get_name(self, response):        
        return response.css('[itemprop="name"]::text').get()

    def get_image_urls(self, response):        
        return response.css('#detailAltImgs > li a::attr(href)').getall()        

    def get_skus(self, response):
        skus = {}
       
        currency_css = '[itemprop="priceCurrency"]::attr(content)'
        currency = response.css(currency_css).get()

        color_css = '.swatchlink .color::attr(data-value)'        
        color_ids = response.css(color_css).getall() or response.css('[name^="specOne"]::attr(value)').get()

        sizes = response.css('a.box.size::attr(id)').getall()                                
        size_ids = [size.split('_')[1] for size in sizes]

        for color_id in color_ids:
            for size_id in size_ids:
                color_css = f'img[id="color_{color_id}"] + div > span::text, #color .basesize::text'
                sku_attributes = {}

                sku_attributes.update(self.get_price(response))                
                sku_attributes['currency'] = currency
                sku_attributes['colour'] = response.css(color_css).get()
                sku_attributes['size'] = response.css(f'a[id$="{size_id}"]::text, #size .basesize::text').get()               

                skus[f'{color_id}{size_id}'] = sku_attributes
                               
        return skus
   
    def get_price(self, response):
        previous_price = response.css('.ctntPrice::text').re_first(r'Was \$(.*);')
        current_price = response.css('[itemprop="price"]::text').get()       

        return parse_price(previous_price, current_price)
        
    def skus_requests(self, response):
        size_cat = response.css('#sizecat > a::attr(id)').getall()
        sizes = [size.split('_')[1] for size in size_cat]        
            
        return [response.follow(f'/p/{id.lower()}', callback=self.parse_skus, dont_filter=True) for id in sizes]

    def availability_requests(self, response):
        availability_requests = []

        product_id = self.get_retailer_sku(response)
        color_css = '.swatchlink .color::attr(data-value)'

        color_ids = response.css(color_css).getall() or response.css('[name^="specOne"]::attr(value)').get()        
        size_ids = [size.split('_')[1] for size in response.css('a.box.size::attr(id)').getall()]
        
        for color_id in color_ids:
            for size_id in size_ids:

                availability_requests.append(
                    response.follow(f'/p/{product_id.lower()}/{color_id}{size_id}',
                    callback=self.parse_availability))

        return availability_requests        
         
    def request_or_product(self, product, requests):           
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            request.meta['requests'] = requests

            return request                                

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
