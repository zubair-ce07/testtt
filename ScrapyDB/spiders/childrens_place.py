# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
import json

from ScrapyDB.items import StackItem, VariationItem, SizeItem

class ChildrensPlaceSpider(scrapy.Spider):
    name = 'ScrapyDB'
    allowed_domains = ['childrensplace.com']
    start_urls = ["https://www.childrensplace.com/shop/us/home"]

    def parse(self, response):
        categories = response.css('li.navigation-level-one')
        for category in categories:
            category_url =urlparse.urljoin(response.url,
                                           category.css('a::attr(href)').extract_first())
            yield scrapy.Request(url=category_url, callback=self.parse_cats)

    def parse_cats(self, response):
        sub_categories = response.css('li.leftNavLevel0')
        for sub_category in sub_categories:
            sub_cats_url = sub_category.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=sub_cats_url, callback=self.parse_sub_cats)

    def parse_sub_cats(self, response):
        for product in response.css('div[class="productRow name"]'):
            item = StackItem()
            title = product.css('span[itemprop="name"]::text').extract_first()
            title = title.encode('utf-8')
            item['title'] = title
            product_url = product.css('a::attr(href)').extract_first()
            product_url = product_url.encode('utf-8')
            item['product_url'] = product_url
            item['brand'] = product_url
            yield scrapy.Request(url=item['product_url'],
                                 callback=self.parse_product, meta={'item': item})

    def parse_product(self, response):
        item = response.meta['item']
        product_detail = response.css('div.product-details')
        for product in product_detail:
            id = product.css('div[class="item-number lighter-grey"] span::text').extract_first()
            id = id.encode('utf-8')
            id = id.strip('Item #:  ')
            item['store_keeping_unit'] = id
            item['description'] = []
            descriptions = product.css('div[class="product-description section-block"] ul li')
            for description in descriptions:
                description = description.css('li::text').extract_first()
                description = description.encode('utf-8')
                item['description'].append(description)
            locale = response.css('ul[id="BVSEO_meta"] li[data-bvseo="cf"]::text').extract_first()
            if type(locale) is unicode:
                locale = locale.encode('utf-8')
            else:
                locale = str(locale)
            locale = locale.split(',')
            item['locale'] = locale[0].strip('loc_')
            variation_item = VariationItem()
            color_name = response.css('span[id="colorName"]::text').extract_first()
            color_name = color_name.encode('utf-8')
            variation_item['display_color_name'] = color_name
            variation_item['image_urls'] = []
            img_urls = response.css('div.product-thumbnails')
            for img_url in img_urls.css('img::attr(src)').extract():
                img_url = img_url.encode('utf-8')
                variation_item['image_urls'].append(urlparse.urljoin(response.url, img_url))
            variation_item['sizes'] = []
            regular_price = response.css('span.regular-price::text').extract_first()
            regular_price = unicode.strip(regular_price)
            regular_price = regular_price.encode('utf-8')
            regular_price = regular_price.strip("Was:\xc2\xa0")
            sale_price = unicode.strip(response.css('span.sale-price::text').extract_first())
            sale_price = sale_price.encode('utf-8')
            price_currency = response.css('span[itemprop="priceCurrency"]::text').extract_first()
            price_currency = price_currency.encode('utf-8')
            item['currency'] = price_currency
            sizes_detail = response.xpath('normalize-space(//div[@class="product"]/script)').extract_first()
            sizes_detail = sizes_detail.split(']')
            size_detail = re.sub(r'^var entitledItem_[0-9]* = ', '', sizes_detail[0])
            size_detail = size_detail.strip('[ * ')
            size_detail = size_detail.replace('},', '}},')
            size_detail = size_detail.split('},')
            for size in size_detail:
                size_item = SizeItem()
                size_dict = json.loads(size.encode('utf-8'))
                quantity = size_dict['qty']
                if quantity is '0':
                    size_item['is_available'] = False
                else:
                    size_item['is_available'] = True
                size_name = re.sub(r'^({\"Size_)','',json.dumps(size_dict['Attributes']))
                size_name = size_name.replace('\": \"1\"}', '')
                size_item['size_name'] = size_name
                if(regular_price == sale_price):
                    size_item['is_discounted'] = False
                else:
                    size_item['is_discounted'] = True
                size_item['price'] = regular_price
                size_item['discounted_price'] = sale_price
                variation_item['sizes'].append(size_item)
            item['variations'] = variation_item
            yield item