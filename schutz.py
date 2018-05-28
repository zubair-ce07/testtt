# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from utils import Utils
class SchutzSpider(CrawlSpider):
    name = 'SchutzSpider'
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
        requests = super(SchutzSpider, self).parse(response)
        for request in requests:
            request.meta['trail'] = ['https://schutz.com/br']
            request.meta['trail'].append(response.url)
            yield request

    def parse_product(self, response):
        price = Utils.get_price_info(response.css('span.sch-price ::text').extract())
       
        size_list = response.xpath('//div[@class="sch-sizes"]/ul/li/label/@class | //div[@class="sch-sizes"]/ul/li/label/text()').extract()
        if size_list:
            sku_info = Utils.get_sku_info(size_list, price,
                                            Utils.get_color_info(response.css('ul.sch-description-list > li')))
            out_of_stock = Utils.is_out_of_stock(size_list)
        else:
            size_list = response.css('div.sch-form-group-select > select > option::text').extract()
            sku_info = Utils.get_sku_info_from_drop_down(size_list, price,
                                                        Utils.get_color_info(response.css('ul.sch-description-list > li')))
            out_of_stock = True
        
        category_list = response.css('ul.clearfix > li > a::text').extract()
        category_list = category_list[1:len(category_list)-1]

        trail = response.meta['trail']
        trail.append(response.url)
        
        yield {
            'brand': 'Schutz',
            'care': Utils.get_care_info(response.css('ul.sch-description-list > li')),
            'category': category_list,
            'currency': 'BRL',
            'description': Utils.get_decription_info(
                                        response.css('div.sch-description-content > p::text').extract_first(),
                                        response.css('ul.sch-description-list > li')),
            'image_urls': response.css('div.is-slider-item > img::attr(src)').extract(),
            'name': response.css('h1.sch-sidebar-product-title::text').extract_first(),
            'price': price,
            'previous-prices': Utils.get_previous_prices(response.css('span.sch-price ::text').extract()),
            'retailer_sku': response.css('div.sch-pdp::attr(data-product-code)').extract(),
            'sku':sku_info,
            'trail':trail,
            'url':response.url,
            'out-of-stock':out_of_stock,
        }
