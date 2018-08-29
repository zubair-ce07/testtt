import copy
import json

import scrapy
from scrapy import Selector

from hm.items import ProductItem, SizeItem


class HMSpider(scrapy.Spider):
    name = 'hm'
    start_urls = [
        'https://kw.hm.com/en'
    ]

    def parse(self, response):
        for level_1_selector in response.css('li.menu--one__list-item'):
            anchor_selector = level_1_selector.css('a.menu--one__link')
            cat_1 = anchor_selector.css('::text').extract_first().strip()
            level_1_url = anchor_selector.css('::attr(href)').extract_first()
            level_2 = level_1_selector.css('li.menu--two__list-item')

            if not level_2:
                url = response.urljoin(level_1_url)
                yield scrapy.Request(url,
                                     meta={'category': [cat_1], 'link': url},
                                     callback=self.parse_listing_page)

            for level_2_selector in level_2:
                anchor_selector = level_2_selector.css('a.menu-two__link')
                cat_2 = anchor_selector.css('::text').extract_first().strip()
                level_2_url = anchor_selector.css('::attr(href)').extract_first()
                level_3 = level_2_selector.css('li.menu--three__list-item')

                if not level_3:
                    url = response.urljoin(level_2_url)
                    yield scrapy.Request(url,
                                         meta={'category': [cat_1, cat_2], 'link': url},
                                         callback=self.parse_listing_page)

                for level_3_selector in level_3:
                    anchor_selector = level_3_selector.css('a.menu--three__link')
                    cat_3 = anchor_selector.css('::text').extract_first().strip()
                    level_3_url = anchor_selector.css('::attr(href)').extract_first()
                    url = response.urljoin(level_3_url)
                    yield scrapy.Request(url,
                                         meta={'category': [cat_1, cat_2, cat_3], 'link': url},
                                         callback=self.parse_listing_page)

    def parse_listing_page(self, response):
        product_links = response.css('.field__items .field__item > a::attr(href)').extract()

        for product_link in product_links:
            product_link = response.urljoin(product_link)
            yield scrapy.Request(product_link, meta=response.meta, callback=self.parse_data)

        url = response.css('li.pager__item a.button::attr(href)').extract_first('')
        if url:
            yield scrapy.Request(response.urljoin(url),
                                 meta=response.meta,
                                 callback=self.parse_listing_page)

    def parse_data(self, response):
        product = ProductItem()
        # Assign website details its name & url through meta
        product['referrer_url'] = response.meta.pop('link')
        # Initialize the dict to store the color & size information
        product['skus'] = []
        product['image_urls'] = []
        product['url'] = response.url
        product['retailer_sku'] = response.css('#block-content ::attr(gtm-product-sku)').extract_first()
        data_sku_id = response.css('.basic-details-wrapper ::attr(data-skuid)').extract_first()
        product['brand'] = response.css('.site-brand-home a::attr(title)').extract_first('H&M')
        product['care'] = response.css('.description-wrapper .care-instructions-value::text').extract_first()
        product['description'] = [element.strip() for element in response.css(
            '.description-wrapper .desc-value::text').extract() if element.strip()]
        product['category'] = response.meta.pop('category')
        product['product_name'] = response.css('.content__title_wrapper h1 > ::text').extract_first('No Title')
        product['currency'] = response.css('.content__title_wrapper .price-currency ::text').extract_first('KWD')

        params = '/{}/get-cart-form/full/{}?_wrapper_format=drupal_ajax'.format('en', data_sku_id)

        yield scrapy.Request(response.urljoin(params),
                             meta={'product': product,
                                   'data_sku_id': data_sku_id},
                             callback=self.fetch_product_color)

    def fetch_product_color(self, response):
        product = response.meta['product']
        data = json.loads(response.css('textarea::text').extract_first())
        settings = form_data = {}
        for element in data:
            if element.get('command') == 'settings':
                settings = element.get('settings')
            elif element.get('method') == 'html':
                form_data = element.get('data')

        if not (settings and form_data):
            yield product
            return

        color_items = settings['sku_configurable_options_color']

        form_response = Selector(text=form_data.strip())
        data_sku_key = form_response.css('input[name=form_id]::attr(value)').extract_first()

        params = '/{}/select-configurable-option/{}?_wrapper_format=drupal_ajax'.\
            format('en', response.meta['data_sku_id'])
        url = response.urljoin(params)
        for color_id, color_data in color_items.items():
            product['color_id'] = color_id
            product['color_name'] = color_data['display_label'] or 'no color'
            response.meta.update({'product': copy.deepcopy(product), 'data_sku_key': data_sku_key})
            yield scrapy.FormRequest(url,
                                     meta=response.meta,
                                     formdata=self.create_form_data(color_id,
                                                                    response.meta['data_sku_id'],
                                                                    data_sku_key),
                                     callback=self.parse_color)

    def parse_color(self, response):
        product = response.meta['product']

        data = json.loads(response.css('textarea::text').extract_first())
        div_selector = ''
        for element in data:
            if element.get('method') == 'replaceDynamicParts':
                div_selector = Selector(text=element['args'][0]['replaceWith'])
                break

        options_selector = div_selector.css('.form-item-configurables-size > .form-select > option:not([disabled])')
        size_collection = dict(zip(options_selector.css('::attr(value)').extract(),
                                   options_selector.css('::text').extract()))

        product['image_urls'] = div_selector.css('.cloudzoom__thumbnails li > a::attr(href)').extract()

        response.meta.update({'size_collection': size_collection})
        yield from self.item_or_request(response)

    def parse_size(self, response):
        data = json.loads(response.css('textarea::text').extract_first())
        div_selector = response
        for element in data:
            if element.get('method') == 'html':
                div_selector = Selector(text=element['data'])
                break

        product = response.meta['product']

        # Populating attributes of Size Item
        size_item = self.fill_size_item(div_selector, *response.meta['item'])

        product['skus'].append(size_item)
        yield from self.item_or_request(response)

    def fill_size_item(self, response, size_identifier, size_name):
        size_item = SizeItem()
        size_item['size_identifier'] = size_identifier
        size_item['size_name'] = size_name
        size_item['stock'] = 1
        size_item['full_price'] = response.css('.price-amount::text').extract_first()
        size_item['sale_price'] = response.css('.special--price .price-amount::text').extract_first(
            size_item['full_price'])
        return size_item

    def item_or_request(self, response):
        product = response.meta['product']
        size_collection = response.meta['size_collection']
        if size_collection:
            item = size_collection.popitem()
            response.meta.update({'item': item})
            yield scrapy.FormRequest(response.url,
                                     meta=response.meta,
                                     formdata=self.create_form_data(product['color_id'],
                                                                    response.meta['data_sku_id'],
                                                                    response.meta['data_sku_key'],
                                                                    'size',
                                                                    item[0]),
                                     callback=self.parse_size)
        else:
            yield product

    def create_form_data(self, color_id, sku_id, sku_key, configurable_key='article_castor_id', size_id=''):
        return {'configurables[article_castor_id]': color_id,
                'configurables[size]': size_id,
                'sku_id': sku_id,
                'form_id': sku_key,
                '_triggering_element_name': 'configurables[{}]'.format(configurable_key)}

