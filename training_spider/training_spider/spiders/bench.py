import json
import re
from json.decoder import JSONDecodeError

from urllib.parse import urljoin

from copy import deepcopy
from scrapy import Spider, Request, FormRequest, Selector

from training_spider.items import TrainingSpiderItem


class BenchSpider(Spider):
    name = 'bench'
    start_urls = [
        'https://shop.bench.com.ph/'
    ]

    form_key_re = re.compile('{\"form_key\".*\"}')

    params_text_t = 'a:6:{{s:4:"sort";s:0:"";s:4:"page";i:{params[page_id]};''' \
                    's:10:"searchword";s:0:"";s:7:"storeId";i:{params[store_id]};s:6:"filter";' \
                    'a:0:{{}}s:6:"cateId";i:{params[cat_id]};}}'

    def parse(self, response):
        categories = response.css(
            'script[type="text/x-magento-init"]'
        ).re_first(self.form_key_re)

        category_json = json.loads(categories)

        categories_url = category_json['getTopMenuList']
        form_key = category_json['form_key']

        for category_id in response.css('#pc-nav .level0::attr(data)').re('\d+'):
            form_data = {'form_key': form_key,
                         'categoryId': category_id
                         }
            yield FormRequest(categories_url,
                              callback=self.parse_categories,
                              formdata=form_data
                              )
            break

    def parse_categories(self, response):
        categories = json.loads(response.text)
        categories = categories['AllChildData']

        for category in self.traverse_categories(response, categories):
            yield category
            break

    def traverse_categories(self, response, categories):
        for category in categories.values():
            url = category['url']
            yield Request(urljoin(response.url, url),
                          callback=self.parse_products,
                          )

            sub_categories = category.get('_child', {})
            yield self.traverse_categories(response, sub_categories)
            break

    def parse_products(self, response):
        raw_script = response.css('#list-div-content script::text').extract_first()
        raw_json = json.loads(raw_script)
        products_grid = raw_json['#list-div-content']
        products_grid = products_grid['Magento_Ui/js/core/app']['components']['listgrid']
        products_details = products_grid['data']

        for detail in products_details['products']:
            url = detail['product_url']

            yield Request(url,
                          callback=self.parse_details,
                          )

        params = {
            'pagination_url': products_grid['requestUrl'],
            'form_key': products_grid['form_key'],
            'cat_id': products_grid['cateId'],
            'store_id': products_grid['storeId'],
            'page_id': 2,
        }
        yield self.request_pagination(params)

    def request_pagination(self, params):
        self.logger.info('request_pagination')
        params_text = self.params_text_t.format(params=params)
        form_data = {
            'form_key': params['form_key'],
            'data': params_text
        }
        return FormRequest(params['pagination_url'],
                           callback=self.parse_pagination,
                           formdata=form_data,
                           meta=params
                           )

    def parse_pagination(self, response):
        self.logger.info('pagination')
        products = json.loads(response.text)['data']

        for detail in products['products']:
            url = detail['product_url']
            yield Request(url,
                          callback=self.parse_details,
                          )
            break

        next_page = products['cannextload']
        if next_page == 'yes':
            params = response.meta
            params['page_id'] = params['page_id'] + 1
            yield self.request_pagination(params)

    def parse_details(self, response):
        self.logger.info('Parse_Details')
        raw_script = response.css('#main-product-content script::text').extract_first()
        if not raw_script:
            self.logger.info('Product is not found')
            return

        raw_json = json.loads(raw_script)['#main-product-content']['Magento_Ui/js/core/app']
        raw_json = raw_json['components']['productshow']
        product_detail = raw_json['data']

        item = TrainingSpiderItem()
        item['product_url'] = response.url
        item['product_id'] = product_detail['id']
        item['product_name'] = response.css('.base::text').extract_first()
        item['currency'] = 'PHP'
        item['country'] = 'ph'

        variations = product_detail['config_attr']
        if variations:
            return self.request_product_color(item, raw_json, product_detail, variations)
        else:
            return self.items_without_variation(item, product_detail)

    def request_product_color(self, item, raw_json, product_datail, variations):
        self.logger.info('request_products')
        product_id = product_datail['id']
        size_mappings = self.get_size_mapping(variations)
        colors_mappings = self.get_colors_mappings(variations, size_mappings)
        product_color_url = self.get_product_colors_url(raw_json, product_id)
        meta = {'item': item,
                'colors': colors_mappings,
                }
        yield Request(product_color_url,
                      callback=self.parse_colors,
                      meta=meta)

    def get_product_colors_url(self, product, product_id):
        self.logger.info('Parse_Colors')
        form_key = product['form_key']
        product_color_url = product['getProductUrl']
        product_color_url = '{url}?id={product_id}&form_key={form_key}'.format(
            url=product_color_url,
            product_id=product_id,
            form_key=form_key
        )
        return product_color_url

    def parse_colors(self, response):
        self.logger.info('Parse_Colors')
        meta = response.meta
        item = meta['item']
        colors = meta['colors']
        variations = []

        for color in colors:
            size_mappings = color['size_mappings']
            color_name = color['color_name']
            color_code = color['color_code']
            color_key = '{}_{}'.format(color_name, color_code)

            color_value = self.get_variations(response, color, size_mappings)
            variations.append({color_key: color_value})

        item['variations'] = variations
        yield item

    def get_variations(self, response, color, size_mappings):
        self.logger.info('Parse_color_variations')
        images_urls = []
        sizes = []
        for product_info in json.loads(response.text)['data']:
            product_id = product_info['id']
            if product_id not in color['product_ids']:
                continue

            if size_mappings:
                size = self.get_size_item(product_info, size_mappings[product_id])
                sizes.append(size)
            else:
                price = product_info['max_price']
                sale_price = product_info['final_price']

                is_available = False
                quantity = product_info.get('qty')
                if float(quantity):
                    is_available = True
                sizes = {
                    '-': {
                        'price': price,
                        'sale_price': sale_price,
                        'is_available': is_available
                    }
                }
            if not images_urls:
                images_urls = [image.get('base', image.get('medium', ''))
                               for image in product_info['gallery']
                               ]
        variations = {
            'sizes': sizes,
            'images_urls': images_urls
        }
        return variations

    def get_size_item(self, item_detail, size):
        price = item_detail['max_price']
        sale_price = item_detail['final_price']
        size_name = size['size_name']

        is_available = False
        quantity = item_detail.get('qty')
        if float(quantity):
            is_available = True
        size = {
            size_name: {
                'price': price,
                'sale_price': sale_price,
                'is_available': is_available
            }
        }
        return size

    def get_colors_mappings(self, variations, size_mappings):
        colors_mappings = []
        for size_or_color in variations:
            for element in size_or_color:
                if not element['frontend_label'] == 'Color':
                    continue

                sizes = {}
                if size_mappings:
                    for product_id in element['product_ids']:
                        sizes.update({product_id: size_mappings[product_id]})

                element = {
                    'color_code': element['option_id'],
                    'color_name': element['label'],
                    'size_mappings': sizes,
                    'product_ids': element['product_ids']
                }
                colors_mappings.append(element)
        return colors_mappings

    def get_size_mapping(self, variations):
        size_mappings = {}
        for sizes_or_colors in variations:
            for element in sizes_or_colors:
                if not element['frontend_label'] == 'Size':
                    continue

                size_name = element['label']
                size_code = element['option_id']
                for product_id in element['product_ids']:
                    size_mappings.update({
                        product_id: {
                            'size_name': size_name,
                            'size_code': size_code}
                    })
        return size_mappings

    def get_description(self, item_detail):
        short_description = Selector(text=item_detail['shot_description'])
        return short_description.css('::text').extract()

    def items_without_variation(self, item, item_detail):
        price = item_detail['max_price']
        sale_price = item_detail['final_price']
        is_available = True
        image_urls = [image.get('base',
                                image.get('medium', '')
                                )
                      for image in item_detail['gallery']
                      ]
        variation = {
            'price': price,
            'sale_price': sale_price,
            'is_available': is_available,
            'image_urls': image_urls
        }

        item['variations'] = variation
        return item
