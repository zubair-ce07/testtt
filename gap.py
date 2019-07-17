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


class GapItem(scrapy.Item):
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


class GapSpider(CrawlSpider):
    name = 'gap'
    allowed_domains = ['gap.cn']
    start_urls = [
        'https://www.gap.cn/gap/rest/category?cid=2300',
        'https://www.gap.cn/gap/rest/category?cid=4',
        'https://www.gap.cn/gap/rest/category?cid=3',
        'https://www.gap.cn/gap/rest/category?cid=6',
        'https://www.gap.cn/gap/rest/category?cid=5',
        'https://www.gap.cn/gap/rest/category?cid=33748',
        'https://www.gap.cn/gap/rest/category?cid=33758',
        'https://www.gap.cn/gap/rest/category?cid=7564',
        'https://www.gap.cn/gap/rest/category?cid=44030',
    ]

    def parse(self, response):
        category_url = 'https://www.gap.cn/gap/rest/category?id='
        yield from [response.follow(f'{category_url}{category_code}',
                                    callback=self.parse_subcategory)
                    for category_code in re.findall('entity_id\":\"(.+?)\"', response.text)]

    def parse_subcategory(self, response):
        subcategory_url = 'https://www.gap.cn/gap/rest/category?cid='
        yield from [response.follow(f'{subcategory_url}{subcategory_code}&store_id=1&from=side'
                                    f'&customer_group_id=0', callback=self.parse_products)
                    for subcategory_code in re.findall('entity_id\":\"(.+?)\"', response.text)]

    def parse_products(self, response):
        product_url = 'https://www.gap.cn/gap/rest/productnew?id='
        yield from [response.follow(f'{product_url}{product_code}&store_id=1&customer_group_id=0',
                                    callback=self.parse_item)
                    for product_code in re.findall('productId\":(.+?),', response.text)]

    def parse_item(self, response):
        raw_json = json.loads(response.text)

        item = GapItem()
        item['retailer_sku'] = self.retailer_sku(raw_json)
        item['gender'] = self.product_gender(raw_json)
        item['name'] = self.product_name(raw_json)
        item['category'] = self.product_category(raw_json)
        item['url'] = self.product_url(raw_json)
        item['brand'] = self.product_brand(raw_json)
        item['description'] = self.product_description(raw_json)
        item['care'] = self.product_care(raw_json)
        item['image_urls'] = self.images_url(raw_json)
        item['skus'] = self.parse_sku(raw_json)

        yield item

    def retailer_sku(self, raw_json):
        return raw_json.get('data').get('trackingcode').get('productId')

    def product_gender(self, raw_json):
        return raw_json.get('data').get('prefixCategoryName')

    def product_name(self, raw_json):
        return raw_json.get('data').get('productName')

    def product_category(self, raw_json):
        return raw_json.get('data').get('categoriesName')

    def product_url(self, raw_json):
        return raw_json.get('data').get('shareUrl')

    def product_brand(self, raw_json):
        return raw_json.get('data').get('trackingcode').get('dps360_brand')

    def product_description(self, raw_json):
        return raw_json.get('data').get('productDetail').get('productFiber')

    def product_care(self, raw_json):
        return raw_json.get('data').get('productDetail').get('productCare')

    def images_url(self, raw_json):
        return [image_list.get('productImageUrl')
                for image_list in raw_json.get('data').get('imageList')]

    def parse_sku(self, raw_json):
        sku = {}

        for color_json in raw_json.get('data').get('colors'):
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

