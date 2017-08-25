# -*- coding: utf-8 -*-
import re
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from ScrapyDB.items import StackItem, VariationItem, SizeItem

class ChildrensPlaceSpider(CrawlSpider):
    name = 'ScrapyDB'
    allowed_domains = ['childrensplace.com']
    start_urls = ['http://www.childrensplace.com/shop/us/home']
    rules = (
        Rule(LinkExtractor(allow=('childrensplace.com'), restrict_css=('div.navigation-container'))),
        Rule(LinkExtractor(allow=('childrensplace.com'), restrict_css=('div.categoryContent')), callback="parse_item", follow=True)
    )

    def parse_item(self, response):
        item = StackItem()
        id = response.css('span[id="partNumber"]::text').extract_first()
        item['store_keeping_unit'] = id.strip('Item #:  ')
        item['title'] = response.css('h1.dark-grey::text').extract_first()
        item['product_url'] = response.url
        item['brand'] = response.url
        item['description'] = response.css('div[class="product-description section-block"] li::text').extract()
        locale = response.css('ul[id="BVSEO_meta"] li[data-bvseo="cf"]::text').extract_first()
        locale = locale.split(',')
        item['locale'] = locale[0].strip('loc_')
        item['currency'] = response.css('span[itemprop="priceCurrency"]::text').extract_first()
        variation_item = VariationItem()
        variation_item['display_color_name'] = response.css('span[id="colorName"]::text').extract_first()
        variation_item['image_urls'] = []
        img_urls = response.css('div.product-thumbnails img::attr(src)').extract()
        for img_url in img_urls:
            variation_item['image_urls'].append(response.urljoin(img_url))
        variation_item['sizes'] = []
        sizes_detail = response.xpath('normalize-space(//div[@class="product"]/script)').extract_first()
        sizes_detail = sizes_detail.split(']')
        size_detail = re.sub(r'^var entitledItem_[0-9]* = ', '', sizes_detail[0])
        size_detail = size_detail.strip('[ * ')
        size_detail = size_detail.replace('},', '}},')
        size_detail = size_detail.split('},')
        regular_price = response.css('span.regular-price::text').extract_first()
        regular_price = regular_price.encode('utf-8')
        regular_price = regular_price.strip("Was:\xc2\xa0")
        sale_price = unicode.strip(response.css('span.sale-price::text').extract_first())
        sale_price = sale_price.encode('utf-8')
        for size in size_detail:
            size_item = SizeItem()
            size_dict = json.loads(size.encode('utf-8'))
            size_name = re.sub(r'^({\"Size_)','',json.dumps(size_dict['Attributes']))
            size_name = size_name.replace('\": \"1\"}', '')
            size_item['size_name'] = size_name
            quantity = size_dict['qty']
            if quantity == '0':
                size_item['is_available'] = False
            else:
                size_item['is_available'] = True
            size_item['price'] = regular_price
            if(regular_price == sale_price):
                size_item['is_discounted'] = False
            else:
                size_item['is_discounted'] = True
            size_item['discounted_price'] = sale_price
            variation_item['sizes'].append(size_item)
        item['variations'] = variation_item
        yield item