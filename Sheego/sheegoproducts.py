# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sheego.items import Product
from scrapy import Request


class SheegoproductsSpider(CrawlSpider):
    name = 'sheegoproducts'
    allowed_domains = ['sheego.de']
    start_urls = ['http://sheego.de/']
    rules = (
            Rule(LinkExtractor(
                deny=('/neu/', '/inspiration/',
                 '/damenmode-sale/', '/magazin/'),
                restrict_css='.cj-mainnav'),
                callback='parse_categories',),
            )
    
    def parse_categories(self, response):
        categories = self.get_categories(response)
        for category in categories:
            url = response.urljoin("?filterSHKategorie={}".format(category))
            yield Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        for url in self.get_products_urls(response):
            category = self.extract_category(url)
            yield Request(
                url=response.urljoin(url), callback=self.parse_product,
                meta={'category': category})
        next_page_url = self.get_next_page(response)
        if next_page_url:
            yield Request(url=next_page_url, callback=self.parse_listing)

    def parse_product(self, response):
        product = Product()
        product_details = self.get_product_details(response)
        product['Id'] = product_details['productId']
        product['name'] = product_details['productName']
        product['category'] = response.meta['category']
        product['brand'] = "sheego"
        product['urls'] = [response.url]
        product['product_imgs'] = self.get_product_imgs(response)
        product['description'] = self.get_product_desc(response)
        product['care'] = self.get_prodct_care(response)
        product['skus'] = {}
        if product_details['productAvailability'] == 'Not-Available':
            product['out_of_stock'] = False
        else:
            product['out_of_stock'] = True
        variants = self.prepare_variants_urls(response)
        url_to_follow = self.get_varaint_url(variants)
        colors = self.get_product_colors(response)
        yield Request(
            url=url_to_follow, callback=self.get_product_viariant,
            meta={
                "product": product, "variants": variants, "colors": colors})

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
        return [response.urljoin(img) for img in imgs]
    
    def get_product_desc(self, response):
        desc = response.css(".details__box__desc p::text").extract()
        desc = self.clean_input(desc)
        return ''.join(str(splited_desc) for splited_desc in desc)
    
    def get_prodct_care(self, response):
        care = response.css(".p-details__material td::text").extract()
        care = self.clean_input(care)
        return ''.join(str(splited_care) for splited_care in care)

    def get_product_details(self, response):
        details = response.css(".js-webtrends-data").extract_first()
        product_data = details[details.find("{"):(details.find("}")+1)]
        return json.loads(product_data)

    def get_product_colors(self, response):
        colors = response.css(
            ".cj-slider__slides .js-ads-script").extract_first()
        colors = colors[colors.find("[")+1:(colors.find("]"))]
        colors = colors.replace(",", " ").replace("\'", "")
        return colors.split()
        
    def get_product_sizes(self, response):
        sizes = response.css(".at-dv-size-button::text").extract()
        return self.clean_input(sizes)
    
    def get_product_skus(self, response, color_id):
        color = self.get_color_name(response)
        sizes = self.get_product_sizes(response)
        product_details = self.get_product_details(response)
        sub_skus = {}
        for size in sizes:
            sub_skus.update({
                "{}_{}".format(color_id, size): {
                    'color': color,
                    'currency': 'EUR',
                    'size': size,
                    'price': product_details['productPrice']
                }
            })
        return sub_skus

    def get_product_viariant(self, response):
        product = response.meta['product']
        variants = response.meta['variants']
        colors = response.meta['colors']
        if not len(variants):
            yield product
        else:
            color_id = self.prepare_color_id(colors)
            skus = self.get_product_skus(response, color_id)
            product['skus'].update(skus)
            product['urls'].append(response.url)
            url_to_follow = self.get_varaint_url(variants)
            yield Request(
                url=url_to_follow, callback=self.get_product_viariant,
                meta={"product": product,
                      "variants": variants, "colors": colors})
    
    def prepare_variants_urls(self, response):
        colors = self.get_product_colors(response)
        return [response.urljoin(
                "?variantid=000000128536000{}023000".format(
                    color)) for color in colors]

    def get_varaint_url(self, variants):
        variant = variants[0]
        variants.pop(0)
        return variant
    
    def get_color_name(self, response):
        color = response.css(".p-details__variants p::text").extract()
        color = self.clean_input(color)
        return ''.join(str(splited_color) for splited_color in color)
    
    def prepare_color_id(self, colors):
        color = colors[0]
        colors.pop(0)
        return "00000128536000{}023000".format(color)

    def clean_input(self, my_input):
        if type(my_input) is list:
            my_input = [txt.strip() for txt in my_input]
            return list(filter(lambda txt: txt != '', my_input))
