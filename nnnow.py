from scrapy import Request, Field, Item
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import json
from urllib.parse import urljoin
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.spiders import Rule, CrawlSpider


class NnnowSpider(CrawlSpider):
    name = 'nnnow'
    start_urls = [
        'https://www.nnnow.com/',
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }
    headers = {
            'Content-Type': "application/json",
            'module': "odin",
    }
    base_url = 'https://www.nnnow.com'

    rules = (
        Rule(LinkExtractor(restrict_css='.nw-leftnavmobile-list a',
             deny=('/offers', )), callback='parse_product_listing'),
    )

    def get_total_pages(self, response):
        find_json = response.css('script').re_first('DATA=(.+)</script>')
        raw_product = json.loads(find_json)
        if raw_product['ProductStore']['ProductData']:
            return raw_product['ProductStore']['ProductData']['totalPages']
        return False

    def parse_product_listing(self, response):
        get_page_numbers = self.get_total_pages(response)
        if get_page_numbers:
            request_url = 'https://api.nnnow.com/d/apiV2/listing/products'
            category_name = response.url.split('/')[3]
            category_id = 'tn_{}'.format(category_name.replace('-', '_'))
            for page in range(int(get_page_numbers)):
                params = {
                    "deeplinkurl": f"/{category_name}?p={page}&cid={category_id}"
                }
                yield Request(request_url, method='POST',
                              body=json.dumps(params),
                              callback=self.parse_pagination,
                              headers=self.headers,
                              meta=response.meta)

    def parse_pagination(self, response):
        raw_products = json.loads(response.text)
        for raw_product in raw_products['data']['styles']['styleList']:
            url = urljoin(self.base_url, raw_product['url'])
            yield Request(url,
                          callback=self.parse_product,
                          meta=response.meta)

    def get_skus(self, raw_product, response):
        currency = 'INR'
        color = response.css('.nw-color-name::text').get()
        skus = []
        for sku in raw_product['skus']:
            skus.append(
                        {'sku_id': sku['skuId'],
                         'color': color,
                         'currency': currency,
                         'size': sku['size'],
                         'out_of_stock': not sku['inStock'],
                         'price': int(sku['mrp']),
                         'previous_price': [int(sku['price'])]}
            )
        return skus

    def parse_product(self, response):
        required_info = response.css('script').re_first('DATA=(.+)</script>')
        raw_product = json.loads(required_info)
        parse_raw_product = raw_product['ProductStore']['PdpData']['mainStyle']
        raw_description = parse_raw_product['finerDetails']['specs']['list']
        raw_gender = parse_raw_product['gender']
        raw_retailer_sku = parse_raw_product['styleId']
        loader = ProductItemLoader(item=ProductFields(), response=response)
        loader.add_css('name', '.nw-product-name .nw-product-title::text')
        loader.add_css('category',
                       '.nw-breadcrumblist-list .nw-breadcrumb-listitem::text')
        loader.add_value('description', raw_description)
        loader.add_css('image_urls', '.nw-maincarousel-wrapper img::attr(src)')
        loader.add_css('brand', '.nw-product-name .nw-product-brandtxt::text')
        loader.add_value('retailer_sku', raw_retailer_sku)
        loader.add_value('url', response.url)
        loader.add_value('skus', self.get_skus(parse_raw_product, response))
        loader.add_value('gender', raw_gender)
        return loader.load_item()


class ProductFields(Item):
    name = Field()
    category = Field()
    description = Field()
    brand = Field()
    image_urls = Field()
    retailer_sku = Field()
    url = Field()
    skus = Field()
    gender = Field()


class ProductItemLoader(ItemLoader):
    default_item_class = ProductFields
    default_output_processor = TakeFirst()
    category_out = Identity()
    description_out = Identity()
    image_urls_out = Identity()
    skus_out = Identity()
