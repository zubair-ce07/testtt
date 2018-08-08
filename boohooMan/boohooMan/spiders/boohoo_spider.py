import scrapy
import time
import re
import queue
from boohooMan.items import BoohoomanItem


class BoohooSpiders(scrapy.Spider):
    name = "boohoo"
    start_urls = [
        'https://www.boohooman.com/',
    ]

    def parse(self, response):
        for item in response.css('li.has-submenu'):

            for subitem in item.css('li a'):
                next_page = subitem.css('a::attr(href)').extract_first()
                if next_page is not None:
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse_url)

    def parse_url(self, response):
        for item in response.css('div.product-tile'):
            product_item = BoohoomanItem()
            product_item['sku'] = {}
            product_item['lang'] = response.css('html::attr(lang)').extract_first()
            product_item['name'] = item.css('div.product-name a::text').extract_first().strip("\n")
            product_item['date'] = time.time()
            item_url = response.urljoin(item.css(
                        'div.product-image a::attr(href)')
                        .extract_first())
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
        colors_items_list = response.css('div.product-variations ul.color \
                                         li.selectable:not(.selected) \
                                         span::attr(data-href) ').extract()
        color_queue = queue.Queue()
        index_colors_items_list = colors_items_list
        for item_url in colors_items_list:
            color_queue.put(scrapy.Request(item_url+"&format=ajax",
                                 callback=self.parse_item_size,
                                 meta={'item': product_item,
                                       'colors_items_list': index_colors_items_list
                                       }
                                 ))
        while not color_queue.empty():
            yield color_queue.get()

    def parse_item_size(self,response):
        product_item = response.meta['item']
        index_colors_items_list = response.meta['colors_items_list']
        size_items_list = response.css('div.product-variations ul.size \
                                        li.selectable:not(.selected) \
                                        span::attr(data-href) ').extract()
        size_queue = queue.Queue()
        for item_url in size_items_list:
            size_queue.put(scrapy.Request(item_url + "&format=ajax",
                                 callback = self.parse_item_info,
                                 meta = {'item': product_item,
                                         'colors_items_list': index_colors_items_list}
                                 ))
        while not size_queue.empty():
            yield size_queue.get()


    def parse_item_info(self, response):
        item_color = response.css('div.product-variations ul.color li.selected span::attr(title) ').extract_first()
        item_size = response.css('div.product-variations ul.size li.selected span::attr(title)').extract_first()
        item_sales_price = response.css('div.product-price span.price-sales::text ').extract_first()
        item_std_price = response.css('div.product-price span.price-standard::text ').extract_first()
        item_currency = response.css('div.product-price meta::attr(content) ').extract_first()
        item_color = re.sub('.*: ' , '' , item_color)
        item_size = re.sub('.*: ' , '' , item_size)
        product_item = response.meta['item']
        index_colors_items_list = response.meta['colors_items_list']
        item = {
             'colour': item_color,
             'item_size': item_size,
             'price': item_sales_price.strip("\u00a3"),
             'previous_prices': item_std_price.strip("\u00a3"),
             'currency': item_currency,
             }
        product_item['sku'].update({(item_color+"-"+item_size) :item})
        # product_item['item_detail']['skus'].update(item)
        if len(index_colors_items_list) > 0:
            index_colors_items_list.pop()
        else:
            yield {
              'item': product_item
            }
