import re

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class SchutzSpider(CrawlSpider):
    name = 'schutzspider'
    allowed_domains = ['schutz.com.br']
    start_urls = ['https://schutz.com.br/store/']
    xpaths = ['//div[@class="sch-main-menu-sub-links-left"]',
                 '//ul[@class="pagination"]/li[@class="next"]']

    # Follow any link scrapy finds (that is allowed and matches the patterns).
    rules = [Rule(LinkExtractor(
                restrict_xpaths=xpaths
                ), callback='parse'),
                Rule(LinkExtractor(
                restrict_xpaths='//a[@class="sch-category-products-item-link"]'
                ), callback='parse_product', follow=True)]
 
    def parse(self, response):
        requests = super(SchutzSpider, self).parse(response)
        for request in requests:
            request.meta['trail'] = ['https://schutz.com/br']
            request.meta['trail'].append(response.url)
            yield request

    def clean_price_list(self, price_list):
        cleaned_price_list = []
        for prices in price_list:
            prices = re.findall('\d+', prices)
            if prices:
                cleaned_price_list.append(int(prices[0]) * 100)
        return cleaned_price_list

    def description(self, response):
        description_text = '.sch-description-content p::text'
        description_list = '.sch-description-list li'

        description = [response.css(description_text).extract_first()]
        for list_item in response.css(description_list):
            span_text = list_item.css('span::text').extract_first()
            strong_text = list_item.css('strong::text').extract_first()
            description.append(f"{span_text}: {strong_text}")  
        return description

    def color(self, description):
        for list_item in description[1:]:
            if 'Cor' in list_item:
                return list_item.split(':')[1]
        return None

    def care(self, description):
        care = []
        for list_item in description[1:]:
            if 'Material' in list_item:
                care.append(list_item)
        return care

    def prices(self, response):
        price_list = response.css('.sch-price ::text').extract()
        price_list = set(self.clean_price_list(price_list))
        return sorted(price_list)

    def category(self, response):
        category_list = response.css('.clearfix a::text').extract()
        return category_list[1:-1]

    def sku(self, response):
        color_dictionary = {}
        price = self.prices(response)[0]
        color = self.color(self.description(response))
        drop_down_sel = '.sch-notify-form .sch-form-group-select select option'
        list_sel = '.sch-sizes label'
        sizes = response.css(list_sel) or response.css(drop_down_sel)
        for size in sizes:
            dictionary = {'color': color, 'currencey': 'BRL', 'price': price}
            size_value = size.css(' ::text').extract_first()
            dictionary['size'] = size_value
            if 'sch-avaiable' not in size.xpath("@class").extract_first():
                dictionary['out_of_stock'] = True
            color_dictionary[f"{color}{size_value}"] = dictionary
        return color_dictionary

    def is_out_of_stock(self, sku):
        for key, value in sku.items():
            if not value.get('out_of_stock', ''):
                return False
        return True

    def retailer_sku(self, response):
        retailer_sku_sel = '.sch-pdp::attr(data-product-code)'
        return response.css(retailer_sku_sel).extract_first()

    def product_name(self, response):
        name_sel = '.sch-sidebar-product-title::text'
        return response.css(name_sel).extract_first()

    def parse_product(self, response):
        price = self.prices(response)
        description = self.description(response)
        sku = self.sku(response)

        yield {
            'brand': 'Schutz',
            'care': self.care(description),
            'category': self.category(response),
            'description': description,
            'name': self.product_name(response),
            'retailer_sku': self.retailer_sku(response),
            'sku': sku,
            'trail': response.meta['trail'],
            'url': response.url,
            'out-of-stock': self.is_out_of_stock(sku),
        }
