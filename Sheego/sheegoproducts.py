# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sheego.items import Product


class SheegoproductsSpider(CrawlSpider):
    name = 'sheegoproducts'
    allowed_domains = ['sheego.de']
    start_urls = ['http://sheego.de/']
    rules = (
            Rule(LinkExtractor(
                allow=('(\w)*'),
                deny=('/neu/', '/inspiration/',
                 '/damenmode-sale/', '/magazin/'),
                restrict_css='.cj-mainnav'),
                callback='parse_categories',),
            )
    
    def parse_categories(self, response):
        categories = self.get_categories(response)
        for category in categories:
            url = response.urljoin("?filterSHKategorie={}".format(category))
            yield scrapy.Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        product_urls = self.get_products_urls(response)
        for url in product_urls:
            category = self.extract_category(url)
            yield scrapy.Request(url=url, callback=self.parse_product,
                                 meta={'category': category})
        next_page_url = self.get_next_page(response)
        yield scrapy.Request(url=url, callback=self.parse_listing)

    def parse_product(self, response):
        product = Product()
        product['Id'] = self.extract_product_id(response.url)
        product['name'] = self.get_product_name(response)
        product['category'] = response.meta['category']
        product['brand'] = "sheego"
        product['urls'] = [response.url]
        product['product_imgs'] = self.get_product_imgs(response)
        product['description'] = self.get_product_desc(response)
        product['care'] = self.get_prodct_care(response)
    
    def get_categories(self, response):
        return response.css(
            ".form-group--checkbox input::attr(value)").extract()

    def get_products_urls(self, response):
        return response.css(
            ".js-product__link::attr(href)").extract()

    def extract_category(self, url):
        return (url[url.find("=")+1:(url.find("&"))] or
                url[url.find("=")+1:])

    def get_next_page(self, response):
        return response.urljoin(
            response.css(".js-next::attr(href)").extract_first())

    def get_product_imgs(self, response):
        imgs = response.css(
            ".p-details__image__thumb__container a::attr(href)").extract()
        imgs = [response.urljoin(img) for img in imgs]
        return response.urljoin(imgs)
    
    def get_product_name(self, url):
        name = response.css(".at-dv-title-box h1 span::text").extract()
        name = self.clean_input(name)
        return ''.join(str(splited_name) for splited_name in name)
    
    def extract_product_id(self, url):
        return url[url.find("_")+1:(url.find("."))]
    
    def get_product_desc(self, response):
        desc = response.css(".details__box__desc p::text").extract()
        desc = self.clean_input(desc)
        return ''.join(str(splited_desc) for splited_desc in desc)
    
    def get_prodct_care(self, response):
        care = response.css(".p-details__material td::text").extract()
        care = self.clean_input(care)
        return ''.join(str(splited_care) for splited_care in care)

    def get_product_colors(self, response):
        pass

    def get_product_sizes(self, response):
        pass
    
    def get_product_skuz(self, response):
        pass
    
    def get_product_viariant(self, response):
        pass

    def has_product_variant(self, response):
        pass
    
    def get_color_name(self, response):
        color = response.css(".p-details__variants p::text").extract()
        color = self.clean_input(color)
        return ''.join(str(splited_color) for splited_color in color)

    def clean_input(self, my_input):
        if type(my_input) is list:
            my_input = [txt.strip() for txt in my_input]
            return list(filter(lambda txt: txt != '', my_input))
