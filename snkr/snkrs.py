# -*- coding: utf-8 -*-
import scrapy
from ..items import SnkrsItem


class SnkrsSpider(scrapy.Spider):
    name = 'snkrs'
    allowed_domains = ['snkrs.com']
    start_urls = ['http://snkrs.com/en/']

    def parse(self, response):
        men_link = response.css('li.li-niveau1.advtm_menu_2.sub > a.a-niveau1::attr(href)').extract_first()
        women_link = response.css('li.li-niveau1.advtm_menu_3.sub > a.a-niveau1::attr(href)').extract_first()
        skate = response.css('li.li-niveau1.advtm_menu_4.menuHaveNoMobileSubMenu' +
        ' > a.a-niveau1::attr(href)').extract_first()
        life_style = response.css('li.li-niveau1.advtm_menu_5.menuHaveNoMobileSubMenu' +
        ' > a.a-niveau1::attr(href)').extract_first() 
        if men_link:
        	print(men_link)
        	yield response.follow(men_link, callback=self.men_list_page)
        if women_link:
            print(women_link)
            yield response.follow(women_link, callback=self.women_list_page)
        if skate:
            print(skate)
            yield response.follow(skate, callback=self.skate_list_page)
        if life_style:
            print(life_style)
            yield response.follow(life_style, callback=self.life_style_list_page)

    def men_list_page(self,response):
    	urls = response.css('ul.product_list.grid.row' +
        ' >.ajax_block_product.block_home.col-xs-6.col-sm-4.col-md-3' +
        ' > .product-container > .left-block > .product-image-container' +
        ' > .product_img_link::attr(href)').extract()
    	for url in urls:
    		print(url)
    		yield response.follow(url, callback=self.product_page)

    def women_list_page(self,response):
        urls = response.css('ul.product_list.grid.row' +
        ' > .ajax_block_product.block_home.col-xs-6.col-sm-4.col-md-3' +
        ' > .product-container > .left-block > .product-image-container' +
        ' > .product_img_link::attr(href)').extract()
        for url in urls:
            print(url)
            yield response.follow(url, callback=self.product_page)

    def skate_list_page(self,response):
        urls = response.css('ul.product_list.grid.row' +
        ' > .ajax_block_product.block_home.col-xs-6.col-sm-4.col-md-3' +
        ' > .product-container > .left-block > .product-image-container' +
        ' > .product_img_link::attr(href)').extract()
        for url in urls:
            print(url)
            yield response.follow(url, callback=self.product_page)

    def life_style_list_page(self,response):
        urls = response.css('ul.product_list.grid.row' +
        ' > .ajax_block_product.block_home.col-xs-6.col-sm-4.col-md-3' +
        ' > .product-container > .left-block > .product-image-container' +
        ' > .product_img_link::attr(href)').extract()
        for url in urls:
            print(url)
            yield response.follow(url, callback=self.product_page)

    def product_page(self,response):
    	items = SnkrsItem()

    	items['retailer_sku'] = response.css('div.nosto_product > span.product_id::text').get()
        items['brand'] = response.css('div.nosto_product > span.brand::text').get()
        items['category'] = response.css('div.nosto_product > span.category::text').re(r'Men .*')
        items['description'] = response.css('div.rte > p::text').extract()
        items['gender'] = response.css('div.nosto_product > span.category').re_first(r'Men')
        items['url'] = response.css('div.nosto_product > span.url::text').get()
        items['name'] = response.css('div.nosto_product > span.name::text').get()
        items['image_urls'] = response.css('div.nosto_product > .image_url::text').extract()
        items['image_urls'].extend(response.css('div.nosto_product > .alternate_image_url::text').extract())
        shoes_name = response.css('div.nosto_product > span.name::text').re_first(r'- .*')
        for sizes in response.css('span.units_container > .size_EU::text').extract():
            items['skus'] = {shoes_name + "_".join(sizes):
            {
                "colour" : shoes_name,
                "currency" : response.css('div.nosto_product > span.price_currency_code::text').get(),
                "price" : response.css('div.nosto_product > span.price::text').get(),
                "size" : sizes
            },
            }

    	yield items
