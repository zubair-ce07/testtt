from datetime import datetime

from scrapy.http.request import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

import json

from khelf.items import KhelfItem


class KhelfSpider(CrawlSpider):
    name = 'khelf'
    start_urls = ['https://www.khelf.com.br']
    rules = [
        Rule(LinkExtractor(restrict_css=(['#nav > li > a', '.next']))),
        Rule(LinkExtractor(restrict_css=(['.url'])), callback="parse_product")
    ]

    token = None
    product_code = None

    API = "https://www.khelf.com.br/ajaxpro/IKCLojaMaster.detalhes,IKCLojaMaster%202.2.ashx"

    def parse_product(self, response):
        product = KhelfItem()
        product['market'] = "BR"
        product['retailer'] = "Khelf-BR"
        product['description'] = self.description(response)
        product['product_name'] = self.product_name(response)
        product['category'] = self.product_category(response)
        product['retailer_sku'] = self.product_retailer_sku(response)
        product['pending_requests'] = []
        product['date'] = datetime.now().timestamp()
        product['price'] = self.price(response)
        product['currency'] = self.currency(response)
        product['lang'] = self.lang(response)
        product['brand'] = self.brand(response)
        product['gender'] = self.gender(response)
        product['url'] = response.url
        product['original_url'] = response.url

        self.token = self.get_token(response)
        self.product_code = self.get_product_code(response)

        product['pending_requests'].append(self.images_request(product))
        product['pending_requests'].append(self.skus_request(product))

        yield self.resolve_requests(product)

    def parse_skus(self, response):
        product = response.meta['product']
        product['skus'] = {}
        response = Selector(text=json.loads(response.body)['value'][0])
        product_colour = self.get_colours(response)
        product_sku_sizes = self.get_sizes(response, product_colour)
        for color in product_colour:
            for sku_size in product_sku_sizes:
                sku_size = sku_size.strip()
                product['skus'][f"{product['retailer_sku']}|{color}|{sku_size}"] = {
                    "colour": color,
                    "size": sku_size,
                    "price": product['price'],
                    "currency": product['currency']
                }
        return self.resolve_requests(product)

    def parse_images(self, response):
        product = response.meta['product']
        product['image_urls'] = []
        for img in json.loads(response.body)['value'][1]:
            if (".jpg" in img or ".gif" in img) and (img not in product['image_urls']):
                product['image_urls'].append(img)
        return self.resolve_requests(product)

    def skus_request(self, product):
        headers = {
            "X-AjaxPro-Method": "CarregaSKU",
            "X-AjaxPro-Token": self.token
        }

        data = {
            "ColorCode": "0",
            "ProdutoCodigo": self.product_code,
            "isRequiredCustomization": False,
        }
        request = Request(url=self.API, method="POST", headers=headers, body=json.dumps(data), callback=self.parse_skus)
        request.meta["product"] = product
        return request

    def images_request(self, product):
        headers = {
            "X-AjaxPro-Method": "DisponibilidadeSKU",
            "X-AjaxPro-Token": self.token
        }
        data = {
            "CarValorCodigo1": "0", "CarValorCodigo2": "0",
            "CarValorCodigo3": "0", "CarValorCodigo4": "0", "CarValorCodigo5": "0",
            "ProdutoCodigo": self.product_code,
            "isRequiredCustomization": False,
            "recurrencyId": "0"
        }
        request = Request(url=self.API, method="POST", headers=headers, body=json.dumps(data), callback=self.parse_images)
        request.meta["product"] = product
        return request

    def resolve_requests(self, product):
        if product["pending_requests"]:
            request = product["pending_requests"].pop()
            return request

        del product["pending_requests"]
        return product

    def get_product_code(self, response):
        return response.css("#ProdutoCodigo::attr(value)").get().strip()

    def product_name(self, response):
        return response.css("#productName::text").get().strip()

    def product_retailer_sku(self, response):
        return response.css("#productInternalCode::text").get().strip()

    def description(self, response):
        return response.css("#descriptionContent::text").get().strip()

    def product_category(self, response):
        links = response.css("#breadcrumbs .link::text").getall()[:-1]
        return links

    def price(self, response):
        return response.css("#lblPrecoPor span::text").get()

    def lang(self, response):
        return response.xpath("//html/@lang").get()

    def brand(self, response):
        return response.xpath("//meta[@name='author']/@content").get()

    def currency(self, response):
        return response.css('.priceCurrency::text').get()

    def get_token(self, response):
        script = response.xpath('//script[@type="text/javascript"][contains(.,"AjaxPro")]')
        return script.re(r'AjaxPro.token = "(\w+)";').pop()

    def gender(self, response):
        if "masculinas" in response.url or "masculino" in response.url:
            gender = "masculino"
        elif "feminino" in response.url:
            gender = "feminino"
        else:
            gender = "unissex"
        return gender

    def get_colours(self, response):
        return response.css(".SKU::attr(alt)").getall()

    def get_sizes(self, response, colors):
        selects = response.css(".select a::attr(title)").getall()
        return list(set(selects) - set(colors))
