import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import StartItem

class MySpider(CrawlSpider):

    name = "derek-rose"
    start_urls = ['https://www.derek-rose.com/']
    rules = (
        Rule(LinkExtractor(restrict_css=(".global-nav__item"))),
        Rule(LinkExtractor(restrict_css=(".category-products")),callback='product'),
   )

    def product(self, response):

        items = StartItem()

        items['retailer_sku'] = self.get_retailer_sku(response)
        items['gender'] = self.extract_gender(response)
        items['brand'] = "derek rose"
        items['url'] = self.get_url(response)
        items['name'] = self.get_name(response)
        items['description'] = self.get_description(response)
        items['care'] = self.get_care(response)
        items['image_urls'] = self.get_image_url(response)
        items['skus'] = self.get_skus(response)

        yield items

    def get_retailer_sku(self,response):
    
        return response.css(".product-details__sku::text").extract_first("").split(": ")[1]
        
    def extract_gender(self,response):

        return response.xpath('//th[contains(text(),"Gender")]/following-sibling::td/text()').extract_first()

    def get_url(self, response):

        return response.url

    def get_name(self, response):

        return response.css(".product-details__sub::text").extract_first()

    def get_description(self, response):

        return response.css(".product-details__short-description span::text").extract_first("").strip()

    def get_care(self, response):

        return response.css(".product-details__attrs:last-child td::text").extract()

    def get_image_url(self, response):

        return  response.css(".product-cloudzoom::attr(src)").extract()

    def get_skus(self, response):

        skus = {}

        price = response.css(".price::text").extract_first()
        currency = 'GDP'
        size_label = response.css(".product-details__option-items a::attr(data-size-label)").extract()
        product_id = response.css(".product-details__option-items a::attr(data-product-id)").extract()
        color = response.xpath('//th[contains(text(),"Colour")]/following-sibling::td/text()').extract_first()
        
        sku = {
            "price": price,
            "currency": currency,
            "color": color,
            "size" : "one_size",
            "sku_id": None 
        }
    
        if size_label is None:
            return sku    

        for size, sku_id in zip(size_label,product_id): 
            
            sku_update = {
                "size": size,
                "sku_id": sku_id 
            }

            sku.update(sku_update)

            skus[sku["sku_id"]] = sku.copy()
            
        return skus
                 
