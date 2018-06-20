import scrapy
import re

from scrapy.spiders import Request, CrawlSpider
from scrapy.loader import ItemLoader

from Trial.items import Product


class PstrialSpider(CrawlSpider):
    name = 'pstrial'
    
    allowed_domains = ['pstrial-2018-05-21.toscrape.com']
    start_urls = ['http://pstrial-2018-05-21.toscrape.com/browse/']
    base_url = 'http://pstrial-2018-05-21.toscrape.com'
    
    allowed_categories = ['insunsh', 'summertime']
    allowed_items = ['item']
    allowed_pages = ['page=']

    def parse(self, response):
        trail = response.meta.get('trail') or []
        products = response.meta.get('products') or []
        
        trail = trail.copy() + [response.url]
        products = products.copy() + response.css('#body div a::attr(href)').extract()
        urls = response.css('#subcats div a::attr(href)').extract()

        if urls:
            for url in urls:
                if any(category in url for category in self.allowed_categories):
                    yield Request(self.base_url+url, callback=self.parse, meta={'trail': trail, 'products': products})
        elif products:
            for product in products:
                if any(item in product for item in self.allowed_items):
                    yield Request(self.base_url+product, callback=self.parse_item, meta={'trail': trail})
                if any(page in product for page in self.allowed_pages) and self.products(response):
                    yield Request(self.base_url+product, callback=self.parse, meta={'trail': trail,
                                                                                    'products': products})
         
    def products(self, response):
        if response.css('#body div a div'):
            return True
        return False

    def products_url(self, response):
        products = []
        products_url = response.css('#body div:nth-child(2) a::attr(href)').extract()
        
        for url in products_url:
            if any(category in url for category in self.allowed_categories) and not any(page in url for page in self.allowed_pages):
                products.append(url)
        
        return products

    def parse_item(self, response):
        raw_dimensions = self.raw_dimensions(response)
        dimensions = self.dimensions(raw_dimensions)
        product = ItemLoader(item=Product(), response=response)

        product.add_value('url', response.url)
        product.add_css('artist', self.artist())
        product.add_css('title', self.title())
        product.add_value('image', self.image(response))
        product.add_css('description', self.description())
        product.add_value('path', response.meta.get('trail'))

        if dimensions and len(dimensions) > 2:
            product.add_value('width', self.width(dimensions))
            product.add_value('height', self.height(dimensions))

        return product.load_item()

    def artist(self):
        return '#content h2::text'

    def title(self):
        return '#content h1::text'

    def image(self, response):
        image = response.css('img::attr(src)').extract_first()
        return self.base_url+image

    def description(self):
        return 'p::text'

    def raw_dimensions(self, response):
        dimension = response.css('dd::text').extract()
        return dimension[2]

    def dimensions(self, raw_dimensions):
        dimensions = re.search('\(([^)]+cm)', raw_dimensions)
        if dimensions:
            dimensions = dimensions.group(1)
            return dimensions.split(' ')

    def width(self, dimensions):
            return dimensions[0]

    def height(self, dimensions):
            return dimensions[2]



