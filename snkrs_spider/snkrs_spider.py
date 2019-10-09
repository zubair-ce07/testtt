import scrapy

from snkrs.items import SnkrsItem


class SnkrsParseSpider():
    one_size = ['oneSize']
     
    def get_retailer_sku(self, response):
        return response.css('span[itemprop="sku"]::text').extract_first()

    def get_brand(self, response):
        return response.css('meta[itemprop="brand"]::attr(content)').extract_first()

    def get_category(self, response):
        return response.css('span.category::text').extract_first().split('/')[2]

    def get_gender(self, response):
        category = self.get_category(response) 
        
        return category.split(' ')[0] if 'men' in category.lower() else 'Unisex adult'     

    def get_url(self, response):
        return response.css('span.url::text').extract_first()

    def get_description(self, response):
        retailer_sku = self.get_retailer_sku(response)
        product_reference = response.css('p#product_reference label::text').extract() + [retailer_sku]
        return product_reference + response.css('div#short_description_content p::text').extract()

    def get_name(self, response):
        return response.css('h1[itemprop="name"]::text').extract_first().split(' - ')[0]

    def get_image_urls(self, response):
        return response.css('div#carrousel_frame li a::attr(href)').extract()

    def get_skus(self, response):
        colour = response.css('h1[itemprop="name"]::text').extract_first().split(' - ')[1]
        size_css = 'span.units_container span.size_EU::text, li:not(.hidden) span.units_container::text'
        sizes = list(filter(lambda size: size != ' ', response.css(size_css).extract())) or self.one_size         
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

class CrawlSpider(scrapy.Spider):
    name = 'snkrs_spider'
    allowed_domains = ['snkrs.com']
    start_urls = ['http://www.snkrs.com/en/']

    def parse(self, response):        
        category_urls = response.css('ul.sf-menu li a::attr(href)').extract() 

        for url in category_urls:
            yield scrapy.Request(url, callback=self.parse_listings)

    def parse_listings(self, response):
        snkrs_parser = SnkrsParseSpider()
        product_urls = response.css('div.product-container a::attr(href)').extract()

        for url in product_urls:
            yield scrapy.Request(url, callback=snkrs_parser.parse_product)                 
