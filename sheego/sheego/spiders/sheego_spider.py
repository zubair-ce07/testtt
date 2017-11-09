import re

from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from ..items import SheegoItem


class MotelRocksSpider(CrawlSpider):
    name = 'sheego-de'
    start_urls = ['https://www.sheego.de/damenmode/']
    allowed_domains = ['sheego.de', ]
    visited_items = set()
    currency = 'EU'
    color_url_t = 'https://www.sheego.de/index.php?anid=126791&cl=oxwarticledetails&varselid%5B0%5D={c_code}'
    products_css = '.js-product-box .product__top'
    pagination_css = '.paging__btn .paging__btn'

    rules = [
        Rule(LinkExtractor(restrict_css=products_css, deny='.php?'), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=pagination_css)),
    ]

    def parse_item(self, response):
        retailer_sku = self.item_retailer_sku(response)
        if self.is_visited(retailer_sku):
            return
        item = SheegoItem()
        item['brand'] = self.item_brand(response)
        item['care'] = self.item_care(response)
        item['category'] = self.item_category(response)
        item['description'] = self.item_description(response)
        item['name'] = self.item_product_name(response)
        item['gender'] = 'women'
        item['retailer_sku'] = retailer_sku
        item['url'] = response.url
        item['skus'] = self.item_skus(response)
        item['image_urls'] = self.item_image_urls(response)

        item['request_queue'] = self.item_color_request(response)
        yield self.next_request_or_item(item)

    def parse_item_skus(self, response):
        item = response.meta['item']
        item_skus = item.get('skus', {})
        item_skus.update(self.item_skus(response))
        item['skus'] = item_skus
        item['image_urls'] += self.item_image_urls(response)
        yield self.next_request_or_item(item)

    def next_request_or_item(self, item):
        request_queue = item.get('request_queue')
        if request_queue:
            request = request_queue.pop()
            request.meta['item'] = item
            return request
        else:
            del item['request_queue']
            return item

    def item_color_request(self, response):
        color_request = []
        colour_codes = response.css('.colorspots__item:not(.cj-active) ::attr(data-varselid)').extract()
        for code in colour_codes:
            color_request.append(Request(self.color_url_t.format(c_code=code), callback=self.parse_item_skus))
        return color_request

    def is_visited(self, retailer_sku):
        if retailer_sku in self.visited_items:
            return True
        self.visited_items.add(retailer_sku)
        return False

    def item_image_urls(self, response):
        urls = response.css('a#magic ::attr(href)').extract()
        return ['http:' + url for url in urls]

    def item_care(self, response):
        return " ".join(self.clean(response.css('.f-xs-12:not(.l-hidden) .p-details__material td ::text').extract()))

    def item_brand(self, response):
        return "".join(self.clean(response.css('.at-brand ::text').extract()))

    def clean(self, data_list_or_str):
        if isinstance(data_list_or_str, str):
            return data_list_or_str.strip()
        return [d.strip() for d in data_list_or_str if d.strip()]

    def item_retailer_sku(self, response):
        return self.clean(response.css('.l-mb-20 .js-artNr ::text').extract_first())

    def item_product_name(self, response):
        return self.clean(response.css('.at-name ::text').extract_first())

    def item_category(self, response):
        return response.css('.at-breadcrumb-item ::text').extract()[:-1]

    def item_description(self, response):
        return " ".join(self.clean(response.css('.at-dv-article-details ::text').extract()))

    def integer_price(self, price):
        price = ''.join(re.findall('\d+', price))
        if price:
            return int(price)

    def item_price(self, response):
        return self.integer_price(response.css('.flex-container .js-lastprice::attr(value)').extract_first())

    def active_color(self, response):
        return response.css('.colorspots__wrapper .cj-active ::attr(title)').extract_first()

    def item_skus(self, response):
        skus = {}
        common = {}
        common['colour'] = self.active_color(response)
        common['currency'] = self.currency
        common['price'] = self.item_price(response)
        for s_selector in response.css('.sizespots__item'):
            sku = common.copy()
            sku['size'] = self.clean(s_selector.css('::text').extract_first())
            if s_selector.css('.sizespots__item--disabled'):
                sku['out_of_stock'] = True
            skus["{}_{}".format(common['colour'], sku['size'])] = sku
        return skus
