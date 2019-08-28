from scrapy import Request, FormRequest, Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from json import loads, dumps

from ..items import StartItem

class Khelapider(CrawlSpider):

    name = "Khela"
    currency = 'Dollars'
    start_urls = ['https://www.khelf.com.br/']
    listings_css = [".menu-categorias", ".link[rel='nex']::attr(href)"]

    rules = (
        Rule(LinkExtractor(restrict_css = listings_css),callback = "Parse"),
    )

    def Parse(self, response):

        for link in response.css(".list-products li"):

            product_link = link.css("a[class='change link url']::attr(href)").extract_first()
            color_tag =  link.css(".skus.p-v.color a::attr(color-code)").extract()

            if product_link is not None:
                request =  Request(url=product_link,method='POST',callback = self.product_parse)
                request.meta["color_tag"] = color_tag
                yield request

    def product_parse(self,response):

        product = StartItem()

        product['retailer_sku'] = self.extract_retailer_sku(response)
        product['brand'] = self.name
        product['url'] = response.url
        product['name'] = self.extract_name(response)
        product["price"] = self.extract_price(response)
        product["gender"] = self.extract_gender(product["name"])
        product["image_urls"] = []
        product['skus'] = []
        product["meta"] = self.extract_requests(product,response)

        raw_description = self.extract_raw_description(response)

        if raw_description is not None:
            product["care"] = self.extract_care(raw_description)
            product["description"] = self.extract_description(raw_description)

        yield self.check_request(product)

    def extract_retailer_sku(self,response):
        return response.css(".fab-cod span::attr(content)").extract_first().split(":")[1] 

    def extract_name(self, response):
        return response.css(".name.fn::text").extract_first("").strip()

    def extract_price(self,response):
        return response.css(".price.sale strong::text").extract_first()

    def extract_gender(self,product_name):

        gender_list = ["Masculina","Masculino","mulheres","infantial","Infantil","Feminino","Feminina","FEMININO"]

        for gender in gender_list:

            if gender in product_name:
                return gender

        return "unisex"
    
    def extract_requests(self,product,response):

        requets = []

        color_data ={
            "ProdutoCodigo":None,"CarValorCodigo1":None,"CarValorCodigo2":"0",
            "CarValorCodigo3": "0","CarValorCodigo4":"0","CarValorCodigo5":"0"
        }
        color_header={
                'X-AjaxPro-Method': 'DisponibilidadeSKU',
                'Referer': None
        }

        for id in response.meta["color_tag"]:

            color_header["Referer"] = response.url
            color_data["CarValorCodigo1"] = id
            color_data["ProdutoCodigo"] = self.extract_ProdutoCodigo(response)

            request = Request(url='https://www.khelf.com.br/ajaxpro/IKCLojaMaster.detalhes,Khelf.ashx',
                        method='POST',headers = color_header, body=dumps(color_data), callback = self.update_product) 
            request.meta['product'] = product
            requets.append(request)

        return requets

    def extract_raw_description(self, response):
        return response.css(".section.about.description p::text").extract()

    def extract_care(self,raw_description):
    
        care_list = [
            "malha de poliamida","poliéster","algodão","pele","Cuidado","resistência","sentindo-me",
            "casual","confortável","couro","tecido","protecção","material","conforto","confortável"
        ]

        care_list = []

        for line in raw_description:
            for care in care_list:

                if care in line:
                    care_list.append(line)
                    raw_description.replace(line,"")

        return care_list

    def extract_description(self,description):
        return description
        
    def update_product(self,response):

        product = response.meta["product"]
        json_response = loads(response.text)
        new_response = Selector(text =json_response["value"][3])

        product['image_urls'] += self.extract_image_url(json_response)
        product['skus'].append(self.extract_skus(product["price"],new_response))

        return self.check_request(product)

    def check_request(self,product):

        if product['meta']:            
            request = product['meta'].pop()
            return request
        else:
            del product['meta']
            return product

    def extract_id(self,response):
        return response.css(".color img::attr(id)").extract()

    def extract_ProdutoCodigo(self,response):
        return response.css("input[id='ProdutoCodigo']::attr(value)").extract_first()

    def extract_image_url(self, json_response):
    
        imgs = []

        for img_url in json_response["value"][1]:

            if ".jpg" in img_url or ".gif" in img_url:
                imgs.append(self.start_urls[0] + img_url)

        return imgs

    def extract_skus(self,price,size):

        skus = []

        price = price
        currency = self.currency
        size_label =  size.css(".select a::text").extract()
        sku_id = size_label

        common_sku = {
            "price": price,
            "currency": currency,
            "sku_id": sku_id
        }

        if size_label is None:
            return common_sku

        if sku_id is None:
            common_sku["sku_id"] = size_label

        for size in size_label:

            sku = {
                "size": size
            }
            sku.update(common_sku)
            skus.append(sku)

        return skus

