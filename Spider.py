from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import StartItem

class FilaSpider(CrawlSpider):

    name = "Fila"
    currency = "Brazilian real"
    start_urls = ["https://www.fila.com.br/"]
    listings_css = [".nav-primary", ".carrossel-thumb"]
    products_css = [".category-products"]

    rules = (
        Rule(LinkExtractor(restrict_css = listings_css)),
        Rule(LinkExtractor(restrict_css = products_css), callback = "product_items"),
    )

    care_list = [
        "malha de poliamida","poliéster","algodão","pele","Cuidado","resistência","sentindo-me",
        "casual","confortável","couro","tecido","protecção","material","conforto","confortável"
    ]
    gender_map = { 
        "men": "masculina",
        "women": "feminino",
        "children": "infantial"
    }

    def product_items(self, response):

        product = StartItem()

        product["retailer_sku"] = self.extract_retailer_sku(response)
        product["brand"] = self.name
        product["url"] = response.url
        product["name"] = self.extract_name(response)
        product["gender"] = self.extract_gender(product["name"])
        product["image_urls"] = self.extract_image_url(response)

        if self.check_instock(response):
            product["out_of_stock"] = True
            product["skus"] = None
        else:
            product["skus"] = self.extract_skus(response)

        product["care"] = self.extract_care(response)
        product["description"] = self.extract_description(response)

        yield product

    def extract_retailer_sku(self,response):
        return response.css(".wrap-sku small::text").extract_first()

    def extract_name(self, response):
        return response.css(".product-name h1::text").extract_first()

    def extract_gender(self,product_name):

        for key, value in self.gender_map.items():

            if (value in product_name) or (value.capitalize() in product_name):
                return key

        return "unisex"

    def extract_image_url(self, response):
        return  response.css(".product-image-gallery img::attr(src)").extract()

    def check_instock(self,response):
        return response.css(".product-shop.unlogged div[class = 'unavailable-product-block']")

    def extract_skus(self, response):
    
        price = response.css(".price::text").extract_first()
        currency = self.currency
        color = response.css(".wrap-sku small::text").extract()[1]
        size_label =  response.css(".configurable-swatch-list.clearfix li::attr(data-size)").extract()

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

        for size in size_label: 

            sku = common_sku.copy()
            sku["size"] = size
            sku["sku_id"] = f"{size}{color}" 

            skus[sku["sku_id"]] = sku.copy()
            
        return skus

    def extract_raw_description(self, response):
        return response.css(".wrap-long-description p::text").extract_first()

    def extract_care(self,response):
        
        raw_description =  self.extract_raw_description(response)
        
        if raw_description is  None:
            return None

        for care_word in self.care_list:

            if care_word in raw_description:
                return raw_description

        return None

    def extract_description(self,response):

        raw_description = self.extract_raw_description(response)
        
        if raw_description is  None:
            return None

        for care_words in self.care_list:

            if care_words in raw_description:
                return None
        
        return raw_description

