from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import StartItem

class DerekroseSpider(CrawlSpider):

    name = "derek-rose"
    start_urls = ["https://www.derek-rose.com/"]

    rules = (
        Rule(LinkExtractor(restrict_css=(".global-nav__item"))),
        Rule(LinkExtractor(restrict_css=(".category-products")),callback="product"),
    )

    def product(self, response):

        product = StartItem()

        product["retailer_sku"] = self.get_retailer_sku(response)
        product["gender"] = self.extract_gender(response)
        product["brand"] = "derek rose"
        product["url"] = self.get_url(response)
        product["name"] = self.get_name(response)
        product["description"] = self.get_description(response)
        product["care"] = self.get_care(response)
        product["image_urls"] = self.get_image_url(response)
        product["skus"] = self.get_skus(response)

        yield product

    def get_retailer_sku(self,response):    
        return response.css(".product-details__sku::text").extract_first("").split(": ")[1]
        
    def extract_gender(self,response):
        return response.xpath("//th[contains(text(),'Gender')]/following-sibling::td/text()").extract_first()

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

        price = response.css(".price::text").extract_first()
        currency = "GDP"
        size_label = response.css(".product-details__option-items a::attr(data-size-label)").extract()
        sku_id = response.css(".product-details__option-items a::attr(data-product-id)").extract()
        color = response.xpath("//th[contains(text(),'Colour')]/following-sibling::td/text()").extract_first()
        
        common_sku = {
            "price": price,
            "currency": currency,
            "color": color,
            "size" : "one_size",
            "sku_id": f"one_size{color}" 
        }
    
        if size_label is None:
            return common_sku    

        skus = {}

        for size, sku_id in zip(size_label,sku_id): 
            
            sku = common_sku.copy()
            sku["size"] = size
            sku["sku_id"] = sku_id 

            skus[sku["sku_id"]] = sku.copy()
            
        return skus

