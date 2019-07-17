import json
import re

import scrapy
from scrapy.spiders import CrawlSpider


def clean(raw_data):
    if isinstance(raw_data, list):
        return [re.sub('\s+', ' ', data).strip() for data in raw_data
                if re.sub('\s+', ' ', data).strip()]
    elif isinstance(raw_data, str):
        return re.sub('\s+', ' ', raw_data).strip()


class WeItem(scrapy.Item):
    retailer_sku = scrapy.Field()
    gender = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    skus = scrapy.Field()


class Gap(CrawlSpider):
    name = 'gap'
    allowed_domains = ['gap.cn']
    api_url = 'https://www.gap.cn/gap/rest/category?'
    product_url = 'https://www.gap.cn/gap/rest/productnew?id='
    start_urls = [
        'https://www.gap.cn/gap/rest/category?action=getTopNavs&store_id=1'
    ]

    def parse(self, response):
        listings_json = json.loads(response.text)

        yield from [response.follow(f'{self.api_url}cid={listing_id.get("id")}',
                                    callback=self.parse_categories)
                    for listing_id in listings_json.get('data').get('marketTopNavs')]

    def parse_categories(self, response):
        categories_json = json.loads(response.text)

        yield from [response.follow(f'{self.api_url}id={category_code}',
                                    callback=self.parse_subcategory)
                    for category_code in
                    categories_json.get('data').get('currentProduct'
                                                    'List').get('currentChildCategoryIdAll').split(',')]

    def parse_subcategory(self, response):
        subcategories_json = json.loads(response.text)

        yield from [response.follow(f'{self.api_url}cid={subcategory_code}&store_id=1&from=side'
                                    f'&customer_group_id=0', callback=self.parse_products)
                    for subcategory_code in subcategories_json.get('data').get('child_categories')]

    def parse_products(self, response):
        products_json = json.loads(response.text)

        yield from [response.follow(f'{self.product_url}{product_code}&store_id=1&customer_group_id=0',
                                    callback=self.parse_item)
                    for product_code in products_json.get('data').get('currentProduct'
                                                                      'List').get('productIds')]

    def parse_item(self, response):
        raw_product = json.loads(response.text)

        item = WeItem()
        item['retailer_sku'] = self.retailer_sku(raw_product)
        item['gender'] = self.product_gender(raw_product)
        item['name'] = self.product_name(raw_product)
        item['category'] = self.product_category(raw_product)
        item['url'] = self.product_url(raw_product)
        item['brand'] = self.product_brand(raw_product)
        item['description'] = self.product_description(raw_product)
        item['care'] = self.product_care(raw_product)
        item['image_urls'] = self.images_url(raw_product)
        item['skus'] = self.parse_sku(raw_product)

        yield item

    def retailer_sku(self, raw_product):
        return raw_product.get('data').get('trackingcode').get('productId')

    def product_gender(self, raw_product):
        return raw_product.get('data').get('prefixCategoryName')

    def product_name(self, raw_product):
        return raw_product.get('data').get('productName')

    def product_category(self, raw_product):
        return raw_product.get('data').get('categoriesName')

    def product_url(self, raw_product):
        return raw_product.get('data').get('shareUrl')

    def product_brand(self, raw_product):
        return raw_product.get('data').get('trackingcode').get('dps360_brand')

    def product_description(self, raw_product):
        return raw_product.get('data').get('productDetail').get('productFiber')

    def product_care(self, raw_product):
        return raw_product.get('data').get('productDetail').get('productCare')

    def images_url(self, raw_product):
        return [image_list.get('productImageUrl')
                for image_list in raw_product.get('data').get('imageList')]

    def parse_sku(self, raw_product):
        sku = {}

        for color_json in raw_product.get('data').get('colors'):
            color = color_json.get("colorName")

            for size in color_json.get('size'):
                size = size.get("sizeNumber")
                sku.update({
                    f'{color}_{size}': {
                        'size': size,
                        'color': color,
                        'sale_price': color_json.get("salePrice"),
                        'price': color_json.get("price")
                    }
                })
        return sku

