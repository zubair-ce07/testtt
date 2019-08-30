from scrapy import Request, FormRequest, Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from json import loads, dumps

from ..items import StartItem

class Khelfpider(CrawlSpider):

    name = "Khelf"
    currency = "Brazilian real"
    start_urls = ["https://www.khelf.com.br/"]
    listings_css = [".menu-categorias", ".link[rel='nex']::attr(href)"]

    rules = (
        Rule(LinkExtractor(restrict_css = listings_css), callback = "Parse"),
    )

    care_list = [
        "malha de poliamida","poliéster","algodão","pele","Cuidado","resistência","sentindo-me",
        "casual","confortável","couro","tecido","protecção","material","conforto","confortável"
    ]
    gender_dic = { 
        "men": "masculina",
        "women": "feminino",
        "children": "infantial"
    }

    def Parse(self, response):

        for link in response.css(".list-products li"):

            product = link.css("a[class='change link url']::attr(href)").extract_first()
            color_codes =  link.css(".skus.p-v.color a::attr(color-code)").extract()

            if product is not None:
                request =  Request(url = product, method="POST", callback = self.product_parse)
                request.meta["color_codes"] = color_codes
                yield request

    def product_parse(self,response):

        product = StartItem()

        product["retailer_sku"] = self.extract_retailer_sku(response)
        product["brand"] = self.extract_brand(response)
        product["url"] = response.url
        product["name"] = self.extract_name(response)
        product["price"] = self.extract_price(response)
        product["gender"] = self.extract_gender(product["name"])
        product["image_urls"] = []
        product["skus"] = {}
        product["meta"] = self.extract_requests(product,response)
        product["care"] = self.extract_care(response)
        product["description"] = self.extract_description(response)

        yield self.check_request(product)

    def extract_retailer_sku(self,response):
        return response.css(".fab-cod span::attr(content)").extract_first().split(":")[1] 
    
    def extract_brand(self,response):
        return response.css("a[rel='home']::attr(title)").extract_first()

    def extract_name(self, response):
        return response.css(".name.fn::text").extract_first("").strip()

    def extract_price(self,response):
        return response.css(".price.sale strong::text").extract_first()

    def extract_gender(self,product_name):
    
        for key, value in self.gender_dic.items():

            if (value in product_name) or (value.capitalize() in product_name):
                return key

        return "unisex"
    
    def extract_requests(self,product,response):

        request_list = []

        color_data ={
            "ProdutoCodigo":None,"CarValorCodigo1":None,"CarValorCodigo2":"0",
            "CarValorCodigo3": "0","CarValorCodigo4":"0","CarValorCodigo5":"0"
        }
        color_header={
                "X-AjaxPro-Method": "DisponibilidadeSKU",
                "Referer": None
        }

        for id in response.meta["color_codes"]:

            color_header["Referer"] = response.url

            color_data["CarValorCodigo1"] = id
            color_data["ProdutoCodigo"] = self.extract_ProdutoCodigo(response)

            request = Request(url="https://www.khelf.com.br/ajaxpro/IKCLojaMaster.detalhes,Khelf.ashx",
                        method="POST",headers = color_header, body=dumps(color_data), callback = self.update_product) 
            request.meta["product_info"] = product
            request_list.append(request)

        return request_list
        
    def extract_ProdutoCodigo(self,response):
        return response.css("input[id='ProdutoCodigo']::attr(value)").extract_first()

    def update_product(self,response):
        
        product = response.meta["product_info"]
        json_response = loads(response.text)

        if self.check_instock(json_response):
            product["image_urls"] += self.extract_image_url(json_response)
            product["skus"] = self.extract_skus(json_response,product["skus"])
        else:
            product["out_of_stock"] = True

        return self.check_request(product)

    def check_instock(self,json_response):
    
        response = Selector(text = json_response["value"][0][0])
        stock_status = response.css(".btn.ir.buy span::attr(content)").extract_first()

        if stock_status == "in_stock":
            return True
        else:
            return False
            
    def check_request(self,product):
    
        if product["meta"]:            
            request = product["meta"].pop()
            return request
        else:
            del product["meta"]
            return product
    
    def extract_image_url(self, json_response):
        
        image_urls = []

        for img_url in json_response["value"][1]:

            if ".jpg" in img_url or ".gif" in img_url:
                image_urls.append(self.start_urls[0] + img_url)

        return image_urls

    def extract_skus(self,json_response,product):

        response = Selector(text = json_response["value"][3])
        price_response = Selector(text = json_response["value"][0][2])
        
    
        size_label =  response.css(".select a::attr(title)").extract()
        price = price_response.css("strong::text").extract_first()
        currency = self.currency
        color = response.css(".color a::attr(title)").extract_first()

        common_sku = {
            "price": price,
            "currency": currency,
            "color": color,
            "size" : "one_size",
            "sku_id": f"one_size{color}" 
        }
    
        if size_label is None and product is None:
            return common_sku        
        elif size_label is None and product is not None:
            return product

        for size in size_label: 

            sku = common_sku.copy()
            sku["size"] = size
            sku["sku_id"] = f"{size}{color}" 

            product[sku["sku_id"]] = sku.copy()
            
        return product

    def extract_raw_description(self, response):
        return response.css(".section.about.description p::text").extract_first("").strip()

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
