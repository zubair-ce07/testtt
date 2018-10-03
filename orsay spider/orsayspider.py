import scrapy
import logging
import w3lib.url

from .productclass import Product
from .dataGetter import DataGetterClass

class OrsaySpider(scrapy.Spider):

    data_getter_class = DataGetterClass()
    name = 'orsayspider'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/produkte/']

    def parse(self, response):
        """
        links List to follow from main page to next 
        products page
        """
        main_page_links = response.xpath(
            '//a[contains(@class, "navigation-link level-3")]/@href'
                        ).extract()

        for link in main_page_links:
            yield scrapy.Request(response.urljoin(link), 
                                callback=self.parse_product_page, 
                                dont_filter=True)
        
    
    def parse_product_page(self, response):
        product_page_links = response.xpath(
            '//a[contains(@class, "thumb-link")]/@href'
        ).extract()

        for link in product_page_links:
            yield response.follow(url=link, 
                                callback=self.parse_product_details, 
                                dont_filter=True)
            
        load_more = response.xpath(
            '//div[contains(@class, "load-next-placeholder")]'
            ).extract_first()

        if load_more:
            temp = int(w3lib.url.url_query_parameter(response.url, "sz"))
            
            if temp:
                link = w3lib.url.add_or_replace_parameter(
                                            response, 'sz', (temp+72))
            else:
                link = response.url + '?sz=72'
                
            yield scrapy.Request(link, callback=self.parse_product_page)

    def parse_product_details(self, response):
        product = Product(
            brand = 'orsay',
            care = self.data_getter_class.product_care(response),
            category = self.data_getter_class.product_category(response),
            discription = self.data_getter_class.product_discription(response),
            image_urls = self.data_getter_class.product_image_urls(response),
            retailer_skus = self.data_getter_class.sku_id(
                                                        response),
            name = self.data_getter_class.product_name(response),
            skus = {
                self.data_getter_class.sku_id(response) : {
                'color' :self.data_getter_class.product_selected_color(response),
                'price' : self.data_getter_class.product_price(response),
                'currency' : self.data_getter_class.product_currency(response),
                'size' : self.data_getter_class.product_size(response)
                }
            },
            url = response.url
        )
        color_list_link = response.xpath(
                            '//ul[contains(@class, "swatches color")]/'\
                            'li[not(contains(@class, "selected"))]//a/@href'
                        ).extract()
        
        return self.next_color_link(color_list_link, product)

    def product_skus(self, response):
        item = response.meta['item']
        color_list_link = response.meta['link']
        item_details = {
            'color' : self.data_getter_class.product_selected_color(response),
            'price' : self.data_getter_class.product_price(response),
            'currency' : self.data_getter_class.product_currency(response),
            'size' : self.data_getter_class.product_size(response)
            }
        item['skus'][self.data_getter_class.sku_id(response)] = item_details
        item['image_urls'] += self.data_getter_class.product_image_urls(response)
        
        return self.next_color_link(color_list_link, item)

    def next_color_link(self, color_list_link, item):    
        if color_list_link:
            link = color_list_link.pop()
            req = scrapy.Request(url=link, callback=self.product_skus)
            req.meta['item'] = item
            req.meta['link'] = color_list_link
            yield req
        else:
            yield item
