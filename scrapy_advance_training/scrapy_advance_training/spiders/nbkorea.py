# -*- coding: utf-8 -*-
import json
import re
from copy import deepcopy
from math import ceil
from urllib import parse

from scrapy import FormRequest, Request, Spider

from scrapy_advance_training.items import ProductItem, SizeInfosItem


class NbkoreaSpider(Spider):
    page_size = '15'

    name = 'nbkorea'
    start_urls = ['https://www.nbkorea.com/']

    total_items_re = re.compile('[0-9]+')

    product_url_t = 'https://www.nbkorea.com/product/productDetail.action?' \
                    'styleCode={}&colCode={}&cIdx={}'
    pagination_url_t = 'https://www.nbkorea.com/product/searchResultFilter.action'

    def parse(self, response):
        nav_urls = response.css('.menu .nav')[:-1].css('div li a::attr(href)').extract()
        for url in nav_urls:
            if '/etc/' not in url and '/lunchingCalendar/' not in url:
                yield Request(response.urljoin(url), self.parse_products)

    def parse_products(self, response):
        if not response.meta.get('pagination'):
            category_names = response.css('.category_title a::text').extract() \
                             + response.css('.category_title h2::text').extract()

            for product in response.css('#prodList li >a'):
                cidx = product.css('::attr(data-cidx)').extract_first()
                style_code = product.css('::attr(data-style)').extract_first()
                color_code = product.css('::attr(data-color)').extract_first()
                yield self.request_product(cidx, color_code, style_code, category_names)
            yield from self.request_pagination(response, category_names)
        else:
            products = json.loads(response.text)
            for product in products['resultList']:
                cidx = product['CIdx']
                color_code = product['ColCode']
                style_code = product['StyleCode']
                yield self.request_product(cidx, color_code, style_code, response.meta['cate_names'])

    def request_pagination(self, response, category_names):
        parsed_products = len(response.css('#prodList li >a'))
        total_products = response.css('.gathering .on span::text').re_first(self.total_items_re)

        if not total_products:
            return

        if int(total_products) == parsed_products:
            return

        total_pages = int(ceil(float(total_products) / float(self.page_size)))
        params = {
            'pageSize': self.page_size,
            'cateGrpCode': self.get_id(response.url, 'cateGrpCode'),
            'cIdx': response.css('#prodList li >a::attr(data-cidx)').extract_first(),
        }
        sub_cate_idx = response.css('.ip_chekbox[name="subCateIdx"]::attr(value)').extract()
        if sub_cate_idx:
            params['subCateIdx[]'] = sub_cate_idx

        for page_no in range(2, total_pages+1):
            params['pageNo'] = str(page_no)
            yield FormRequest(
                formdata=params,
                url=self.pagination_url_t,
                callback=self.parse_products,
                meta={'cate_names': category_names, 'pagination': True},
            )

    @staticmethod
    def get_id(link, key):
        url_parse = parse.urlparse(link)
        url_info = dict(parse.parse_qsl(url_parse.query))
        return url_info.get(key)

    def request_product(self, cidx, color_code, style_code, category_names):
        url = self.product_url_t.format(style_code, color_code, cidx)
        return Request(url, self.parse_product, meta={'cate_names': category_names})

    def parse_product(self, response):
        currency = response.css('.price .won::text').extract_first()
        price = response.css('.price .won strong::text').extract_first()

        product_item = ProductItem(
            brand='NB',
            size_infos=[],
            old_price_text='',
            currency=currency,
            country_code='kr',
            url=response.url,
            new_price_text=price,
            category_names=response.meta['cate_names'],
            full_price_text='{}{}'.format(price, currency),
            referer_url=response.request.headers.get('Referer', ''),
            base_sku=response.css('.info_list div::text').extract_first(),
            language_code=response.css('html::attr(lang)').extract_first(),
            title=response.css('#displayName.title::text').extract_first(),
            description_text=response.css('.info_list div p::text').extract()
        )
        yield from self.parse_color(product_item, response)

    def parse_color(self, product_item, response):
        image_urls = response.css('.pr_visual .thumb img::attr(src)').extract()

        for color in response.css('.color ul input'):
            product_itm = deepcopy(product_item)

            product_itm['color_code'] = color.css('::attr(value)').extract_first()
            product_itm['color_name'] = color.css('::attr(data-info)').extract_first()
            product_itm['image_urls'] = [self.get_image_url(product_itm['color_code'], image)
                                         for image in image_urls]
            product_itm['sku'] = '{}{}'.format(product_itm['base_sku'], product_itm['color_code'])
            product_itm['identifier'] = product_itm['sku']

            self.parse_size(product_itm, response)
            yield product_itm

    @staticmethod
    def parse_size(product_item, response):
        availability = False
        for size in response.css('#optSizeSection input'):
            disabled = size.css('::attr(disabled)').extract_first('')
            size_item = SizeInfosItem(
                stock=0 if disabled else 1,
                size_name=size.css('::attr(data-info)').extract_first(),
                size_identifier=size.css('::attr(value)').extract_first()
            )
            product_item['size_infos'].append(size_item)

            if not disabled and not availability:
                availability = True
        product_item['available'] = availability

    @staticmethod
    def get_image_url(color_id, image_url):
        url_parts = image_url.split('_')
        url_parts[-2] = color_id
        return '_'.join(url_parts)
