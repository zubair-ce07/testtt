import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from softsurroundings.items import SoftsurroundingsItem      


class ParseSpider():

    def get_retailer_sku(self, response):
        return response.css('input[name^=sku_]::attr(value)').extract_first()

    def get_gender(self, response):
        title_text = response.css('title::text').extract_first()        
        return title_text.split(' ')[0] if 'men' in title_text.lower() else 'Unisex adult'

    def get_brand(self, response):
        brand_css = 'meta[property="og:site_name"]::attr(content)'
        return response.css(brand_css).extract_first()

    def get_care(self, response):
        care_css = '#careAndContentInfo::text'        
        return response.css(care_css).extract()    

    def get_category(self, response):        
        category_css = '.pagingBreadCrumb a:nth-child(2)::text'        
        return response.css(category_css).extract()

    def get_description(self, response):
        description_css = 'span[itemprop="description"]::text'
        return response.css(description_css).extract()

    def get_url(self, response):
        return response.url

    def get_name(self, response):
        name_css = 'span[itemprop="name"]::text'
        return response.css(name_css).extract_first()

    def get_image_urls(self, response):
        images_css = '#detailAltImgs > li a::attr(href)'
        return response.css(images_css).extract()

    def skus_requests(self, response):
        sizes = response.css('#sizecat > a::attr(id)').extract()
        size_ids = [size.split('_')[1] for size in sizes]
        BASE_URL = 'https://www.softsurroundings.com'

        return [scrapy.Request(f'{BASE_URL}/p/{size_id}', callback=self.parse_skus) for size_id in size_ids]

    def request_or_product(self, product):
        if product['requests']:
            request = product['requests'].pop()
            request.meta['product'] = product
            return request
        else:
            del product['requests']

        return product

    def parse_skus(self, response):
        product = response.meta['product']
        skus = self.get_skus(response)
        if skus:
            product['skus'] = skus

        return self.request_or_product(product)

    def get_skus(self, response):
        skus = {}
        colours_css = '.swatchHover > span::text, .basesize'
        colours = response.css(colours_css).extract()
        sizes = response.css('.box.size::text').extract()
        availability = response.css('.stockStatus b.basesize::text')

        for size in sizes:
            for colour in colours:
                skus[f'{colour}_{size}'] = {
                    'price': response.css('span[itemprop="price"]::text').extract_first(),
                    'currency': response.css('span[itemprop="priceCurrency"]::attr(content)').extract_first(),
                    'colour': colour,
                    'size': size,
                    'out_of_stock': 'True' if availability != 'In Stock' else 'False'
                } 
               
        return skus

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


class CrawlSpider(CrawlSpider):
    name = 'softsurroundings_spider'    
    allowed_domains = ['softsurroundings.com']
    start_urls = ['http://www.softsurroundings.com']

    softsurroundings_parser = ParseSpider()

    listings_css = 'ul#menubar'
    product_css = 'div.product'

    def parse_item(self, response):
        return self.softsurroundings_parser.parse_product(response)

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )
