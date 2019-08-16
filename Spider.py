import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import StartItem



class MySpider(CrawlSpider):

    name = "derek-rose"
    start_urls = ['https://www.derek-rose.com/kids/childrens-clothing/kids-pyjamas/kids-pyjamas-paris-16-cotton-jacquard-navy.html'
    ]

    def parse(self, response):

        items = StartItem()
        items['retailer_sku'] = self.get_retailer_sku(response)
        items['gender'] = "boy"
        items['brand'] = "derek rose"
        items['url'] = self.get_url(response)
        items['name'] = self.get_name(response)
        items['description'] = self.get_description(response)
        items['care'] = self.get_care(response)
        items['image_urls'] = self.get_image_url(response)
        items['skus'] = self.get_skus(response)
        yield items


    def get_retailer_sku(self,response):

        return response.css(".product-details__sku::text").extract_first().split(": ")[1]

    def get_gender(self, response):

        return response.css(".product-details__attrs::text").extract()

    def get_url(self, response):

        return self.start_urls

    def get_name(self, response):

        return response.css(".product-details__sub::text").extract_first()

    def get_description(self, response):

        return response.css(".product-details__short-description span::text").extract_first("").strip()

    def get_care(self, response):

        care = response.css(".product-details__attrs:last-child")
        return care.css(".product-details__attrs td::text").extract()

    def get_image_url(self, response):

        return  response.css(".product-cloudzoom::attr(src)").extract()

    def get_skus(self, response):

        sku = []

        price = response.css(".price::text").extract_first()
        currency = 'GDP'
        size = response.css(".product-details__option-items a::attr(data-size-label)").extract()
        sku_id = response.css(".product-details__option-items a::attr(data-product-id)").extract()
        
        for get_size,get_id in zip(size,sku_id):

            dic = {
                "price": price,
                "currency": currency,
                "size": get_size,
                "sku-id": get_id
            }
            sku.append(dic)


        return sku
         
        