# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from ..items import WoolworthCoItem


class WoolsWorthSpider(CrawlSpider):
    name = 'woolsworth'
    allowed_domains = ['www.woolworths.co.za']
    start_urls = ['http://www.woolworths.co.za/store/cat']

    rules = (
        Rule(LinkExtractor(restrict_css='a.pagination__nav')),
        Rule(LinkExtractor(deny='/Food/', restrict_css="a.product-card__details"), callback="parse_product"),)

    price_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/price.jsp?' \
                'productItemId={0}&colourSKUId={1}&sizeSKUId={2}'
    item_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/product-item.jsp' \
               '?productItemId={0}&colourSKUId={1}'

    def parse_product(self, response):
        item = WoolworthCoItem()
        item['name'] = self.get_name(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['brand'] = self.get_brand(response)
        item['categories'] = self.get_categories(response)
        item['details'] = self.get_details(response)
        item['image_urls'] = self.get_image_urls(response)

        colour_list = self.get_colour_list(response)
        colour_ids = self.extract_colour_ids(colour_list)
        item['skus'] = {}
        request_list = []

        for colour_id in colour_ids:
            request_list.append(scrapy.Request(
                url=self.item_url.format(item['retailer_sku'], colour_id),
                callback=self.parse_colours,
                meta={'item': item,
                      'colour_id': colour_id,
                      'request_list': request_list}))
        yield request_list.pop(0)

    def parse_colours(self, response):
        item = response.meta['item']
        request_list = response.meta['request_list']
        colour_id = response.meta['colour_id']
        colour = self.get_colour(colour_id, response)
        size_list = self.get_size_list(response)
        size_ids = self.extract_size_ids(size_list)
        for size_id in size_ids:
            meta_data = {
                'size_id': size_id,
                'colour': colour,
                'item': item,
                'request_list': request_list
            }
            request_list.append(
                scrapy.Request(url=self.price_url.format(item['retailer_sku'], colour_id, size_id),
                               callback=self.parse_size, meta=meta_data))
        yield request_list.pop(0)

    def parse_size(self, response):
        price = self.get_price(response)
        item = response.meta['item']
        colour = response.meta['colour']
        size_id = response.meta['size_id']
        sku_key = colour + '_' + size_id
        sku_data = {
            'size_id': size_id,
            'colour': colour,
            'price': price
        }
        current_sku = {
            sku_key: sku_data
        }
        item['skus'].update(current_sku)
        request_list = response.meta['request_list']
        if request_list:
            yield request_list.pop(0)
        else:
            yield item

    def get_name(self, response):
        return response.css('input#gtmProductDisplayName::attr(value)').extract_first()

    def get_price(self, response):
        return response.css('span.price[itemprop="price"]::attr(content)').extract_first()

    def get_size_list(self, response):
        return response.css('a.product-size::attr(onclick)').extract()

    def get_colour_list(self, response):
        return response.css('img.colour::attr(onclick)').extract()

    def get_image_urls(self, response):
        image_urls = response.css('div.pdp__image img::attr(src)').extract()
        image_urls.append(response.css('div[data-js="pdp-carousel"] ::attr(src)').extract())
        return image_urls

    def get_details(self, response):
        return response.css('meta[itemprop="description"]::attr(content)').extract_first()

    def get_categories(self, response):
        return response.css('ol.breadcrumb a::text').extract()

    def get_brand(self, response):
        return response.css('meta[itemprop="brand"]::attr(content)').extract_first()

    def get_colour(self, colour_id, response):
        return response.css('input#colour_' + colour_id + '::attr(value)').extract_first()

    def get_retailer_sku(self, response):
        return response.css('input#gtmProductId::attr(value)').extract_first()

    def extract_id_string(self, st):
        return st[st.find("(") + 1:st.rfind(")")]

    def extract_colour_ids(self, selector_list):
        selector_list = [self.extract_id_string(x) for x in selector_list]
        ids_list = [x.split(',')[0] for x in selector_list]
        return ids_list

    def extract_size_ids(self, selector_list):
        selector_list = [self.extract_id_string(x) for x in selector_list]
        ids_list = [x.split(',')[1] for x in selector_list]
        return ids_list
