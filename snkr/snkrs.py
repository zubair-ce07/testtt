# -*- coding: utf-8 -*-
import scrapy
from ..items import SnkrSpiderItem


class SnkrsSpider(scrapy.Spider):
    name = 'snkrs'
    allowed_domains = ['snkrs.com']
    start_urls = ['https://www.snkrs.com/en/']

    def parse(self, response):
        men = response.css('a.a-niveau1::attr(href)').re_first(r'https://www.snkrs.com/en/263-men')
        yield response.follow(men, callback=self.men_snkr_link)

    def men_snkr_link(self,response):
    	men_snkr = response.css('a::attr(href)').re_first(r'https://www.snkrs.com/en/2-sneakers')
    	yield response.follow(men_snkr, callback=self.adidas_men)

    def adidas_men(self,response):
    	adidas = response.css('a::attr(href)').re_first(r'https://www.snkrs.com/en/adidas/adidas-hu-nmd-hu-made-whitescarlet-10195.html')
    	yield response.follow(adidas, callback=self.adidas_white_scarlet)

    def adidas_white_scarlet(self,response):
        items =  SnkrSpiderItem()

        items['retailer_sku'] = response.css('div.nosto_product > span.product_id::text').get()
        items['brand'] = response.css('div.nosto_product > span.brand::text').get()
        items['category'] = response.css('div.nosto_product > span.category::text').re(r'Men .*')
        items['description'] = response.css('p::text').re(r'- .*')
        items['gender'] = response.css('li > a::text').re_first(r'Men')
        items['url'] = response.css('div.nosto_product > span.url::text').get()
        items['name'] = response.css('div.nosto_product > span.name::text').get()
        items['image_urls'] = response.css('a::attr(href)').re(r'https://media.*')
        items['skus'] = {
                'White/Scarlet_37 1/3' : {
                    'colour' : response.css('div.nosto_product > span.name::text').re_first(r'White/Scarlet'),
                    "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                    "price" : response.css('div.nosto_product > span.price::text').get(),
                    "size" : response.css('span.units_container > span.size_EU::text').re_first(r'37 .*')
                },
                'White/Scarlet_38' : {
                    'colour' : response.css('div.nosto_product > span.name::text').re_first(r'White/Scarlet'),
                    "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                    "price" : response.css('div.nosto_product > span.price::text').get(),
                    "size" : response.css('span.units_container > span.size_EU::text').re_first(r'38')
                },
                "White/Scarlet_38 2/3" : {
                   "colour" : response.css('div.nosto_product > span.name::text').re_first(r'White/Scarlet'),
                   "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                   "price" : response.css('div.nosto_product > span.price::text').get(),
                   "size" : response.css('span.units_container > span.size_EU::text').re_first(r'38 .2*')
               },
               "White/Scarlet_39 1/3" : {
                   "colour" : response.css('div.nosto_product > span.name::text').re_first(r'White/Scarlet'),
                   "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                   "price" : response.css('div.nosto_product > span.price::text').get(),
                   "size" : response.css('span.units_container > span.size_EU::text').re_first(r'39 .*')
               },
               "White/Scarlet_40" : {
                   "colour" : response.css('div.nosto_product > span.name::text').re_first(r'White/Scarlet'),
                   "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                   "price" : response.css('div.nosto_product > span.price::text').get(),
                   "size" : response.css('span.units_container > span.size_EU::text').re_first(r'40')
               },
               "White/Scarlet_40 2/3" : {
                   "colour" : response.css('div.nosto_product > span.name::text').re_first(r'White/Scarlet'),
                   "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                   "price" : response.css('div.nosto_product > span.price::text').get(),
                   "size" : response.css('span.units_container > span.size_EU::text').re_first(r'40 .2*')
               },
               "White/Scarlet_41 1/3" : {
                   "colour" : response.css('div.nosto_product > span.name::text').re_first(r'White/Scarlet'),
                   "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                   "price" : response.css('div.nosto_product > span.price::text').get(),
                   "size" : response.css('span.units_container > span.size_EU::text').re_first(r'41 .*')
               },
               "White/Scarlet_42 " : {
                    "colour" : response.css('div.nosto_product > span.name::text').re_first(r'White/Scarlet'),
                    "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                    "price" : response.css('div.nosto_product > span.price::text').get(),
                    "size" : response.css('span.units_container > span.size_EU::text').re_first(r'42')
                },
               "White/Scarlet_42 2/3" : {
                   "colour" : response.css('div.nosto_product > span.name::text').re_first(r'White/Scarlet'),
                   "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                   "price" : response.css('div.nosto_product > span.price::text').get(),
                   "size" : response.css('span.units_container > span.size_EU::text').re_first(r'42 .2*')
               }
            }
        yield items
     	