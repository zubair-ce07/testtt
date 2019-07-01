# -*- coding: utf-8 -*-
import scrapy
import json
from newYorker.items import NewyorkerItem
from newYorker.image import NewyorkerItemsVariantsImage
from newYorker.variant import NewyorkerItemsVariant
from newYorker.size import NewyorkerItemsVariantsSize


class NewYorkerSpider(scrapy.Spider):
    name = 'new_yorker'
    allowed_domains = ['newyorker.de']
    start_urls = ['https://www.newyorker.de/pt/products']

    def parse(self, response):
        yield scrapy.Request(
            url='https://api.newyorker.de/csp/products/public/filters',
            callback=self.parse_categories)

    def parse_categories(self, response):
        filters = response.text.strip(
            'jQuery1124033955090772971586_1528569153921()')
        filters_json = json.loads(filters)
        for gender in filters_json.keys():
            yield scrapy.Request(
                url="https://api.newyorker.de/csp/products/public/query?"
                    "filters[country]=pt"
                    "&filters[gender]="+str(gender) +
                    " &filters[brand]="
                    "&filters[web_category]="
                    "&filters[collections]="
                    "&limit=24"
                    "&offset=0",
                meta={"gender": gender},
                callback=self.parse_categories_until_end)

    def parse_categories_until_end(self, response):
        categories = response.text.strip(
            'jQuery1124033955090772971586_1528569153921()')
        categories_json = json.loads(categories)
        for i in range(25, categories_json['totalCount'], 24):
            yield scrapy.Request(
                url="https://api.newyorker.de/csp/products/public/query?"
                    "filters[country]=pt"
                    "&filters[gender]=" + response.meta['gender'] +
                    " &filters[brand]="
                    "&filters[web_category]="
                    "&filters[collections]="
                    "&limit=24"
                    "&offset="+str(i),
                callback=self.parse_items)

    def parse_items(self, response):
        items = response.text.strip(
            'jQuery1124033955090772971586_1528569153921()')
        items_json = json.loads(items)
        for item in items_json['items']:
            yield scrapy.Request(
                url='https://api.newyorker.de/csp/products/public/product'
                    '/matchingProducts?country=de&id=' +
                    str(item['id'])+'&variantId=001&limit=3',
                callback=self.extract_product
            )

    def extract_product(self, response):
        variants = []
        product_types = []
        response = response.text.strip(
            'jQuery1124033955090772971586_1528569153921()')
        response = json.loads(response)
        for variant in response:
            variants.append(variant)
            product_types.append(NewyorkerItem(
                id=variant['id'],
                country=variant['country'],
                maintenance_group=variant['maintenance_group'],
                web_category_id=variant['web_category_id'],
                web_category=variant['web_category'],
                brand=variant['brand'],
                sales_unit=variant['sales_unit'],
                customer_group=variant['customer_group'],
                variants=variants))
        return product_types

    def calculate_product_variant(self, product_variant):
        sizes = []
        images = []
        for size in product_variant['sizes']:
            sizes.append(self.extract_product_size_data(size))
        for image in product_variant['images']:
            images.append(self.extract_product_image_data(image))
        return NewyorkerItemsVariant(
            basic_color=product_variant['basic_color'],
            blue=product_variant['blue'],
            color_group=product_variant['color_group'],
            coming_soon=product_variant['coming_soon'],
            currency=product_variant['currency'],
            current_price=product_variant['current_price'],
            green=product_variant['green'],
            id=product_variant['id'],
            color_name=product_variant['color_name'],
            images=images,
            new_in=product_variant['new_in'],
            original_price=product_variant['original_price'],
            pantone_color=product_variant['pantone_color'],
            pantone_color_name=product_variant['pantone_color_name'],
            product_id=product_variant['product_id'],
            publish_date=product_variant['publish_date'],
            red=product_variant['red'],
            red_price_change=product_variant['red_price_change'],
            sale=product_variant['sale'],
            sizes=sizes)

    def extract_product_image_data(self, product_image):
        return NewyorkerItemsVariantsImage(
                key=product_image['key'],
                type=product_image['type'],
                angle=product_image['angle'],
                has_thumbnail=product_image['has_thumbnail'],
                position=product_image['position'])

    def extract_product_size_data(self, product_size):
        return NewyorkerItemsVariantsSize(
                size_value=product_size['size_value'],
                size_name=product_size['size_name'],
                bar_code=product_size['bar_code'])
