from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from snkrs.items import SnkrsItem, SnkrsSkuItem


class SnkrsSpider(CrawlSpider):
    name = 'snkrsspider'
    start_urls = ['https://www.snkrs.com/en/']
    css_rules = [
        '.sf-menu',
        '#pagination_next_bottom',
    ]

    rules = (
        Rule(link_extractor=LinkExtractor(restrict_css='div.row #center_column #product_list'),
             callback='parse_product'),
        Rule(link_extractor=LinkExtractor(restrict_css=css_rules))
    )

    def parse_product(self, response):
        print(f'<><><><><><><><><><><>{response.url}<><><><><><><><><><><><><>')
        snkrs_item = SnkrsItem()
        snkrs_item['name'] = response.css('.pb-center-column h1::text').extract_first()
        snkrs_item['retailer_sku'] = response.css('#product_reference span::text').extract_first()
        snkrs_item['lang'] = response.css('html::attr(lang)').extract_first()
        #TODO Item trail, gender
        snkrs_item['category'] = response.css('.breadcrumb li a::text').extract()[1:-1]
        snkrs_item['brand'] = response.css('#product_marques img::attr(alt)').extract_first()
        snkrs_item['url'] = response.url
        snkrs_item['url_original'] = response.css('#center_column meta::attr(content)').extract_first()
        snkrs_item['description'] = response.css('#short_description_content p::text').extract()
        snkrs_item['image_urls'] = response.css('.pb-left-column img#bigpic::attr(src)').extract()
        snkrs_item['image_urls'].extend(response.css('#views_block #carrousel_frame li a::attr(href)').extract())
        snkrs_item['price'] = response.css('#our_price_display::attr(content)').extract_first()
        snkrs_item['currency'] = response.css('p.our_price_display meta::attr(content)').extract_first()
        snkrs_item['skus'] = []
        yield snkrs_item
