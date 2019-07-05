import re
import time
import json
import scrapy

from itertools import product
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ProductsSpider(CrawlSpider):
    name = "woolrich"
    start_urls = [
        'https://www.woolrich.com/'
    ]
    attr_url = "https://www.woolrich.com/remote/v1/product-attributes/"
    rules = (
        Rule(LinkExtractor(restrict_css = ["#primary > ul > li", ".pagination-item--next"])),
        Rule(LinkExtractor(restrict_css = ".card-figure"), callback = "parse_item")
    )

    def parse_item(self, response):
        attr_for_size = response.css(".productView-details .product-size"
                                    " .form-radio::attr(name)").get()
        attr_for_color = (
            f"attribute["
            f"{response.css('.productView-details [data-swatch-id]::attr(data-swatch-id)').get()}"
            f"]"
        )
        size_ids = response.css(".productView-options .product-size .form-radio"
                                    "::attr(value)").getall()
        color_ids = response.css(".productView-options [aria-checked]::attr(value)").getall()
        color_names = response.css(".productView-options [data-swatch-id]::attr(title)").getall()
        size_names = response.css(".productView-options .product-size .form-option span"
                                    "::text").getall()
        categories = response.css(".breadcrumb-label::text").getall()
        item_id = response.css(".jrb-product-view::attr(data-entity-id)").get()
        gender = "Men" if "Men" in categories else "Women" if "Women" in categories else "Unisex"
        price = response.css(".productView-details .price::text").get()
        separated_price = self.split_price(price)
        item = {
            'retailer_sku': response.css(".parent-sku::text").get(),
            'lang': response.css("html::attr(lang)").get(),
            'gender': gender,
            'category': categories,
            'url': response.url,
            'date': time.time(),
            'market': response.css(".navPages-item--location img::attr(alt)").get(),
            'name': response.css(".productView-title::text").get(),
            'description': response.css("#details-content::text").getall(),
            'care': response.css("ul#features-content li::text").getall(),
            'image_urls': response.css("#zoom-modal img::attr(src)").getall(),
            'skus': {},
            'price': float(separated_price[1]),
            'currency': separated_price[0]
        }
        sku_url = f"{self.attr_url}{item_id}"
        combinations = list(product(color_ids, size_ids))
        if combinations:
            (color, size) = combinations.pop()
            form_data = {
                'action': 'add',
                attr_for_color: color,
                attr_for_size: size,
                'product_id': item_id,
                'qty[]': '1'
            }
            meta_data = {
                'pairs': combinations,
                'color_attr': attr_for_color,
                'size_attr': attr_for_size,
                'item_id': item_id,
                'color': color_names[color_ids.index(color)],
                'size': size_names[size_ids.index(size)],
                'color_names': color_names,
                'size_names': size_names,
                'color_ids': color_ids,
                'size_ids': size_ids,
                'item': item
            }
            yield scrapy.FormRequest(
                url = sku_url,
                formdata = form_data,
                meta = meta_data,
                callback = self.parse_skus
            )
    
    def parse_skus(self, response):
        obj = json.loads(response.text)
        price = obj['data']['price']['without_tax']['formatted']
        price_separated = self.split_price(price)
        if 'rrp_without_tax' in obj['data']['price']:
            previous_price_formatted = obj['data']['price']['rrp_without_tax']['formatted']
            previous_price = float(self.split_price(previous_price_formatted)[1].replace(',', ''))
        else:
            previous_price = None
        sku = {
                    obj['data']['sku']: {
                        'price': float(price_separated[1].replace(',', '')),
                        'currency': price_separated[0],
                        'previous_prices': previous_price,
                        'color': response.meta['color'],
                        'size': response.meta['size'],
                        'availability': obj['data']['instock']
                    }   
                }
        response.meta['item']['skus'].update(sku)
        if response.meta['pairs']:
            sku_url = f"{self.attr_url}{response.meta['item_id']}"
            (color, size) = response.meta['pairs'].pop()
            form_data = {
                'action': 'add',
                response.meta['color_attr']: color,
                response.meta['size_attr']: size,
                'product_id': response.meta['item_id'],
                'qty[]': '1'
            }
            meta_data = response.meta
            meta_data['color'] = meta_data['color_names'][meta_data['color_ids'].index(color)]
            meta_data['size'] = meta_data['size_names'][meta_data['size_ids'].index(size)]
            yield scrapy.FormRequest(
                url = sku_url,
                formdata = form_data,
                meta = meta_data,
                callback = self.parse_skus
            )
        else:
            yield response.meta['item']

    def split_price(self, price):
        return re.split(r'([0-9]*[,]*[0-9]*[.][0-9]*)', price)
