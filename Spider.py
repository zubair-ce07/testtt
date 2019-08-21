from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import StartItem


class FilasSpider(CrawlSpider):

    name = "Fila"
    start_urls = ['https://www.fila.com.br/']
    product_grid = ".category-products"
    next_page = ".carrossel-thumb"
    pagging = [product_grid, next_page]

    rules = (
        Rule(LinkExtractor(restrict_css=".nav-primary")),
        Rule(LinkExtractor(restrict_css = pagging),callback='product_items'),
    )

    gender_list = ["Masculina","Masculino","mulheres","infantial","Infantil","Feminino","Feminina"]
    care_list = ["malha de poliamida","poliéster","algodão","pele","Cuidado","resistência","sentindo-me",
                "casual","confortável","couro","tecido","protecção","material","conforto","confortável"
    ]

    def product_items(self, response):

        product = StartItem()

        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['brand'] = "Fila"
        product['url'] = response.url
        product['name'] = self.extract_name(response)
        product['gender'] = self.extract_gender(product['name'])
        product['description'] = self.extract_description(response)
        product['care'] = self.extract_care(product['description'])
        product['image_urls'] = self.extract_image_url(response)
        product['skus'] = self.extract_skus(response)

        yield product

    def extract_retailer_sku(self,response):
        return response.css(".wrap-sku small::text").extract_first()

    def extract_name(self, response):
        return response.css(".product-name h1::text").extract_first()

    def extract_gender(self,product_name):

        for gender in self.gender_list:
            if gender in product_name:
                return gender
        return None

    def extract_description(self, response):
        return response.css(".wrap-long-description p::text").getall()

    def extract_care(self, description):    
        
        for care in self.care_list:
            if care in description:
                return description
        return None

    def extract_image_url(self, response):
        return  response.css(".product-image-gallery img::attr(src)").getall()

    def extract_skus(self, response):

        price = response.css(".price::text").extract_first()
        currency = 'Dollar'
        size_label =  response.css(".configurable-swatch-list.clearfix li::attr(data-size)").extract()
        product_id = response.css(".no-display input[id = 'product-id']::attr(value)").extract()

        sku = {
            "price": price,
            "currency": currency,
            "size": size_label,
            "sku-id": product_id
        }

        return sku
