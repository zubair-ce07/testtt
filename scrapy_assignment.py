# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import Rule
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor


class QuoteSpider(CrawlSpider):
    name = 'spiders2'
    start_urls = ['http://www.orsay.com/de-de/']
    rules = (
    Rule(LinkExtractor(allow_domains=('orsay.com'), restrict_css=('div.nav-container'))),
    Rule(LinkExtractor(allow_domains=('orsay.com'), restrict_css=('div.category-products')),
                  callback='parse_product_data'),)

    def parse_product_data(self, response):

        product_id, retailer_sku = self.product_id(response)
        brand = self.get_brand(response)
        care = self.get_care(response)
        image_urls = self.get_img_url(response)
        description = self.get_description(response)
        product_name = self.get_product_name(response)
        price = self.get_price(response)
        color = self.get_color(response)
        product_url = self.get_url(response)
        skus = self.get_skus(response, color, price, product_id)
        product = scrapy.Field(brand=brand, care=care,
                               description=description, gender='Women',
                               image_url=image_urls, name=product_name,
                               retailer_sku=retailer_sku, skus=skus,
                               url=product_url, origional_url=url)
        yield product

    def get_color(self, response):
        quotes = response.css('div.page')
        color = quotes.css('img.has-tip::attr(title)').extract()
        return color

    def get_url(self, response):
        quotes = response.css('div.page')
        product_url = quotes.css('li.store-hu_HU'
                         ' a::attr(href)').extract_first()
        product_url = (url.split('?'))[0]
        return product_url

    def get_brand(self, response):
        quotes = response.css('div.page')
        brand = quotes.css('a.logo img::attr(alt)').extract_first()
        brand = (brand.split(' '))[0]
        return brand

    def get_care(self, response):
        quotes = response.css('div.page')
        care = quotes.css('p.material::text, li > img::attr(src)').extract()
        return care

    def get_product_name(self, response):
        quotes = response.css('div.page')
        product_name = quotes.css('h1.product-name::text').extract()
        return product_name

    def get_description(self, response):
        quotes = response.css('div.page')
        description = quotes.css('div.short-description::text').extract()
        description = self.clean_spaces(description)
        return description

    def get_img_url(self, response):
        quotes = response.css('div.page')
        image_urls = quotes.css('a.MagicZoom::attr(href)').extract()
        return image_urls

    def get_price(self, response):
        quotes = response.css('div.page')
        price = quotes.css('span.price::text').extract_first()
        price = (price.strip())
        price = price.split(' ')
        return price

    def product_id(self, response):
        quotes = response.css('div.page')
        product_id = quotes.css('li.store-hu_HU a::attr(href)').extract()
        product_id = product_id[0].split('.html')
        product_id = product_id[0].split('-')
        product_id = product_id[len(product_id) - 1]
        retailer_sku = (product_id[:6])
        return (product_id, retailer_sku)

    def get_size_of_product(self, response):
        quotes = response.css('div.page')
        size_available = (quotes.css('li[class$="size-box '
                                     'ship-available"]::text').extract())
        size_unAvailable = (quotes.css('li.size-box.ship-available.'
                                       'size-unavailable::text').extract())
        size_available = map(str, size_available)
        size_unAvailable = map(str, size_unAvailable)
        size_available, size_unAvailable = self.clean_char(size_available,
                                                           size_unAvailable)
        return (size_available, size_unAvailable)

    def clean_char(self, size_avail, size_unavail):
        avaiable = []
        un_avaiable = []
        for i in range(len(size_unavail)):
            size = size_unavail[i].strip()
            if size is not '':
                un_avaiable.append(size)
        for i in range(len(size_avail)):
            size = size_avail[i].strip()
            if size is not '':
                avaiable.append(size)
        return (avaiable, un_avaiable)

    def clean_spaces(self, attribute):
        attr = []
        for space in range(len(attribute)):
            attr1 = attribute[space].strip()
            attr.append(attr1)
        return attr

    def get_skus(self, response, colors, prices, product_id):
        data = []
        size_available, sizeun_available = self.get_size_of_product(response)
        for i in range(len(size_available)):
            id_size = '{}_{}'.format(product_id, size_available[i])
            product_info_available = scrapy.Field(color=colors,
                                                  price=prices[0],
                                                  currency="EUR",
                                                  size=size_available[i])
            sku1 = (id_size, product_info_available)
            data.append(sku1)
        for i in range(len(sizeun_available)):
            id_size = '{}_{}'.format(product_id, sizeun_available[i])
            product_info_available = scrapy.Field(color=colors,
                                                  price=prices[0],
                                                  currency="EUR",
                                                  size=sizeun_available[i],
                                                  out_of_stock=True)
            sku2 = (id_size, product_info_available)
            data.append(sku2)
        skus = scrapy.Field(sku=data)
        return skus

