# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class OrsayproductSpider(CrawlSpider):
    name = 'orsayproducts'
    allowed_domains = ['orsay.com']
    start_urls = ['http://www.orsay.com/de-de/']
    rules = (
                Rule(LinkExtractor(
                    allow=(r'([\w \W])*/produkte/\Z',)), follow=True),
                Rule(LinkExtractor(
                    allow=(r'([\w \W])*/produkte/([\w \W])*',)),
                    callback='parse_listings', follow=True),
                Rule(LinkExtractor(
                    allow=(r'([\w \W])*.html\Z',)),
                    callback='parse_product', follow=True),
            )

    def parse_listings(self, response):
        next_page = self.get_next_page(response)
        if next_page:
            yield scrapy.Request(
                    url=next_page, callback=self.parse_listings)

    def parse_product(self, response):
        product_item = {
            "brand": "Orsay",
            "description": self.get_product_description(response),
            "product_imgs": self.get_product_imgs(response),
            "category": (self.get_product_details(response))["categoryName"],
            "name": (self.get_product_details(response))["name"],
            "skus": self.convert_gen_to_dict(self.get_product_skus(response)),
            "urls": [response.request.url],
            "care": [self.get_care_text(response)]
        }
        colors_to_follow = self.has_more_colors(response)
        if len(colors_to_follow) > 1:
            url = self.get_color_url(colors_to_follow)
            yield scrapy.Request(
                    url=url, callback=self.get_product_skus,
                    meta={'colors_list': colors_to_follow,
                          'item':  product_item})
        else:
            yield product_item

    def clean_text(self, text):
        text = [txt.strip() for txt in text]
        return list(filter(lambda txt: txt != '', text))
                
    def get_number(self, text_str):
        return re.findall(r'\d+', text_str)[0]

    def has_numbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def get_total_products(self, response):
        total_products = response.css(
                ".load-more-progress-label::text").extract()
        for txt in total_products:
            if self.has_numbers(txt):
                return self.get_number(txt)
    
    def get_next_page(self, response):
        product_url = response.url
        if not self.has_numbers(response.url):
            product_url = response.urljoin("?sz=72")    
        total_products = self.get_total_products(response)
        listed_products = self.get_number(product_url)
        if (int(total_products) < int(listed_products) 
                and int(total_products) > 72):
            return response.url.replace(
                    listed_products, str(int(listed_products)+72))
        else:
            return None

    def get_product_imgs(self, response):
        product_imgs = response.css(".productthumbnail::attr(src)").extract()
        return ([img.replace("sw=100", "sw=700").replace(
                "sh=150", "sh=750") for img in product_imgs])

    def get_product_details(self, response):
        details = response.css(".js-product-content-gtm").extract_first()
        product_data = details[details.find("{"):(details.find("}")+1)]
        return json.loads(product_data)

    def get_product_colors(self, response):
        colors = response.css(".swatches .selected img::attr(alt)").extract()
        return [color[color.find("- ")+2:] for color in colors]
    
    def get_product_sizes(self, response):
        sizes = response.css(".swatches li.selectable a::text").extract()
        return [size.replace("\n", "") for size in sizes if size is not "\n"]

    def get_product_description(self, response):
        description = response.css(".product-details div::text").extract()
        return self.clean_text(description)

    def get_product_skus(self, response):
        product_details = self.get_product_details(response)
        colors = self.get_product_colors(response)
        sizes = self.get_product_sizes(response)
        sub_skus = {}
        for size in sizes:
            for color in colors:
                skus = {
                    product_details["productId"]+"_"+size: {
                        "color": color,
                        "currency": product_details["currency_code"],
                        "price": product_details["netPrice"],
                        "size": size
                    }
                }
                sub_skus.update(skus)
        product_item = None
        if 'item' in response.meta:
            product_item = response.meta['item']
            product_item['skus'].update(sub_skus)
            response.meta['item']['urls'].append(response.url)
        else:
            yield sub_skus
        if 'colors_list' in response.meta:
            if len(response.meta['colors_list']) == 0:
                yield response.meta['item']
            else:
                colors_to_follow = response.meta['colors_list']
                url = self.get_color_url(colors_to_follow)
                yield scrapy.Request(
                        url=url, callback=self.get_product_skus,
                        meta={'colors_list': colors_to_follow,
                              'item':  product_item})
            
    def get_care_text(self, response):
        care_text = response.css(
                    ".product-material div::text,.product-material p::text "
                    ).extract()
        care_text.extend(response.css(".content-asset p::text").extract())
        return self.clean_text(care_text)
    
    def has_more_colors(self, response):
        colors_to_follow = response.css(
            ".color .selectable a::attr(href)").extract()
        return colors_to_follow
    
    def get_color_url(self, colors_to_follow):
        url = colors_to_follow[0]
        colors_to_follow.pop(0)
        return url
        
    def convert_gen_to_dict(self, gen_obj):
        for obj in gen_obj:
            return obj
