import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class AsicsItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()
    requests = scrapy.Field()


def clean(raw_data):
    if isinstance(raw_data, list):
        return [re.sub('\s+', ' ', data).strip() for data in raw_data
                if re.sub('\s+', ' ', data).strip()]
    elif isinstance(raw_data, str):
        return re.sub('\s+', ' ', raw_data).strip()


class AsicsSpider(scrapy.Spider):
    name = 'asics'
    allowed_domains = ['asics.com']
    start_urls = [
        # 'https://www.asics.com/us/en-us/',
        'https://www.asics.com/us/en-us/court-ff-novak/p/0020013180.100'

    ]


    def aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaparse(self, response):
        listing_urls = response.css('.childlink-wrapper ::attr(href)').getall()
        yield from [response.follow(url=url, callback=self.parse_category)
                    for url in listing_urls]

    def parse_category(self, response):
        product_urls = response.css('.prod-wrap ::attr(href)').getall()
        yield from [response.follow(url=url, callback=self.parse_item)
                    for url in product_urls]

        next_page_url = response.css('rightArrow ::attr(href)').get()
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse_category)

    def parse(self, response):
        item = AsicsItem()
        item['retailer_sku'] = self.product_id(response)
        item['name'] = self.product_name(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['url'] = self.product_url(response)
        item['description'] = self.product_description(response)
        item['image_urls'] = self.image_urls(response)
        item['care'] = []
        item['brand'] = self.product_brand(response)
        item['skus'] = {}
        item['requests'] = self.product_colors(response)

        yield from self.next_request_or_item(item)


    def product_id(self, response):
        return response.css('[itemprop="productID"] ::attr(content)').get()

    def product_name(self, response):
        return response.css('.single-prod-title ::text').get()

    def product_gender(self, response):
        return response.css('script[type="text/javascript"]').re('\"gender\":\"(.+?)\"')[0]

    def product_category(self, response):
        return response.css('.breadcrumb ::text').getall()[1]

    def product_url(self, response):
        return response.url

    def product_description(self, response):
        raw_descriptions = response.css('.tabInfoChildContent ::text').getall()
        return clean(raw_descriptions)[1:]

    def image_urls(self, response):
        return response.css('.owl-carousel ::attr(data-big)').getall()

    def product_brand(self, response):
        return response.css('html ::attr(data-brand)').get()

    def product_colors(self,response):
        color_urls = response.css('.colorVariant ::attr(href)').getall()
        return [response.follow(color_url, callback=self.product_skus)
                for color_url in color_urls]

    def product_skus(self, response):
        print('\n\n\n\n\n\nAAAAAAAAAAAAAAAAAAAAAA')

        item = response.meta['item']
        prev_price = response.css('.pull-right del ::text').getall()
        color = response.css('[itemprop="color"] ::text').get()
        raw_skus = item['skus']
        print('\n\n\n\n\n\n\n\n Color: ', color)
        for sku_sel in response.css('#sizes-options .SizeOption.inStock :first-of-type'):
            print('\n\n\n\n\n',sku_sel.css('::attr(data-value)').get())
            print(sku_sel.css('[itemprop="priceCurrency"]::attr(content)').get())
            print(sku_sel.css('[itemprop="price"]::attr(content)').get())
            print('Size:',clean(sku_sel.css('a.SizeOption ::text').get()))


            # print('\n\n\n\n\n\n\n\n SIZE: ', clean(sku_sel.css('.SizeOption ::text').get()))
            # single_sku = {
            #     sku_sel.css('::attr(data-value)').get():
            #         {
            #
            #             'color': color,
            #             'currency': sku_sel.css('[itemprop="priceCurrency"]::attr(content)').get(),
            #             'price': sku_sel.css('[itemprop="price"]::attr(content)').get(),
            #             'size': clean(sku_sel.css('.SizeOption ::text').get()),
            #             'previous_price': prev_price
            #         }
            # }
            # raw_skus.update(single_sku)

        item['skus'] = raw_skus
        yield from self.next_request_or_item(item)

    def next_request_or_item(self, item):

        print('\n\n\n\n\n',item['requests'])

        if item['requests']:
            request = item['requests'].pop()
            request.meta.update({'item': item})
            print('QQQQQQQQQQQQQQQQQQQQ',request.callback)
            yield request
            return

        item.pop('requests', None)
        # yield item
#ARSH
