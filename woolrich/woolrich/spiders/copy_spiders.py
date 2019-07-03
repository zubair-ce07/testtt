import time
import json
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ProductsSpider(CrawlSpider):
    name = "copies"
    start_urls = [
        'https://www.woolrich.com/'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css="#primary > ul:nth-child(3) > li")),
        Rule(LinkExtractor(restrict_css=".pagination-item--next")),
        Rule(LinkExtractor(restrict_css=".card-figure"), 
                            callback = "parse_item")
    )
    def parse_item(self, response):
        categories = response.css(".jrb-product-view::attr(data-product-category)").get()
        item_id = response.css(".jrb-product-view::attr(data-entity-id)").get()
        attr_for_color = response.css((".productView-options .form-field:not(.product-size) "
                                        "input.form-radio::attr(name)")).get()
        attr_for_size = response.css(".productView-options .product-size input.form-radio::attr(name)").get()
        color_ids = response.css((".productView-options .form-option-swatch:not(.swatch-show-product)"
                                        "::attr(data-product-attribute-value)")).getall()
        color_names = response.css((".productView-options .form-option-swatch:not(.swatch-show-product)"
                                        "::attr(title)")).getall()
        size_ids = response.css(".productView-options .product-size input.form-radio::attr(value)").getall()
        size_names = response.css((".productView-options .product-size "
                                        ".form-option span.form-option-variant::text")).getall()
        
        gender = "Male" if "Men" in categories else "Female" if "Women" in categories else "Unisex"
        variants = []
        data_to_yield = {
            'sku': response.css(".parent-sku::text").get(),
            'name': response.css(".productView-title::text").get(),
            'url': response.url,
            'date': time.time(),
            'description': response.css("#details-content::text").get(),
            'categories': categories,
            'price': response.css(".price.price--withoutTax.bfx-price::text").get(),
            'gender': gender,
            'image-urls': response.css("#zoom-modal img::attr(src)").getall(),
            'colors': response.css(".productView-options .form-option-variant--pattern::attr(title)").getall(),
            'id': item_id,
            'variants': variants
        }
        url_new = f"https://www.woolrich.com/remote/v1/product-attributes/{item_id}"
        combinations = []
        for color in color_ids:
            for size in size_ids:
                combinations.append(tuple((color, size)))
        if combinations:
            temp_color = combinations[0][0]
            temp_size = combinations[0][1]
            color_name = color_names[color_ids.index(temp_color)]
            size_name = size_names[size_ids.index(temp_size)]
            combinations.pop(0)
            form_data = {
                'action': 'add',
                attr_for_color: temp_color,
                attr_for_size: temp_size,
                'product_id': item_id,
                'qty[]': '1'
            }
            meta_data = {
                'combs': combinations,
                'color_attr': attr_for_color,
                'size_attr': attr_for_size,
                'itemid': item_id,
                'color': color_name,
                'size': size_name,
                'color_names': color_names,
                'size_names': size_names,
                'color_ids': color_ids,
                'size_ids': size_ids,
                'main_object': data_to_yield
            }
            yield scrapy.FormRequest(
                url = url_new,
                formdata = form_data,
                meta = meta_data,
                callback = self.each_type
            )
    
    def each_type(self, response):
        obj = json.loads(response.text)
        new_type = {
                    'sku': obj['data']['sku'],
                    'price': obj['data']['price']['without_tax']['formatted'],
                    'color': response.meta['color'],
                    'size': response.meta['size'],
                    'availability': obj['data']['instock']
                }
        response.meta['main_object']['variants'].append(new_type)
        print(self.data_to_yield)
        if response.meta['combs']:
            url_new = f"https://www.woolrich.com/remote/v1/product-attributes/{response.meta['itemid']}"
            temp_color = response.meta['combs'][0][0]
            temp_size = response.meta['combs'][0][1]
            color_name = response.meta['color_names'][response.meta['color_ids'].index(temp_color)]
            size_name = response.meta['size_names'][response.meta['size_ids'].index(temp_size)]
            response.meta['combs'].pop(0)
            form_data = {
                'action': 'add',
                response.meta['color_attr']: temp_color,
                response.meta['size_attr']: temp_size,
                'product_id': response.meta['itemid'],
                'qty[]': '1'
            }
            meta_data = {
                'combs': response.meta['combs'],
                'color_attr': response.meta['color_attr'],
                'size_attr': response.meta['size_attr'],
                'itemid': response.meta['itemid'],
                'color': color_name,
                'size': size_name,
                'color_names': response.meta['color_names'],
                'size_names': response.meta['size_names'],
                'color_ids': response.meta['color_ids'],
                'size_ids': response.meta['size_ids'],
                'main_object': response.meta['main_object']
            }
            yield scrapy.FormRequest(
                url = url_new,
                formdata = form_data,
                meta = meta_data,
                callback = self.each_type
            )
        else:
            yield response.meta['main_object']
