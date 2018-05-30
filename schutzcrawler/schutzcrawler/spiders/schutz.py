import re
import copy

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from schutzcrawler.items import ProductItem
from schutzcrawler.PriceExtractor import PriceExtractor


class SchutzSpider(CrawlSpider):
    name = 'schutzspider'
    allowed_domains = ['schutz.com.br']
    start_urls = ['https://schutz.com.br/store/']
    default_xpaths = ['//div[@class="sch-main-menu-sub-links-left"]', 
                      '//ul[@class="pagination"]/li[@class="next"]']
    product_xpath = '//a[@class="sch-category-products-item-link"]'

    # Follow any link scrapy finds (that is allowed and matches the patterns).
    rules = [Rule(LinkExtractor(restrict_xpaths=default_xpaths), callback='parse'),
             Rule(LinkExtractor(restrict_xpaths=product_xpath
             ), callback='parse_product', follow=True)]
 
    def parse(self, response):
        requests = super(SchutzSpider, self).parse(response)
        trail = copy.deepcopy(response.meta.get('trail', []))
        trail.append(response.url)
        for request in requests:
            request.meta['trail'] = trail
            yield request

    def parse_product(self, response):
        price = PriceExtractor.prices(response)
        description = self.description(response)
        skus = self.sku(response)

        product = ProductItem()
        product['brand'] = 'Schutz'
        product['care'] = self.care(response)
        product['category'] = self.category(response)
        product['description'] = description
        product['name'] = self.product_name(response)
        product['retailer_sku'] = self.retailer_sku(response)
        product['sku'] = skus
        product['trail'] = response.meta.get('trail', [])
        product['url'] = response.url
        product['out_of_stock'] = self.is_out_of_stock(skus)

        yield product

    def raw_description(self, response):
        description_text = '.sch-description-content p::text'
        description_list = '.sch-description-list li'

        description = [response.css(description_text).extract_first()]
        for list_item in response.css(description_list):
            span_text = list_item.css('span::text').extract_first()
            strong_text = list_item.css('strong::text').extract_first()
            description.append(f"{span_text}: {strong_text}")  
        return description

    def description(self, response):
        raw_description = self.raw_description(response)
        description = [raw_description[0]]
        [description.append(item) for item in raw_description if 'Material' not in item]
        return description

    def color(self, response):
        raw_description = self.raw_description(response)
        color = [item.split(':')[1] for item in raw_description if 'Cor' in item]
        return color[0]

    def care(self, response):
        raw_description = self.raw_description(response)
        care = [item for item in raw_description if 'Material' in item]
        return care

    def category(self, response):
        category_list = response.css('.clearfix a::text').extract()
        return category_list[1:-1]

    def sku(self, response):
        color_dictionary = {}
        prices = PriceExtractor.prices(response)
        previous_prices = prices[1:]
        price = prices[0]
        color = self.color(response)
        drop_down_sel = '.sch-notify-form .sch-form-group-select select option'
        list_sel = '.sch-sizes label'
        sizes = response.css(list_sel) or response.css(drop_down_sel)
        for size in sizes:
            dictionary = {'color': color, 'currency': 'BRL', 'price': price}
            size_value = size.css(' ::text').extract_first() or size.css(' ::text').extract_first()
            dictionary['size'] = size_value
            if size.xpath('self::*[not(contains(@class, "sch-avaiable"))]').extract():
                dictionary['out_of_stock'] = True
            if previous_prices:
                dictionary['previous_prices'] = previous_prices

            color_dictionary[f"{color}{size_value}"] = dictionary
        return color_dictionary

    def is_out_of_stock(self, sku):
        return not any(v.get('out_of_stock', False) is False for v in sku.values())

    def retailer_sku(self, response):
        retailer_sku_sel = '.sch-pdp::attr(data-product-code)'
        return response.css(retailer_sku_sel).extract_first()

    def product_name(self, response):
        name_sel = '.sch-sidebar-product-title::text'
        return response.css(name_sel).extract_first()
