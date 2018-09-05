# -*- coding: utf-8 -*-
import re
from copy import deepcopy
from json import loads

from scrapy import Request, Spider

from scrapy_advance_training.items import ProductItem, SizeInfosItem


class StoriesSpider(Spider):
    name = 'stories'
    allowed_domains = ['stories.com']
    color_code_re = re.compile('[0-9]+')

    def start_requests(self):
        urls = {
            'us': ('en', 'https://www.stories.com/en_usd/'),
            'gb': ('en', 'https://www.stories.com/en_gbp/'),
            'dk': ('en', 'https://www.stories.com/en_dkk/'),
        }
        for country_code, value in urls.items():
            language_code, url = value
            meta = {'country_code': country_code, 'language_code': language_code}
            yield Request(url, self.parse, meta=meta)

    def parse(self, response):
        for category in response.css('.categories a'):
            category_names = [category.css('::text').extract_first('').strip()]
            response.meta['category_names'] = category_names
            yield Request(category.css('::attr(href)').extract_first(),
                          self.parse_products,
                          meta=response.meta)

    def parse_products(self, response):
        category_names = response.meta['category_names']
        for sub_category in response.css('.subcategories a'):
            cat_names = deepcopy(category_names)
            cat_names += [sub_category.css('::text').extract_first('').strip()]
            response.meta['category_names'] = cat_names
            yield Request(sub_category.css('::attr(href)').extract_first(),
                          self.parse_products,
                          meta=response.meta)

        for product_url in response.css('#reloadProducts a::attr(href)').extract():
            yield Request(response.urljoin(product_url),
                          self.parse_product,
                          meta=response.meta)

    def parse_product(self, response):
        description_text = response.css('meta[property="og:description"]::attr(content)').extract()
        currency = response.css('meta[property="og:price:currency"]::attr(content)').extract_first()

        product_item = ProductItem(
            brand='stories',
            currency=currency,
            description_text=description_text,
            country_code=response.meta['country_code'],
            language_code=response.meta['language_code'],
            category_names=response.meta['category_names'],
            title=response.css('#productTitle::text').extract_first(),
        )

        for color in response.css('#swatchDropdown .options li'):
            color_code = color.css('::attr(data-articlecode)').extract_first()
            color_name = color.css('::attr(data-value)').extract_first()
            url = re.sub(self.color_code_re, color_code, response.url)

            meta = {'color_name': color_name,
                    'color_code': color_code,
                    'product_item': deepcopy(product_item)}
            yield Request(url, self.parse_color, meta=meta, dont_filter=True)

    def parse_color(self, response):
        product_item = response.meta['product_item']
        product_item['color_code'] = response.meta['color_code']
        product_item['color_name'] = response.meta['color_name']

        old_price, new_price = self.extract_price(response)
        identifier = response.css('.o-olapic-gallery::attr(data-product-id)').extract_first()

        product_item['sku'] = identifier
        product_item['url'] = response.url
        product_item['available'] = 'true'
        product_item['old_price_text'] = old_price.strip()
        product_item['identifier'] = identifier
        product_item['base_sku'] = identifier[:7]
        product_item['new_price_text'] = new_price.strip()
        product_item['full_price_text'] = new_price.strip()
        product_item['image_urls'] = self.get_image_urls(response)
        product_item['referer_url'] = response.request.headers.get('Referer', '')
        yield self.parse_size(response, product_item)

    @staticmethod
    def extract_price(response):
        new_price_text = response.css('.price-value::text').extract_first('').strip()
        if new_price_text:
            return '', new_price_text

        return response.css('#product-price label::text').extract()

    @staticmethod
    def parse_size(response, product_item):
        sizes = response.css('.o-page-content >script::text').extract_first().strip()
        sizes = ' '.join(text.strip() for text in sizes.split('\t'))
        sizes = sizes.replace(' ', '').replace('varproductArticleDetails=', '').replace(';', '')
        sizes = sizes.replace(',}', '}').replace('\'', '"')
        index = sizes.find('themeName')
        if index != -1:
            sizes = sizes.replace(sizes[index:], '')
            sizes = sizes[:-2]
        sizes = sizes.replace(sizes[:sizes.find('variants')-1], '').replace('"variants":', '')
        index = sizes.find('productFrontImages')
        if index != -1:
            sizes = sizes.replace(sizes[index-2:], '')
        sizes = loads(sizes)

        product_item['size_infos'] = list()
        
        for size in sizes:
            size_item = SizeInfosItem(
                stock=1,
                size_name=size['sizeName'],
                size_identifier=size['sizeCode']
            )
            product_item['size_infos'].append(size_item)
        return product_item

    @staticmethod
    def get_image_urls(response):
        return [
            response.urljoin(url)
            for url in response.css('#imageContainer img::attr(src)').extract()
        ]
