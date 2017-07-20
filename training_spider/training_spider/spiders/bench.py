import json
import re
from json.decoder import JSONDecodeError

from scrapy import Spider, Request, FormRequest

from training_spider.items import TrainingSpiderItem


class BenchSpider(Spider):
    name = 'bench'
    start_urls = [
        'https://shop.bench.com.ph/'
    ]

    form_key_re = re.compile('{\"form_key\".*\"}')

    def parse(self, response):
        categories = response.css(
            'script[type="text/x-magento-init"]'
        ).re_first(self.form_key_re)

        category_json = json.loads(categories)

        url = category_json['getTopMenuList']
        form_key = category_json['form_key']

        for category_id in response.css('#pc-nav .level0::attr(data)').re('\d+'):
            yield FormRequest(url,
                              callback=self.parse_categories,
                              formdata={'form_key': form_key,
                                        'categoryId': category_id}
                              )

    def parse_categories(self, response):
        categories = json.loads(response.text)
        categories = categories['AllChildData']

        for category in categories.values():
            url = category['url']
            yield response.follow(url, callback=self.parse_pagination)

            sub_categories = category.get('_child')
            if sub_categories:
                for sub_category in sub_categories.values():
                    url = sub_category['url']
                    yield response.follow(url, callback=self.parse_pagination)

    def parse_pagination(self, response):
        try:
            products = json.loads(response.text)['data']
            for product in products['products']:
                url = product['product_url']
                yield Request(url, callback=self.parse_products)

            next_page = products['cannextload']
            if next_page == 'yes':
                params = response.meta
                params['page_id'] = params['page_id'] + 1
                params_text = params['params_text']
            else:
                return
        except JSONDecodeError:
            product_json = json.loads(
                response.css('#list-div-content script::text').extract_first()
            )['#list-div-content']['Magento_Ui/js/core/app']['components']['listgrid']

            products = product_json['data']['products']
            for product in products:
                product_url = product['product_url']
                yield Request(product_url, callback=self.parse_products)

            params_text = 'a:6:{opening_brace}s:4:"sort";s:0:"";s:4:"page";i:' \
                          '{page_id};''s:10:"searchword";s:0:"";s:7:"storeId";i:' \
                          '{store_id};s:6:"filter";a:0:{braces}s:6:' \
                          '"cateId";i:{cat_id};{closing_brace}'

            params = {
                'pagination_url': product_json['requestUrl'],
                'form_key': product_json['form_key'],
                'cat_id': product_json['cateId'],
                'store_id': product_json['storeId'],
                'page_id': 2,
                'params_text': params_text
            }

        params_text = params_text.format(page_id=params['page_id'],
                                         store_id=params['store_id'],
                                         cat_id=params['cat_id'],
                                         opening_brace='{',
                                         closing_brace='}',
                                         braces='{}'
                                         )
        yield FormRequest(params['pagination_url'],
                          callback=self.parse_pagination,
                          formdata={'form_key': params['form_key'],
                                    'data': params_text},
                          meta=params
                          )

    def parse_products(self, response):
        raw_script = response.css('#main-product-content script::text').extract_first()
        if not raw_script:
            print('Product is not found')
            return

        product = json.loads(raw_script)['#main-product-content']['Magento_Ui/js/core/app']
        product = product['components']['productshow']

        item = TrainingSpiderItem()
        item['product_url'] = response.url
        item['product_id'] = product['data']['id']
        item['product_name'] = response.css('.base::text').extract_first()
        item['currency'] = 'PHP'

        return self.request_product_color(item, product)

    def request_product_color(self, item, product):
        product_info = product['data']
        product_id = product_info['id']
        sizes_and_colors = product_info['config_attr']

        if sizes_and_colors:
            sizes_ids = self.get_sizes_ids(sizes_and_colors)
            product_colors_ids = self.get_colors_ids(sizes_and_colors, sizes_ids)
            product_color_url = self.get_product_colors_url(product, product_id)

            return Request(product_color_url,
                           callback=self.parse_colors,
                           meta={'item': item,
                                 'colors': product_colors_ids}
                           )
        else:
            price = product_info['final_price']
            sale_price = product_info['max_price']
            is_available = True
            main_image = product_info['gallery'][0]['medium']
            images_urls = [image['small'] for image in product_info['gallery']]

            item['variations'] = {
                'price': price,
                'sale_price': sale_price,
                'is_available': is_available,
                'main_image': main_image,
                'images_urls': images_urls
            }
            return item

    def get_product_colors_url(self, product, product_id):
        form_key = product['form_key']
        product_color_url = product['getProductUrl']
        product_color_url = '{url}?id={product_id}&form_key={form_key}'.format(
            url=product_color_url,
            product_id=product_id,
            form_key=form_key
        )
        return product_color_url

    def get_colors_ids(self, sizes_and_colors, sizes_ids):
        product_colors_ids = []
        for size_or_color in sizes_and_colors:
            for color in size_or_color:
                if not color['frontend_label'] == 'Color':
                    continue

                color_label = color['label']
                sizes = self.get_sizes(color, sizes_ids)

                color = {color_label: sizes}
                product_colors_ids.append(color)
        return product_colors_ids

    def get_sizes(self, color, sizes_ids):
        sizes = []
        for product_id in color['product_ids']:
            if sizes_ids:
                size = [siz for siz in sizes_ids if product_id == list(siz.keys())[0]]
                if size:
                    size = size[0]
                else:
                    size = {product_id: '-'}
            else:
                size = {product_id: '-'}

            sizes.append(size)
        return sizes

    def get_sizes_ids(self, sizes_and_colors):
        sizes = []
        for sizes_or_colors in sizes_and_colors:
            for size in sizes_or_colors:
                if not size['frontend_label'] == 'Size':
                    continue
                size_label = size['label']
                for id in size['product_ids']:
                    _size = {id: size_label}
                    sizes.append(_size)
        return sizes

    def parse_colors(self, response):
        meta = response.meta
        item = meta['item']
        colors = meta['colors']
        for color in colors:
            color_key = list(color.keys())[0]
            for size in color[color_key]:
                updated_size = self.update_size(response, size)
                size.update(updated_size)

        item['variations'] = colors
        yield item

    def update_size(self, response, size):
        size_key = list(size.keys())[0]

        for product in json.loads(response.text)['data']:
            if size_key != product['id']:
                continue

            size_label = size.pop(size_key)
            price = product['final_price']
            sale_price = product['max_price']

            is_available = False
            quantity = product['qty']
            if int(float(quantity)):
                is_available = True

            main_image = product['ImgUrl']
            images_urls = [image['small'] for image in product['gallery']]

            updated_size = {
                size_label: {
                    'is_available': is_available,
                    'price': price,
                    'sale_price': sale_price,
                    'main_image': main_image,
                    'images_urls': images_urls}
            }

            return updated_size
