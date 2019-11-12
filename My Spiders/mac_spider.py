from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.selector import Selector

from ..items import Product 
from ..utils import map_gender, format_price


class MacParseSpider():

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
        product['requests'] = self.color_requests(response)

        return self.request_or_product(product)

    def parse_skus(self, response):              
        product = response.meta['product']                                  
        product['skus'].update(self.get_skus(response))
        return self.request_or_product(product)

    def get_retailer_sku(self, response):
        return response.css('[itemprop="sku"]::text').getall()[1].strip()
               
    def get_brand(self, response):        
        return response.css('[itemprop="brand"]::attr(content)').get()

    def get_gender(self, response):
        title_text = response.css('title::text').get()
        categories = self.get_category(response)
        description = self.get_description(response)
        gender_soup = ' '.join(categories + description) + title_text

        return map_gender(gender_soup)

    def get_care(self, response):
        care_s = response.css('.product-links li::attr(data-content)').get()
        selector = Selector(text=care_s)                        
        return [care.strip() for care in selector.css('td div::text').getall()]    

    def get_category(self, response):                
        return response.css('.breadcrumb--list [itemprop="name"]::text').getall()

    def get_description(self, response):             
        return response.css('[itemprop="description"] li::text').getall()

    def get_url(self, response):
        return response.url

    def get_name(self, response):        
        return response.css('.product--title::text').get().strip()

    def get_image_urls(self, response):        
        return response.css('.image-slider--container [itemprop="image"]::attr(srcset)').getall()

    def get_colour(self, response):
        return response.css('.color-images--article-switcher .selected--option a::attr(title)').get()

    def get_sizes(self, response):
        return [size.strip() for size in response.css('[for="group[1]"]:not(.is--disabled)::text').getall()]

    def get_sizes_out_of_stock(self, response):
        css = '.variant--option.no--stock [for="group[1]"]::text'
        return [size.strip() for size in response.css(css).getall()]

    def get_lengths(self,response):
        return [size.strip() for size in response.css('[for="group[2]"]:not(.is--disabled)::text').getall()]

    def get_lengths_out_of_stock(self, response):
        css = '.variant--option.no--stock [for="group[2]"]::text'
        return [size.strip() for size in response.css(css).getall()]

    def get_skus(self, response):
        skus = {}
        common_sku = {}                                           
                                               
        if self.get_colour(response):
            common_sku['colour'] = self.get_colour(response)

        common_sku.update(self.get_price(response))  
            
        for size in self.get_sizes(response):
            for length in self.get_lengths(response):    
                sku_attributes = {**common_sku}                
                sku_attributes['size'] = size
                sku_attributes['out_of_stock'] = size in self.get_sizes_out_of_stock(response) \
                    or length in self.get_lengths_out_of_stock(response)               
                
                if 'colour' in common_sku: 
                    skus[f"{common_sku['colour']}_{size}_{length}"] = sku_attributes
                else:
                    skus[f'{size}_{length}'] = sku_attributes
                               
        return skus
   
    def get_price(self, response):        
        previous_price = response.css('.content--discount span::text').re_first(r'EUR\xa0(.*)')
        previous_price = previous_price.split(',') if previous_price else []
        current_price = response.css('[itemprop="price"]::attr(content)').get()
        
        price = format_price(current_price, '.'.join(previous_price))
        price['currency'] = response.css('[itemprop="priceCurrency"]::attr(content)').get()                          
       
        return price    

    def color_requests(self, response):        
        color_urls = response.css('.color-images--article-switcher a::attr(href)').getall()        
        return [response.follow(url, callback=self.parse_skus, dont_filter=True) for url in color_urls]

    def request_or_product(self, product):           
        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request
        else:
            del product['requests']

        return product


class MacCrawlSpider(CrawlSpider):
    name = 'mac_spider'
    allowed_domains = ['mac-jeans.com']
    start_urls = ['https://mac-jeans.com/at-de']

    product_parser = MacParseSpider()

    category_css = '.navigation--link'
    allow_re = ['/women', '/men']    

    rules = (
        Rule(LinkExtractor(restrict_css=category_css, allow=allow_re), callback='parse_category'),        
    )

    def parse_category(self, response):
        category_urls = response.css('div.sidebar--categories-navigation a::attr(href)').getall()[:-2]        
        return [response.follow(url, callback=self.parse_pagination) for url in category_urls]

    def parse_pagination(self, response):      
        total_pages = response.css('.paging--display strong::text').get()
        
        if total_pages:             
            return [response.follow(f'{response.url}?p={p}', callback=self.parse_listings) for p in range( 
                    1, int(total_pages)+1)]

        return response.follow(response.url, callback=self.parse_listings)         

    def parse_listings(self, response):
        product_urls = response.css('.product--info a::attr(href)').getall()                       
        return [response.follow(url, callback=self.product_parser.parse_product) for url in product_urls]
