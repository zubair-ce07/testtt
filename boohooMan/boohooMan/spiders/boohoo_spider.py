import scrapy
import time
import re
from boohooMan.items import BoohoomanItem

class BoohooSpiders(scrapy.Spider):
    name = "boohoo"
    start_urls = [
        'https://www.boohooman.com/',
    ]

    def parse(self, response):
        for item in response.css('li.has-submenu'):
            for subitem in item.css('li a'):
                # print(subitem.css('a::attr(href)').extract_first())
                # print(subitem.css('a::text').extract_first())
                next_page = subitem.css('a::attr(href)').extract_first()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse_url)

    def parse_url(self, response):
        for item in response.css('div.product-tile'):
            product_item = BoohoomanItem()
            product_item['name'] = item.css('div.product-name a::text').extract_first()
            product_item['date'] = time.time()
            item_url = response.urljoin(item.css(
                        'div.product-image a::attr(href)')
                        .extract_first())
            product_item['standard_price'] = item.css(
                         'div.product-pricing \
                          span.product-standard-price::text').extract_first()
            product_item['sales_price'] = item.css(
                          'div.product-pricing \
                           span.product-sales-price::text').extract_first()
            product_item['colors'] = item.css(
                      'div.product-swatches \
                       li.product-swatch-item  a::attr(title)').extract(),
            product_item['url'] = response.urljoin(item.css(
                        'div.product-image a::attr(href)').extract_first())
            yield scrapy.Request(item_url, callback=self.parse_item_color,meta={'item': product_item})

        next_page = response.css('li.pagination-item a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    def parse_item_color(self,response):
        product_item = response.meta['item']
        product_item['retailer_sku'] = response.css('div.product-number span::text').extract_first()
        product_item['retailer'] = 'boohooman-us'
        colors_items_list = response.css('div.product-variations ul.color li.selectable:not(.selected) span::attr(data-href) ').extract()
        for item_url in colors_items_list:
            yield scrapy.Request(item_url+"&format=ajax", callback=self.parse_item_size,meta={'item': product_item })

    def parse_item_size(self,response):
        product_item = response.meta['item']
        size_items_list = response.css('div.product-variations ul.size li.selectable:not(.selected) span::attr(data-href) ').extract()
        for item_url in size_items_list:
            yield scrapy.Request(item_url+"&format=ajax", callback=self.parse_item_info,meta={'item': product_item })

    def parse_item_info(self,response):
        item_color = response.css('div.product-variations ul.color li.selected span::attr(title) ').extract()
        item_size = response.css('div.product-variations ul.size li.selected span::attr(data-variation-values) ').extract()
        item_color = re.sub('.*: ' , '' , item_color[0] )
        print("gggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
        print(item_size[0])
        # item_size =  dict(item_size)

        yield{
             # 'item_color': item_color,
             'item_size': item_size
        }

#
#
# def parse_item_color(self,response):
#     product_item = response.meta['item']
#     product_item['retailer_sku'] = response.css('div.product-number span::text').extract_first()
#     product_item['retailer'] = 'boohooman-us'
#     colors_items_list = response.css('div.product-variations ul.color li.selectable:not(.selected) span::attr(data-href) ').extract()
#     yield{
#          'item' : product_item
#     }
#         # yield scrapy.Request(item_url+"&format=ajax", callback=self.parse_item_size,meta={'item': product_item })
#
# def parse_item_color(self,response):
#     pass
