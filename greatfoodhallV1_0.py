# -*- coding: utf-8 -*-
import scrapy
import logging as log


class Greatfoodhallv10Spider(scrapy.Spider):
    name = 'greatfoodhallV1.0'
    allowed_domains = ['greatfoodhall.com']
    start_urls = ['http://www.greatfoodhall.com/eshop/OnlieShopLanding.do']
    #start_urls = ['http://www.greatfoodhall.com/eshop/ShowProductPage.do?service=direct&service=1&service=ProductList.%24ProductView.%24DirectLink&sp=l44806']
    count = 0
    products_links = []
    
    def parse(self, response):
        
        self.online_nav_links=response.xpath(
                    '//div[contains(@class, "item")]/a/@href'
                ).extract()

        yield scrapy.Request(
            url=response.urljoin(self.online_nav_links.pop()), 
                callback=self.get_products_links
            )
             
    def get_products_links(self, response):
        
        self.products_links += response.xpath(
                    '//div[contains(@class, "productTmb")]//a/@href'
                ).extract()

        try:
            curr_items=self.get_curr_items(response)
            total_items=self.get_total_items(response)
            
            if curr_items < total_items:   
                self.count += 1
                req = scrapy.Request(url=(response.url).split('?')[0] 
                                        + "?curPage_1=" 
                                        + str(self.count+1), 
                            callback=self.get_products_links,
                            dont_filter=True)
                yield req
            
            elif self.online_nav_links:

                self.count=0

                yield scrapy.Request(
                    url='http://www.greatfoodhall.com/eshop/'
                        +self.online_nav_links.pop(), 
                            callback=self.get_products_links)
            else:
                self.products_links = list(set(self.products_links))

                for url in self.products_links:
                    yield scrapy.Request(url=url,
                            callback = self.get_item_data)
        except:
            log.warning('\n\nFound Error in --> ' + response.url+ '\n\n')
    
    def get_item_data(self, response):
        yield {
            'company' : self.get_company_name(response),
            'product Name' : self.get_product_name(response),
            'weight' : self.get_weight(response),
            'price' : self.get_price(response),
            'nuterition info' : self.get_nutrition_info(response),
            'images' : 'http://www.greatfoodhall.com/eshop'+self.get_product_img_url(response),
            'category' : self.get_category(response),
            'country flag' : 'http://www.greatfoodhall.com/eshop'+self.get_country(response),
            'product url' : response.url
        }


######################### Data Getters Defined Below #########################        

    def get_curr_items(self, response):
        return int((response.xpath(
            '//b[contains(@class, "currentPage")]/text()'
        ).extract_first()).split('-')[-1])
    
    def get_total_items(self, response):
        return int(response.xpath(
            '//b[contains(@class, "totalItem")]/text()'
        ).extract_first())

    def get_company_name(self, response):
        return response.xpath(
            '//h1[contains(@class, "pL6")]/text()'
        ).extract_first(default='N/A')
    
    def get_product_name(self, response):
        return response.xpath(
            '//p[contains(@class, "description")]/text()'
        ).extract_first(default='N/A')
    
    def get_weight(self, response):
        return response.xpath(
            '//span[contains(@class, "pL6")]/text()'
        ).extract_first(default='N/A')
    
    def get_price(self, response):
        return response.xpath(
            '//div[contains(@class, "itemOrgPrice2")]/text()'
        ).extract_first()
    
    def get_country(self, response):
        return response.xpath(
            '//img[contains(@class, "flag")]/@src'
        ).extract_first(default='N/A')
    
    def get_product_img_url(self, response):
        return response.xpath(
            '//div[contains(@class, "productPhoto")]/img/@src'
        ).extract_first(default='N/A')
    
    def get_nutrition_info(self, response):
        return response.xpath(
            '//div[contains(@id, "nutrition")]//td/text()'
        ).extract_first(default='N/A')
    
    def get_category(self, response):
        try:
            return response.xpath(
                '//a[contains(@class, "highlight")]/text()'
            )[-1].extract_first(default='N/A')  
        except:
            pass
            return 'None'
    