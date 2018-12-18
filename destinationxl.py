# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Selector
from destinationxl_spider.items import DestinationxlSpiderItem




class DestinationxlSpider(scrapy.Spider):
    name = 'destinationxl'
    allowed_domains = ['www.destinationxl.com']
    start_urls = ['http://www.destinationxl.com/mens-big-and-tall-store/']


    def parse(self, response):
        all_categories_url = response.xpath('//header/nav/ul//li//a/@href').extract()
        for category in all_categories_url:
            if 'mens-jeans' in category:
                yield response.follow(category, callback=self.parse_all_pages)


    def parse_all_pages(self, response):
        script = response.css('script#dxl-state').extract_first()
        get_script = script.split('<script id="dxl-state" type="application/json">')[1]
        clean_data = get_script.strip('</script>')
        category = clean_data.replace('&q;', '"')
        data = json.loads(category)
        try:
            data_keys = data['plpResponse']['contents'][0]['SecondaryContent'][1]['' \
                                'contents'][0]['navigation']
        except IndexError:
            data_keys = None

        if data_keys:
            for raw_keys in data_keys:
                if 'refinements' not in raw_keys.keys():
                    return
                for keys in raw_keys['refinements']:
                    url_n = keys['navigationState'].split('&')[0]
                    url = url_n.split('+')[0]
                    yield response.follow(url, callback=self.parse_products)

    def parse_products(self, response):
        base_url = 'http://www.destinationxl.com'
        product_urls = response.css('.switch-hover a::attr(href)').extract()

        for product_url in product_urls:
            url = '{}{}'.format(base_url, product_url)
            yield scrapy.Request(url, callback=self.parse_item)


        if self.parse_next_url(response) != 0:
            for no_of_products in range(30, (self.parse_next_url(response)-1) * 30, 30):
                if no_of_products == 90:
                    break
                if self.parse_next_url(response) != 0:
                    if '&' in response.url:
                        next_url = response.url.split('&')[0]
                        url = '{}&No={}'.format(next_url, no_of_products)
                        yield scrapy.Request(url, callback=self.parse_products)
                    else:
                        url = '{}&No={}'.format(response.url, no_of_products)
                        yield scrapy.Request(url, callback=self.parse_products)

    def parse_item(self, response):
        item = DestinationxlSpiderItem()
        page_url = response.url
        item['page_url'] = page_url
        item['category'] = self.get_item_categroy(response)
        item_url = 'https://www.destinationxl.com/public/v1/dxlproducts/{}/{}'

        url = item_url.format(response.url.split('/')[-2], response.url.split('/')[-1])

        yield scrapy.Request(url, meta={'item': item}, callback=self.parse_combinations)

    def parse_combinations(self, response):

        item = response.meta['item']
        size_and_color = json.loads(response.text)

        text = Selector(text=size_and_color['longDescription'])
        description = text.css('p::text').extract_first()

        price = size_and_color['price']
        original_price = price['originalPrice']
        if bool(price['onSale']):
            sale_price = price['salePrice']
            on_sale = price['saleMessage']
        else:
            sale_price = None
            on_sale = None

        item['original_price'] = original_price
        item['sale_price'] = sale_price
        item['on_sale'] = on_sale
        item['description'] = description
        item['image_url'] = self.get_image_url(response)

        c_url = '{}?&isSelection=True&attributes=color={}'
        for color_id in size_and_color['colorGroups'][0]['colors']:
            url = c_url.format(response.url, color_id['id'])
            yield scrapy.Request(url, callback=self.filter_selection, meta=response.meta)

    def filter_selection(self, response):

        base_url = 'http://www.destinationxl.com/mens-big-and-tall-store/{}/{}/{}/{}'
        url_cat = response.url.split('/')
        url = base_url.format(url_cat[-4], url_cat[-3], url_cat[-2], url_cat[-1])

        yield scrapy.Request(url, callback=self.parse_details, meta=response.meta)

    def parse_details(self, response):
        script = response.css('script#dxl-state').extract_first()
        get_script = script.split('<script id="dxl-state" type="application/json">')[1]
        clean_data = get_script.strip('</script>')
        category = clean_data.replace('&q;', '"')
        data = json.loads(category)

        try:
            product_attr = data['pDetails']['sizes'][0]['attribute']
        except IndexError:
            product_attr = None

        try:
            for length in data['pDetails']['sizes'][0]['values']:
                product_url = 'https://www.destinationxl.com/public/v1/dxlproducts/{}/{}@{}={}'
                url = product_url.format(response.url.split('/')[-2],
                                         response.url.split('/')[-1], product_attr, length['value'])
                yield scrapy.Request(url, callback=self.parse_size, meta=response.meta)
        except IndexError:
            data['pDetails']['sizes'][0]['values'] = None

    def parse_size(self, response):
        colors = []
        item = response.meta['item']
        item['info'] = []
        data = json.loads(response.text)
        for color in data['colorGroups'][0]['colors']:
            if bool(color['selected']) and bool(color['available']):
                colors.append(color['id'])

        for sizes in data['sizes']:
            for size in sizes['values']:
                if bool(size['available']) and bool(size['selected']):
                    size_name = {'name':data['sizes'][0]['displayName']}
                    size_value = {'selected_length': size['value']}
                    selected_size = {
                        'size_name':size_name,
                        'size_value':size_value
                    }
                    item['info'].append(selected_size)
        for sizes in data['sizes'][1]['values']:
            if bool(sizes['available']):
                size_name = {'name':data['sizes'][1]['displayName']}
                size_value = {'lenght':sizes['value']}

                size_details = {
                    'size_name':size_name,
                    'size_value': size_value
                }
                item['info'].append(size_details)


        item['selected_color'] = colors
        yield item

    def parse_next_url(self, response):
        no_of_pages = response.xpath('//*[contains(@class,"page-nos")]/span[last()-1]//text()')\
                                        .extract_first()
        if no_of_pages and no_of_pages != '' and no_of_pages != '...':
            return int(no_of_pages)
        else:
            return 0

    def get_image_url(self, response):
        size_and_color = json.loads(response.text)
        image_url = size_and_color['colorGroups'][0]['colors'][0]['largeSwatchImageUrl']
        zoomed_url = image_url[:-17]
        return zoomed_url

    def get_item_categroy(self, response):
        category = response.xpath('//breadcrumb/nav/ul//li//text()').extract()[1:]
        category = [cat.strip('//') for cat in category]
        category = [i for i in category if i != ' ']
        return category
