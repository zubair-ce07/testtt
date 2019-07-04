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
        categories = response.css("a.breadcrumb-label::text").getall()
        item_id = response.css(".jrb-product-view::attr(data-entity-id)").get()
        attr_for_color = response.css(".form-field input.form-radio::attr(name)").get()
        attr_for_size = response.css(".product-size input.form-radio::attr(name)").get()

        color_ids = response.css((".productView-options .form-option-swatch:not(.swatch-show-"
                                        "product)::attr(data-product-attribute-value)")).getall()

        color_names = response.css((".productView-options .form-option-swatch:not"
                                        "(.swatch-show-product)::attr(title)")).getall()

        size_ids = response.css((".productView-options .product-size input.form-radio"
                                        "::attr(value)")).getall()

        size_names = response.css((".productView-options .product-size .form-option"
                                        " span.form-option-variant::text")).getall()
        
        gender = "Male" if "Men" in categories else "Female" if "Women" in categories else "Unisex"
        variants = []
        item = {
            'sku': response.css(".parent-sku::text").get(),
            'name': response.css(".productView-title::text").get(),
            'url': response.url,
            'date': time.time(),
            'description': response.css("#details-content::text").get(),
            'categories': categories,
            'price': response.css(".price.price--withoutTax.bfx-price::text").get(),
            'gender': gender,
            'image-urls': response.css("#zoom-modal img::attr(src)").getall(),
            'id': item_id,
            'variants': variants
        }

        sku_url = f"{self.attr_url}{item_id}"
        sparse_combinations = list(product(color_ids, size_ids))
        combinations = [pair for pair in sparse_combinations if pair[0] and pair[1]]
        if combinations:
            temp_color = combinations[0][0]
            temp_size = combinations[0][1]
            form_data = {
                'action': 'add',
                attr_for_color: temp_color,
                attr_for_size: temp_size,
                'product_id': item_id,
                'qty[]': '1'
            }
            combinations.pop(0)
            meta_data = {
                'pairs': combinations,
                'color_attr': attr_for_color,
                'size_attr': attr_for_size,
                'item_id': item_id,
                'color': color_names[color_ids.index(temp_color)],
                'size': size_names[size_ids.index(temp_size)],
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
        new_variant = {
                    'sku': obj['data']['sku'],
                    'price': obj['data']['price']['without_tax']['formatted'],
                    'color': response.meta['color'],
                    'size': response.meta['size'],
                    'availability': obj['data']['instock']
                }
        response.meta['item']['variants'].append(new_variant)
        if response.meta['pairs']:
            sku_url = f"{self.attr_url}{response.meta['item_id']}"
            temp_color = response.meta['pairs'][0][0]
            temp_size = response.meta['pairs'][0][1]
            form_data = {
                'action': 'add',
                response.meta['color_attr']: temp_color,
                response.meta['size_attr']: temp_size,
                'product_id': response.meta['item_id'],
                'qty[]': '1'
            }
            response.meta['pairs'].pop(0)
            meta_data = {
                'pairs': response.meta['pairs'],
                'color_attr': response.meta['color_attr'],
                'size_attr': response.meta['size_attr'],
                'item_id': response.meta['item_id'],
                'color': response.meta['color_names'][response.meta['color_ids'].index(temp_color)],
                'size': response.meta['size_names'][response.meta['size_ids'].index(temp_size)],
                'color_names': response.meta['color_names'],
                'size_names': response.meta['size_names'],
                'color_ids': response.meta['color_ids'],
                'size_ids': response.meta['size_ids'],
                'item': response.meta['item']
            }
            yield scrapy.FormRequest(
                url = sku_url,
                formdata = form_data,
                meta = meta_data,
                callback = self.parse_skus
            )
        else:
            yield response.meta['item']
