import json
from urllib.parse import urljoin

from scrapy import Request, Field, Item
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.spiders import Rule, CrawlSpider


class Product(Item):
    name = Field()
    category = Field()
    description = Field()
    brand = Field()
    image_urls = Field()
    retailer_sku = Field()
    url = Field()
    skus = Field()
    gender = Field()


class Sku(Item):
    sku_id = Field()
    color = Field()
    currency = Field()
    size = Field()
    out_of_stock = Field()
    price = Field()
    previous_price = Field()


class SkuItemLoader(ItemLoader):
    default_item_class = Sku
    default_output_processor = TakeFirst()
    previous_price_out = Identity()


class ProductItemLoader(ItemLoader):
    default_item_class = Product
    default_output_processor = TakeFirst()
    category_out = Identity()
    description_out = Identity()
    image_urls_out = Identity()
    skus_out = Identity()


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
             deny=('/offers')), callback='parse_product_listing'),
    )

    def get_pages_count(self, response):
        raw_product = json.loads(response.css
                                 ('script').re_first('DATA=(.+)</script>'))
        parse_raw_product = raw_product['ProductStore']['ProductData']
        return 1 if not parse_raw_product else parse_raw_product['totalPages']

    def parse_product_listing(self, response):
        get_page_numbers = self.get_pages_count(response)
        if get_page_numbers:
            request_url = 'https://api.nnnow.com/d/apiV2/listing/products'
            category_name = response.url.split('/')[3]
            category_id = 'tn_{}'.format(category_name.replace('-', '_'))
            for page in range(get_page_numbers):
                params = {
                    "deeplinkurl": f"/{category_name}?p={page}&cid={category_id}"
                }
                yield Request(request_url, method='POST',
                              body=json.dumps(params),
                              callback=self.parse_listing,
                              headers=self.headers)

    def parse_listing(self, response):
        raw_product = json.loads(response.text)
        for raw_product in raw_product['data']['styles']['styleList']:
            url = urljoin(self.base_url, raw_product['url'])
            yield Request(url,
                          callback=self.parse_product)

    def get_skus(self, raw_product, response):
        skus = []
        for sku in raw_product['skus']:
            loader = SkuItemLoader(item=Sku(), selector=sku)
            loader.add_value('sku_id', sku['skuId']),
            loader.add_value('currency', 'INR'),
            loader.add_value('size', sku['size']),
            loader.add_value('out_of_stock', not sku['inStock']),
            loader.add_value('price', sku['price']),
            loader.add_value('previous_price', sku['price'])
            skus.append(loader.load_item())
        return skus

    def parse_product(self, response):
        raw_product = json.loads(response.css('script')
                                 .re_first('DATA=(.+)</script>'))
        parse_raw_product = raw_product['ProductStore']['PdpData']['mainStyle']
        loader = ProductItemLoader(item=Product(), response=response)
        loader.add_css('name', '.nw-product-name .nw-product-title::text')
        loader.add_css('category',
                       '.nw-breadcrumblist-list .nw-breadcrumb-listitem::text')
        loader.add_value('description',
                         parse_raw_product['finerDetails']['specs']['list'])
        loader.add_css('image_urls', '.nw-maincarousel-wrapper img::attr(src)')
        loader.add_css('brand', '.nw-product-name .nw-product-brandtxt::text')
        loader.add_value('retailer_sku', parse_raw_product['styleId'])
        loader.add_value('url', response.url),
        loader.add_value('skus', self.get_skus(parse_raw_product, response)),
        loader.add_value('gender', parse_raw_product['gender'])
        return loader.load_item()
