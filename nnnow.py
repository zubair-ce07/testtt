from scrapy import Spider, Request, Field, Item
from scrapy.loader import ItemLoader
import json
from urllib.parse import urljoin
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class NnnowSpider(Spider):
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
    product_listing = '.nw-productlist'

    rules = (
        Rule(LinkExtractor(restrict_css=product_listing), callback='parse_product_listing')
    )

    def parse(self, response):
        meta = {'dont_merge_cookies': True}
        required_info = response.css('script').re_first('DATA=(.+)</script>')
        raw_data = json.loads(required_info)
        raw_urls = raw_data['NavListStore']['navListData']['data']['menu']['level1']
        for main_nav_links in raw_urls:
            for sub_nav_links in main_nav_links['level2']:
                for sub_nav_link in sub_nav_links['level3']:
                    yield response.follow(sub_nav_link['url'],
                                          callback=self.parse_product_listing,
                                          meta=meta)

    def get_total_page_status(self, response):
        find_json = response.css('script').re_first('DATA=(.+)</script>')
        raw_product = json.loads(find_json)
        if raw_product['ProductStore']['ProductData']:
            return raw_product['ProductStore']['ProductData']['totalPages']
        return False

    def parse_product_listing(self, response):
        get_page_numbers = self.get_total_page_status(response)
        if get_page_numbers:
            request_url = 'https://api.nnnow.com/d/apiV2/listing/products'
            category_name = response.url.split('/')[3]
            category_id = 'tn_{}'.format(category_name.replace('-', '_'))
            for page in range(int(get_page_numbers)):
                params = {
                    "deeplinkurl": f"/{category_name}?p={page}&cid={category_id}"
                }
                yield Request(request_url, method='POST', body=json.dumps(params),
                              callback=self.parse_pagination, headers=self.headers,
                              meta=response.meta)

    def parse_pagination(self, response):
        raw_products = json.loads(response.text)
        for raw_product in raw_products['data']['styles']['styleList']:
            url = urljoin(self.base_url, raw_product['url'])
            yield Request(url,
                          callback=self.parse_product,
                          meta=response.meta)

    def get_name(self, response):
        return response.css('.nw-product-name .nw-product-title::text').get()

    def get_brand(self, response):
        return response.css('.nw-product-name .nw-product-brandtxt::text') \
            .get()

    def get_categories(self, response):
        return response.css('.nw-breadcrumblist-list .nw-breadcrumb-listitem::text') \
            .getall()

    def get_image_urls(self, response):
        return response.css('.nw-maincarousel-wrapper img::attr(src)').getall()

    def get_currency(self, response):
        return response.css('.nw-sizeblock-container  span::attr(content)').get()

    def get_url(self, response):
        return response.css("meta[name='og_url']::attr(content)").get()

    def get_description(self, raw_product):
        return raw_product['finerDetails']['specs']['list']

    def get_retailer_sku(self, raw_product):
        return raw_product['styleId']

    def get_gender(self, raw_product):
        return raw_product['gender']

    def get_skus(self, raw_product, color, currency):
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
        currency = 'INR'
        color = response.css('.nw-color-name::text').get()
        loader = ProductItemLoader(selector=response)
        loader.add_value('name', self.get_name(response))
        loader.add_value('category', self.get_categories(response))
        loader.add_value('description', self.get_description(parse_raw_product))
        loader.add_value('image_urls', self.get_image_urls(response))
        loader.add_value('brand', self.get_brand(response))
        loader.add_value('retailer_sku', self.get_retailer_sku(parse_raw_product))
        loader.add_value('url', response.url)
        loader.add_value('skus', self.get_skus(parse_raw_product, color, currency))
        loader.add_value('gender', self.get_gender(parse_raw_product))
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
    name_out = TakeFirst()
    category_out = Identity()
    description_out = Identity()
    brand_out = TakeFirst()
    image_urls_out = Identity()
    retailer_sku_out = TakeFirst()
    url_out = TakeFirst()
    skus_out = Identity()
    gender_out = TakeFirst()
