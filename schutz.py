# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
class schutzSpider(CrawlSpider):
    name = 'schutzSpider'
    allowed_domains = ['schutz.com.br']
    start_urls = ['https://schutz.com.br/store']

    # Follow any link scrapy finds (that is allowed and matches the patterns).
    rules = [Rule(LinkExtractor(
                restrict_xpaths=['//div[@class="sch-main-menu-sub-links-left"]', '//ul[@class="pagination"]/li[@class="next"]']
                ), callback='parse'),
                Rule(LinkExtractor(
                restrict_xpaths='//a[@class="sch-category-products-item-link"]'
                ), callback='parse_product', follow=True)]
     
    def parse (self, response):
        requests = super(schutzSpider, self).parse(response)
        for request in requests:
            request.meta['trail'] = ['https://schutz.com/br']
            request.meta['trail'].append(response.url)
            yield request
        
    def parse_product(self, response):
        #Currency
        currency = 'BRL'
        
        #Extracting Price
        price = 0
        price_list = response.css('span.sch-price ::text').extract()
        price_list = price_list[0:int(len(price_list)/2)]
        cleaned_price_list = []
        if int(len(price_list)) > 1:
            for prices in price_list:
                prices = prices.replace('\r\n\t', '').replace('\t', '').replace('R$', '')
                
                if prices.isdigit():
                    cleaned_price_list.append(int(prices) * 100)
            price = cleaned_price_list[len(cleaned_price_list)-1]
            cleaned_price_list = cleaned_price_list[0:len(cleaned_price_list)-1]
        else:
            price = int(price_list[0].replace('\t','').replace('\nR$','').replace('\r','')) * 100
        
        #Decription
        color = ''
        care = []
        description = [response.css('div.sch-description-content > p::text').extract_first()]
        for list_item in response.css('ul.sch-description-list > li'):
            span_text = list_item.css('span::text').extract_first()
            strong_text = list_item.css('strong::text').extract_first()
            if 'Material' not in span_text:
                description.append(f"{span_text}: {strong_text}")
            else:
                care.append(f"{span_text}: {strong_text}")
            if 'Cor' in span_text:
                color = strong_text

        #Category of product
        category_list = response.css('ul.clearfix > li > a::text').extract()
        category_list = category_list[1:len(category_list)-1]

        #sku info
        color_dictionary = {}
        item_out_of_stock = True
        size_list = response.xpath('//div[@class="sch-sizes"]/ul/li/label/@class | //div[@class="sch-sizes"]/ul/li/label/text()').extract()
        if size_list:
            dictionary = {size_list[i+1]: size_list[i] for i in range(0, len(size_list), 2)}

            for key,value in dictionary.items():
                dictionary = {'color':color, 'currencey':currency, 'price':price, 'size':key}
                if 'sch-avaiable' in value:
                    item_out_of_stock = False
                else:
                    dictionary['out-of-stock'] = True
                color_dictionary[f"{color}{key}"] = dictionary
        else:
            size_list = response.css('div.sch-form-group-select > select > option::text').extract()
            color_dictionary = {}
            for value in size_list:
                dictionary = {'color':'color', 'currencey':currency, 'price':price, 'size':value, 'out-of-stock':True}
                color_dictionary[f"{color}{value}"] = dictionary
        
        #Trail
        trail = response.meta['trail']
        trail.append(response.url)
        
        yield {
            'brand': 'Schutz',
            'care': care,
            'category': category_list,
            'currency': 'BRL',
            'description': description,
            'image_urls': response.css('div.is-slider-item > img::attr(src)').extract(),
            'name': response.css('h1.sch-sidebar-product-title::text').extract_first(),
            'price': price,
            'previous-prices': cleaned_price_list,
            'retailer_sku': response.css('div.sch-pdp::attr(data-product-code)').extract(),
            'sku':color_dictionary,
            'trail':response.meta['trail'],
            'url':response.url,
            'out-of-stock':item_out_of_stock,
        }