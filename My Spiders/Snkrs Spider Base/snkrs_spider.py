from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'snkrs'
    allowed_domains = ['snkrs.com']    


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'    
    start_urls = ['https://www.snkrs.com/en/']


class MixinFR(Mixin):    
    retailer = Mixin.retailer + '-fr'
    market = 'FR'
    start_urls = ['https://www.snkrs.com/fr/']


class SnkrsParseSpider(BaseParseSpider):
    description_css = '#short_description_content p::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['url'] = response.url
        garment['brand'] = self.product_brand(response)
        garment['gender'] = self.product_gender(response, garment)
        garment['merch_info'] = self.merch_info(garment)
        garment['image_urls'] = self.image_urls(response)        
        garment['skus'] = self.skus(response)

        return garment

    def product_id(self, response):
        return response.css('[itemprop="sku"]::text').get()

    def product_brand(self, response):
        return response.css('[itemprop="brand"]::attr(content)').get()

    def product_gender(self, response, garment):
        title_text = response.css('title::text').get()
        category = self.product_category(response)
        description = garment['description']

        gender_soup = ' '.join(category + description) + title_text
        return self.gender_lookup(gender_soup)  

    def product_name(self, response):
        return response.css('[itemprop="name"]::text').get()

    def image_urls(self, response):
        return clean(response.css('#carrousel_frame li a::attr(href)'))   

    def product_category(self, response):
        category = response.css('span.category::text').get()
        return clean(category.split('/'))

    def merch_info(self, garment):
        soup = ' '.join(garment['description'])
        if 'limited edition' in soup.lower():
            return ['Limited Edition']
        return []

    def product_colour(self, response):
        colour = self.product_name(response)        
        return colour.split(' - ')[1] if ' - ' in colour else ''

    def money_strs(self, response):
        current_price = response.css('[itemprop="price"]::attr(content)').get()
        previous_price = response.css('#old_price_display .price::text').re_first(r"\d+")
        currency = response.css('[itemprop="priceCurrency"]::attr(content)').get()

        return [previous_price, current_price, currency]

    def skus(self, response):
        skus = {}        
        
        common_sku = self.product_pricing_common(None, money_strs=self.money_strs(response))
        colour = self.product_colour(response)
        
        if colour:
            common_sku['colour'] = colour

        common_sku['out_of_stock'] = False
        size_css = 'span.size_EU::text, li:not(.hidden) span.units_container::text'
        sizes = [size for size in response.css(size_css).getall() if size != ' '] or [self.one_size]

        for size in sizes:
            sku = {**common_sku}            
            sku['size'] = size
            skus.update({(f"{colour}_" if colour else '') + size: sku})

        return skus  


class SnkrsCrawlSpider(BaseCrawlSpider):
    listings_css = '#menu li'
    product_css = 'div.product-container'    

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )        


class SnkrsUSParseSpider(MixinUS, SnkrsParseSpider):
    name = MixinUS.retailer + '-parse'


class SnkrsUSCrawlSpider(MixinUS, SnkrsCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = SnkrsUSParseSpider()


class SnkrsFRParseSpider(MixinFR, SnkrsParseSpider):
    name = MixinFR.retailer + '-parse'


class SnkrsFRCrawlSpider(MixinFR, SnkrsCrawlSpider):
    name = MixinFR.retailer + 'crawl'
    parse_spider = SnkrsFRParseSpider()
