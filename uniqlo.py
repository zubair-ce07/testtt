import json
import re

import lxml
import scrapy
from scrapy.spiders import CrawlSpider


def clean(raw_data):
    if isinstance(raw_data, list):
        return [re.sub('\s+', ' ', data).strip() for data in raw_data
                if re.sub('\s+', ' ', data).strip()]
    elif isinstance(raw_data, str):
        return re.sub('\s+', ' ', raw_data).strip()


class UniqloItem(scrapy.Item):
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


class UniqloSpider(CrawlSpider):
    name = 'uniqlo'
    listings_url = 'https://www.uniqlo.cn/public/image/L1/2019/common/files'
    products_url = 'https://www.uniqlo.cn/data/products/spu/zh_CN/'
    allowed_domains = ['uniqlo.cn']

    start_urls = [
        'https://www.uniqlo.cn/'
    ]

    def parse(self, response):
        yield from [response.follow(f'{self.listings_url}{listing_name}',
                                    callback=self.parse_categories,
                                    meta={'catg': [listing_name.split('-')[1][:-5]]})
                    for listing_name in re.findall('files(.+?)\"', response.text)]

    def parse_categories(self, response):

        for catg_url, catg_name in zip(response.css('a ::attr(href)').getall(),
                                       response.css('a ::text').getall()):
            acc_catg = response.meta['catg'].copy()
            acc_catg.append(catg_name)
            yield response.follow(catg_url, callback=self.parse_products, meta={'catg': acc_catg})

    def parse_products(self, response):
        raw_json = re.findall('\"data-components\" hidden>(.+?)</text', response.text)
        products_json = json.loads(raw_json[0])

        for section in products_json.get('components'):
            for product in products_json.get('components', {}).get(section, {}).get('props', {}). \
                    get('items', {}):
                yield response.follow(f'{self.products_url}{product.get("productCode")}.json',
                                      callback=self.parse_item,
                                      meta={'catg': response.meta["catg"]})

    def parse_item(self, response):
        raw_product = json.loads(response.text)

        item = UniqloItem()
        item['retailer_sku'] = self.retailer_sku(raw_product)
        item['gender'] = self.product_gender(raw_product)
        item['name'] = self.product_name(raw_product)
        item['category'] = response.meta["catg"]
        item['url'] = self.product_url(response)
        item['brand'] = self.product_brand(raw_product)
        item['description'] = self.product_description(raw_product)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.images_url(raw_product)
        item['skus'] = self.parse_sku(raw_product)

        yield item

    def retailer_sku(self, raw_product):
        return raw_product.get('summary').get('productCode')

    def product_gender(self, raw_product):
        return raw_product.get('summary').get('sex')

    def product_name(self, raw_product):
        return raw_product.get('summary').get('fullName')

    def product_url(self, response):
        return response.url

    def product_brand(self, raw_product):
        return 'Uniqlo'

    def product_description(self, raw_product):
        raw_descp = raw_product.get('desc').get('instruction')
        return lxml.html.fromstring(raw_descp).text_content()

    def product_care(self, response):
        return re.findall('【洗涤信息】(.+?)<', response.text)

    def images_url(self, raw_product):
        raw_html = raw_product.get('desc').get('description')
        return re.findall('<img src=\'(.+?)\'', raw_html)

    def parse_sku(self, raw_product):
        sku = {}
        price = raw_product.get('summary').get('originPrice')
        for product_sku in raw_product.get('rows'):
            sku.update({
                f'{product_sku.get("style")}_{product_sku.get("size")}':
                    {
                        'size': product_sku.get("size"),
                        'color': product_sku.get("style"),
                        'price': price
                    }
            })
        return sku

