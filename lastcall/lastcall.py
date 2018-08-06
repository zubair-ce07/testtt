# -*- coding: utf-8 -*-
import base64
import copy
import json
import math
import urllib.parse as urlparse

from parsel import Selector
from scrapy import Request, FormRequest, Spider

from products import *


class LastcallSpider(Spider):
    name = 'lastcall'
    blacklist = ['designers', 'fashion dash', 'shop by face shape']
    item_per_page = 30
    seen_cats = set()

    def start_requests(self):
        yield Request(
            url='https://www.lastcall.com/',
            callback=self.parse_homepage
        )

    def parse_homepage(self, response):
        for level_1 in response.css('.silo-trigger'):
            label1 = level_1.css('div a::text').extract_first()
            if label1.lower() in self.blacklist:
                continue

            for level_2 in level_1.css('.silo-column > *'):
                if level_2.css('h6'):
                    label2 = level_2.css('h6 a::text').extract_first().strip()
                    url2 = level_2.css('h6 a::attr(href)').extract_first()

                    yield Request(
                        url=url2,
                        callback=self.parse_category_page,
                        meta={
                            'category': [label1, label2]
                        })
                else:
                    for level_3 in level_2.css('li'):
                        label3 = level_3.css('a::text').extract_first().strip()
                        url3 = level_3.css('a::attr(href)').extract_first()

                        yield Request(
                            url=url3,
                            callback=self.parse_category_page,
                            meta={
                                'category': [label1, label2, label3]
                            })

    def parse_category_page(self, response):
        # handle sub_cats in side bar not stated in main navigation menu
        yield from self.parse_sub_cats(response)

        # handle products on first page
        yield from self.parse_products(response)

        total_items = int(response.css('#numItems::text').extract_first())
        total_page = total_items/self.item_per_page
        total_page = int(math.ceil(total_page)) + 1  # 1 added so that loop sends the last request
        for page_num in range(2, total_page):
            params = self.category_params_data(response, page_num)
            yield FormRequest(
                url='https://www.lastcall.com/category.service',
                formdata=params,
                callback=self.parse_products,
                meta=response.meta,
                dont_filter=True
            )

    def parse_sub_cats(self, response):
        data = response.css('.category-menu-container .active + ul li h2')
        for sub_cat in data.css('a'):
            category_name = sub_cat.css('::text').extract_first().strip()
            if category_name.lower() in self.blacklist:
                continue
            category = copy.deepcopy(response.meta['category'])
            category.append(category_name)
            category_url = sub_cat.css('::attr(href)').extract_first()

            yield Request(
                url=response.urljoin(category_url),
                callback=self.parse_category_page,
                meta={
                    'category': category
                }
            )

    def category_params_data(self, response, page_offset):
        navpath = response.url.split('?')[-1]
        personalized_id = navpath.split('=')[-1]
        personalized_id = personalized_id[6:]
        data = {
            'GenericSearchReq': {
                'pageOffset': page_offset,
                'pageSize': self.item_per_page,
                'refinements': '',
                'selectedRecentSize': '',
                'activeFavoriteSizesCount': '0',
                'activeInteraction': 'true',
                'mobile': 'false',
                'sort': 'PCS_SORT',
                'personalizedPriorityProdId': personalized_id,
                'endecaDrivenSiloRefinements': navpath,
                'definitionPath': '/nm/commerce/pagedef_rwd/template/EndecaDriven',
                'userConstrainedResults': 'true',
                'updateFilter': 'false',
                'rwd': 'true',
                'advancedFilterReqItems': {
                    'StoreLocationFilterReq': [{
                        'allStoresInput': 'false',
                        'onlineOnly': ''}]
                },
                'categoryId': response.css('#endecaContent::attr(categoryid)').extract_first(),
                'sortByFavorites': 'false',
                'isFeaturedSort': 'false',
                'prevSort': ''
            }
        }
        data = json.dumps(data)
        data = base64.b64encode(data.encode())
        data = b'$b64$' + data

        params = {
            'bid': 'GenericSearchReq',
            'data': data.decode('utf-8'),
            'service': 'getCategoryGrid',
            'sid': 'getCategoryGrid'
        }
        return params

    def parse_products(self, response):
        if response.css('#productTemplateId'):
            sel = response
        else:
            data = json.loads(response.text)
            data = data['GenericSearchResp']['productResults']
            sel = Selector(data)
        item_urls = sel.css('#productTemplateId::attr(href)').extract()
        for url in item_urls:
            yield Request(
                url=response.urljoin(url),
                callback=self.parse_item,
                meta=response.meta
            )

    def parse_item(self, response):
        if response.css('.flag-sold-out').extract_first():
            return
        item = ProductItem()
        item['category'] = response.meta['category']
        item['url'] = response.url
        item['retailer_sku'] = response.css('.prod-img::attr(prod-id)').extract_first()

        data_tag = response.css('.product-details-source')
        item['name'] = data_tag.css('span[itemprop="name"]::text').extract_first().strip()
        brand_sel = response.css('[itemprop=brand]')
        brand_sel = brand_sel.css('::attr(content)') or brand_sel.css('::text')
        item['brand'] = brand_sel.extract_first('LastCall').strip()
        item['description'] = [line.strip() for line in data_tag.css('.productCutline div ul li::text').extract()]

        image_urls = self.extract_image_urls(response)
        if isinstance(image_urls, list):
            item['image_urls'] = image_urls
        item['skus'] = []

        full_price = (data_tag.css('.sale-text .item-price::text') or
                      data_tag.css('.product-price::text')).extract_first()
        sale_price = data_tag.css('.promo-price::text').extract_first() or full_price

        params = self.color_params(item['retailer_sku'])
        yield FormRequest(
            url='https://www.lastcall.com/product.service',
            formdata=params,
            callback=self.parse_color,
            meta={
                'full_price': full_price.strip(),
                'sale_price': sale_price.strip(),
                'item': item,
                'image_urls': image_urls
            },
            dont_filter=True
        )

    @staticmethod
    def color_params(retailer_sku):
        data_dict = {
            'ProductSizeAndColor': {
                'productIds': retailer_sku
            }
        }
        data_str = base64.b64encode(json.dumps(data_dict).encode())
        data_str = b'$b64$' + data_str[:-1] + b'$'
        return {
            'bid': 'ProductSizeAndColor',
            'data': data_str.decode('utf-8'),
            'sid': 'getSizeAndColorData'
        }

    @staticmethod
    def parse_color(response):
        data = json.loads(response.text, encoding=response.encoding)
        data = data['ProductSizeAndColor']['productSizeAndColorJSON']
        data = json.loads(data)
        data = data[0]['skus']
        colors_names = set([record.get('color', 'no color').split('?')[0] for record in data])
        color_data = {}
        for color in colors_names:
            item = copy.deepcopy(response.meta['item'])
            item['color'] = color
            color_data.update({
                color: item
            })
        for record in data:
            size_item = SizeItem()
            color_name = record.get('color', 'no color').split('?')[0]
            size_item['size_name'] = record.get('size', 'one_size')
            size_item['in_stock'] = record.get('stockLevel', 0)
            size_item['full_price'] = response.meta['full_price']
            size_item['sale_price'] = response.meta['sale_price']
            color_data[color_name]['skus'].append(size_item)
        image_urls = response.meta['image_urls']
        for color in colors_names:
            item = color_data[color]
            if not item.get('image_urls'):
                item['image_urls'] = image_urls[color]
            yield item

    @staticmethod
    def extract_image_urls(response):
        base_url = response.css('.product-thumbnail::attr(data-zoom-url)').extract()
        if not base_url:
            base_url = [response.css('img[itemprop]::attr(data-zoom-url)').extract_first()]
        image_urls = {}
        for color in response.css('.color-picker'):
            color_name = color.css('::attr(data-color-name)').extract_first()
            color_dict = color.css('::attr(data-sku-img)').extract_first()
            color_dict = json.loads(color_dict)

            url_list = []
            for sku_value in color_dict.values():
                url_parts = urlparse.urlparse(base_url[0])
                path = url_parts[2].split('/')
                path[-1] = sku_value
                url_list.append(url_parts._replace(path='/'.join(path), scheme='https').geturl())

            image_urls.update({
                color_name: url_list
            })
        return image_urls or base_url
