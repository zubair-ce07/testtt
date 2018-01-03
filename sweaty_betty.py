# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import datetime
import re


class SweatyBettySpider(CrawlSpider):
    name = 'sweaty_betty'
    allowed_domains = ['sweatybetty.com']
    start_urls = ['http://sweatybetty.com/']

    rules = (
        Rule(LinkExtractor(restrict_css=
                           '#header .megamenu > .megaitem .cats a:first-child'),
             follow=True),
        Rule(LinkExtractor(restrict_css=
                           '#listing-pagenation > .next'),
             follow=True),
        Rule(LinkExtractor(restrict_css=
                           '#productDataOnPage .productlistcell .prodlink.showonhover'),
             callback='parse_product', follow=True),
    )

    def parse_product(self, response):
        product_info = self.product_info(response)
        yield product_info

    def product_info(self, response):
        product = {
            'crawl_start_time': datetime.datetime.now(),
            'name': self.get_product_name(response),
            'price': self.get_product_price(response),
            'description': self.get_product_description(response),
            'lang': self.get_product_language(response),
            'url': self.get_product_link(response),
            'brand': self.get_product_brand(response),
            'retailer_sk': self.get_article_code(response),
            'image_urls': self.get_product_images(response),
            'care': self.get_product_care_info(response),
            'currency': self.get_product_currency(response),
            'gender': 'women',
            'skus': self.product_color_skus(response)
        }
        return product

    def get_product_currency(self, response):
        return response.css('meta[property="og:price:currency"]::attr(content)').get()

    def get_product_care_info(self, response):
        return response.css('.prod-left.mt0-important > div:last-child ::text').getall()

    def get_product_images(self, response):
        image_links = []
        links = re.findall(r'var colourArray_.+?= new Array\((.*?)\)', str(response.body))
        for link in links:
            image_links.append(link.split(","))
        return [link for sublist in image_links for link in sublist]

    def get_article_code(self, response):
        return response.css('.prod-right .block.valign-baseline.f-small.mt::text').get()

    def get_product_brand(self, response):
        return response.css('img[itemprop="logo"]::attr(title)').get()

    def get_product_link(self, response):
        return response.url

    def get_product_language(self, response):
        return response.css('html[lang]::attr(lang)').get()

    def get_product_description(self, response):
        return response.css('.prod-left div[itemprop="description"] ::text').getall()

    def get_product_price(self, response):
        return response.css('#priceCopy ::text').getall()
        # return response.css('#priceCopy > span[itemprop="price"]::text').getall() + \
        #        response.css('#priceCopy::text').getall()

    def get_product_name(self, response):
        return response.css('.prod-right h1[itemprop="name"]::text').get()

    def product_color_skus(self, response):
        product_color_info = {}
        product_currency_code = self.get_product_currency(response)
        skus_combinations = re.findall(r'new seldata\(new Array\((.*?)\),(.*?)\);', str(response.body))

        for skus_combination in skus_combinations:
            product_size_detail = skus_combination[0].split(",")
            product_color_detail = skus_combination[1].split(",")
            product_size_length = [item.replace("\\'", '') for item in product_size_detail]
            product_detail = [item.replace("\\'", '') for item in product_color_detail]

            if len(product_size_length) > 2 and \
                    "Select Your Size" not in product_size_length[1] and \
                    "select your length" not in product_size_length[2]:
                product_size = product_size_length[1]
                product_length, out_of_stock = self.get_size_and_length(product_size_length[2])
                product_id = product_detail[2]
                product_color = product_size_length[0]
                product_price = re.findall(r'>(.*?)</span', product_detail[0])

                color_info_key = '{}_{}'.format(product_id, product_size)
                product_color_info[color_info_key] = self.product_sku(product_color, product_currency_code,
                                                                      product_length, product_price, product_size,
                                                                      out_of_stock)
            elif len(product_size_length) > 1 and \
                    "Select Your Size" not in product_size_length[1]:
                product_size, out_of_stock = self.get_size_and_length(product_size_length[1])
                product_length = None
                product_id = product_detail[2]
                product_color = product_size_length[0]
                product_price = re.findall(r'>(.*?)</span', product_detail[0])

                color_info_key = '{}_{}'.format(product_id, product_size)
                product_color_info[color_info_key] = self.product_sku(product_color, product_currency_code,
                                                                      product_length, product_price, product_size,
                                                                      out_of_stock)
        return product_color_info

    def product_sku(self, product_color, product_currency_code, product_length, product_price, product_size,
                    out_of_stock=False):
        color_info = {
            'price': product_price,
            'length': product_length,
            'colour': product_color,
            'size': product_size,
            'currency': product_currency_code,
            'out_of_stock': out_of_stock
        }
        return color_info

    def get_size_and_length(self, product_size_length):
        size_availability = product_size_length.split("-")
        product_length = size_availability[0].strip()
        out_of_stock = size_availability[len(size_availability) - 1].strip() if len(
            size_availability) > 1 else False

        return (product_length, out_of_stock)
