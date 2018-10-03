# -*- coding: utf-8 -*-
import json
import scrapy
from .lornajane_dataGetter import dataGetterClass as dgc


class Lornajanev10Spider(scrapy.Spider):
    name = 'lornajaneV1.0'
    allowed_domains = ['lornajane.sg']
    start_urls = ['https://www.lornajane.sg/c-Shop-All']
    
    item_urls = []
    dgc_obj = dgc()
    count = 0
    total = 0

    def parse(self, response):

        self.total = self.dgc_obj.get_total_count(response)
        self.log('\n\n\n'+ str(self.total))
        links = response.xpath(
            '//div[contains(@class, "product-item")]//a/@href'
        ).extract()
        
        self.item_urls += links

        if self.count < self.total:
            url = 'https://www.lornajane.sg/c-Shop-All?partitial=true'\
            +'&q=&sort=&count=1'\
            +'&page='+str(self.count)\
            +'&numberOfPages=22&totalNumberOfResults=436'
            self.count += 20
            req = scrapy.Request(url=url, callback=self.get_links)
            yield req

    def get_links(self, response):
        json_dict = json.loads(response.text) 
        products_list = json_dict['productsGTM']

        for item in products_list:
            url = item['id']
            self.item_urls.append(url)

        
        if self.count < self.total:
            url = 'https://www.lornajane.sg/c-Shop-All?partitial=true'\
            +'&q=&sort=&count=1'\
            +'&page='+ str(self.count)\
            +'&numberOfPages=22&totalNumberOfResults=434'
            self.count += 20
            
            req = scrapy.Request(url=url, callback=self.get_links)
            yield req
        
        else:
            self.item_urls = list(set(self.item_urls))
            self.log(str(len(self.item_urls)))
            for link in self.item_urls:
                yield scrapy.Request(url='https://www.lornajane.sg/p-' + link,
                                    callback=self.get_data,  
                                    dont_filter=True)
        
    def get_data(self, response):
        yield {
            'brand' : 'Lornajane',
            'care' : self.dgc_obj.get_care(response),
            'category' : self.dgc_obj.get_category(response) ,
            'image-urls' : self.dgc_obj.get_image_urls(response),
            'name' :  self.dgc_obj.get_name(response),
            'skus' : {
                'color' : self.dgc_obj.get_color(response),
                'price' : self.dgc_obj.get_price(response),
                'currency' : self.dgc_obj.get_currency(response),
                'size' : self.dgc_obj.get_size(response) 
                }
            }