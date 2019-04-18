
from ..items import DecimasCrawlerItem
from ..mappings import Mapping
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from ..utility_functions import get_price, gender_extractor
import json


class ProductCrawlerSpider(scrapy.spiders.CrawlSpider):
    name = 'decimas_crawler'
    allowed_domains = ['decimas.es']
    start_urls = ['https://www.decimas.es']
    rules = (
        Rule(LinkExtractor(restrict_css=".clever-mega-menu"), callback='parse', follow=True),
        Rule(LinkExtractor(restrict_css="li.product-item"), callback='parse_item', follow=True),
    )

    def parse_item(self, response): 
        item = DecimasCrawlerItem()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['gender'] = self.extract_gender(response)
        item['brand'] = self.extract_brand(response)
        item['url'] = self.extract_url(response)
        item['retailer'] = self.extract_retailer()
        item['name'] = self.extract_name(response)
        item['description'] = self.extract_description(response)
        item['previous_price'] = self.extract_previous_price(response)
        item['image_urls'] = self.extract_img_urls(response)
        item['skus'] = self.extract_skus(response)
        item['currency'] = self.extract_currency(response)
        item['price'] = self.extract_final_price(response)
        yield item
        
    def extract_retailer_sku(self, response):
        return response.css('div.price-box::attr(data-product-id)').extract_first()
        
    def extract_gender(self, response):
        product_name = self.extract_name(response)
        return gender_extractor(product_name)
        
    def extract_brand(self, response):
        brand_names = response.css('a.brand img::attr(title)').extract()
        product_name = self.extract_name(response)

        for brand in brand_names:
            if brand.lower() in product_name.lower():
                return brand
    
    def extract_url(self, response):
        return response.url
    
    def extract_retailer(self):
        return "Decimas.es"

    def extract_name(self, response):
        return response.css('div.attribute.name h1::text').extract_first()    
        
    def extract_description(self, response):
        return response.css('div.value::text').extract_first()

    def extract_previous_price(self, response):
        current_price = self.price_only(response) 
        if current_price:
            if len(current_price) >= 2:
                return current_price.remove(min(current_price))         
                
    def extract_img_urls(self, response):
        images_urls = []
        data = self.raw_products(response)
        image_sources = data['images']
        for color in data['attributes']['93']['options']:
            for product in color['products']:
                product_images = image_sources[product]
                for product_image in product_images:
                    images_urls.append(product_image['full'])       
        return images_urls    
    
    def extract_skus(self, response):
        skus =[]
        data = self.raw_products(response)   
        currency = data['currencyFormat']
        currency = (currency.replace("%s",u' ')).strip()
        currency = Mapping.currency_map[currency]
        previous_price = self.extract_previous_price(response)
        for color in data['attributes']['93']['options']:
            for size in data['attributes']['154']['options']:
                for k in color['products']:
                    for t in size['products']:
                        if k==t:
                            skus.append(self.make_sku(data['optionPrices'][t]['finalPrice']['amount'], \
                            currency, color['label'], size['label'], k, previous_price))
        return skus

    def extract_currency(self, response):
        data = self.raw_products(response)
        currency = data['currencyFormat']
        currency = (currency.replace("%s",u' ')).strip()
        return Mapping.currency_map[currency]
        
    def extract_final_price(self, response):
        current_price = self.price_only(response)
        if current_price:
            if len(current_price) >= 2:
                return min(current_price)         
            else:
                return current_price

    def price_only(self, response):
        current_price = response.css('span.price::text').extract()
        current_price = [x.replace(u'\xa0€', u' ') for x in current_price if x]
        return get_price(current_price)    

    def make_sku(self, price, currency, color, size, sku_id, previous_price):
        skus = {}
        skus['price'] = price
        skus['currency'] = currency
        skus['size'] = size
        skus['color'] = color
        skus['sku_id'] = sku_id
        skus ['previous_price'] = previous_price
        return skus

    def raw_products(self, response):
        script_text = response.xpath("//script[contains(text(),'[data-role=swatch-options]')]/text()").extract_first()
        #script_text = response.css("script[type='text/x-magento-init']::text").extract()
        json_object = json.loads(script_text)
        return json_object["[data-role=swatch-options]"]["Magento_Swatches/js/swatch-renderer"]["jsonConfig"]
