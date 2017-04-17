import json
import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean, reset_cookies


class Mixin:
    retailer = 'bonton-us'
    market = 'US'
    allowed_domains = ['www.bonton.com', 's7d4.scene7.com']
    start_urls = ['https://www.bonton.com/']
    images_url_t = add_or_replace_parameter('{path}{color}_IMAGESET', 'req', 'set,json,UTF-8')
    images_url_t = add_or_replace_parameter(images_url_t, 'handler', 's7sdkJSONResponse')
    brand_list = []
    gender_map = [
        ('women', 'women'),
        ('men', 'men'),
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('kid', 'unisex-children'),
        ('handbags & accessories', 'women'),
        ('juniors', 'women')
    ]


class BontonParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.product_pageDesign_pageGroup .btnSalePrice,.product_pageDesign_pageGroup .price'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        if self.out_of_stock(self.price_css, response):
            return self.out_of_stock_garment(response, self.product_id(response))

        self.boilerplate(garment, response)

        garment['brand'] = self.product_brand(response)
        garment['name'] = self.product_name(response, garment['brand'])
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)
        garment['image_urls'] = self.image_urls(response)
        garment['category'] = self.product_category(response)
        garment['industry'] = self.product_industry(garment)

        if not garment['industry']:
            garment['gender'] = self.product_gender(garment)

        garment['skus'] = self.skus(response)

        garment['meta'] = {'requests_queue': self.image_requests(response), 'request_attempt': 1}
        return self.next_request_or_garment(garment, drop_meta=False)

    def out_of_stock(self, hxs, response):
        if not clean(response.css(hxs).extract()):
            return True
        return False

    def product_id(self, response):
        return response.css('[itemprop="sku"]::text').extract_first()

    def product_composite_id(self, response):
        return response.css('#compositeProductId::attr(value)').extract_first()

    def product_name(self, response, brand):
        sel = response.css('title::text')
        name = sel.re('{}®*\s*(.*)'.format(brand)) or sel.extract()
        return name[0]

    def product_brand(self, response):
        return response.css('[itemprop="brand"]::text').extract_first()

    def product_category(self, response):
        return clean(response.css('.categoryBreadcrumb ::text').extract())

    def product_description(self, response):
        description = clean(response.css('#summarycontent ::text').extract())
        return [rd for rd in description if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        description = clean(response.css('#summarycontent ::text').extract())
        return [rd for rd in description if self.care_criteria_simplified(rd)]

    def image_urls(self, response):
        image_urls = []
        raw_skus = self.raw_skus(response)
        for raw_sku in raw_skus:
            image = raw_sku.get('ItemImage', None)
            if image and image not in image_urls:
                image_urls.append(image)
        return image_urls

    def image_requests(self, response):
        image_requests = []
        image_path = response.css('#imagePath::attr(value)').extract_first()

        colors = response.css('[data-swatchName=Color]::attr(data-scene7path)').extract()
        for color in colors:
            images_url = self.images_url_t.format(path=image_path, color=color)
            image_requests.append(Request(url=images_url, callback=self.parse_image_urls))

        if not colors:
            images_url = self.images_url_t.format(path=image_path, color=self.product_id(response)+'_'+'nocolor')
            image_requests.append(Request(url=images_url, callback=self.parse_image_urls))

        return image_requests

    def parse_image_urls(self, response):
        garment = response.meta['garment']
        image_urls = []

        images_text = re.search(r'(\{"set":.*\})', response.text)
        raw_images = json.loads(images_text.groups()[0])
        images = raw_images['set']['item']

        if type(images) is dict:
            images = [images]

        for image in images:
            image = image.get('s', None)
            if image:
                image_url = re.sub('BonTon/', '', image['n'])
                image_urls.append(response.urljoin(image_url))

        if image_urls:
            if garment['meta'].get('request_attempt', 0) == 1:
                garment['meta']['request_attempt'] = 0
                garment['image_urls'] = image_urls
            else:
                garment.get('image_urls', []).extend(image_urls)

        return self.next_request_or_garment(garment, drop_meta=False)

    def skus(self, response):
        skus = {}
        previous_price, price, currency = self.product_pricing_new(response)
        colors = response.css('[data-attrName=Color]::attr(data-attrvalue)').extract()
        sizes = response.css('[data-attrName=Size]::attr(data-attrvalue)').extract() or [self.one_size]
        raw_skus = self.raw_skus(response)

        for size in sizes:
            common = {
                'price': price,
                'currency': currency,
                'size': size
            }

            if previous_price:
                common['previous_prices'] = previous_price

            size_id = self.sku_attribute_id(response, size)
            if colors:
                for color in colors:
                    sku = common.copy()
                    sku['colour'] = color
                    if not self.is_in_stock(response, raw_skus, size_id, color):
                        sku['out_of_stock'] = True

                    skus[color + '_' + str(size_id)] = sku
            else:
                sku = common.copy()
                if size_id and not self.is_in_stock(response, raw_skus, size_id):
                    sku['out_of_stock'] = True

                skus[size] = sku

        return skus

    def sku_attribute_id(self, response, attribute):
        css = '[data-swatch-size="{}"]::attr(data-swatchvalueid)'.format(attribute)
        return response.css(css).extract_first()

    def raw_skus(self, response):
        css = '#entitledItem_{}::text'.format(self.product_composite_id(response))
        skus_text = response.css(css).extract_first()
        return json.loads(skus_text)

    def is_in_stock(self, response, raw_skus, size_id, color=None):
        color_id = self.sku_attribute_id(response, color)
        for raw_sku in raw_skus:
            size_available = raw_sku['Attributes'].get('Size_{}'.format(size_id), None)
            color_available = raw_sku['Attributes'].get('Color_{}'.format(color_id), None)
            if all([size_available and color_id and color_available]) \
                    or all([not color_id and size_available]):
                return True

        return False

    def product_gender(self, garment):
        soup = ' '.join(garment['category'] + [garment['name']] + [garment['url_original']]).lower()

        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'

    def product_industry(self, garment):
        soup = ' '.join(garment['category'] + [garment['url_original']]).lower()

        for homeware in ['home', 'bed-bath']:
            if homeware in soup:
                return 'homeware'


class BenettonCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = BontonParseSpider()

    listing_css = [
        '.catalog-links',
        '#facetsWrapper',

    ]
    products_x = [
        '//a[contains(@class,"productLink")]',
    ]
    deny_r = [
        'shoe-care-accessories',
        'jewelry-boxes',
        'baby-baby-gear',
        'baby-baby-gifts-essentials',
        'baby-nursery-furniture-accessories',
        'baby-kids/toys-games-toys',
        'toys-games-playroom-storage-accessories',
    ]
    rules = [
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_r), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_xpaths=products_x), callback='parse_item'),
    ]

    def parse_pagination(self, response):
        for req in self.parse(response):
            yield req

        return self.get_pagination_request(response)

    def get_pagination_request(self, response):
        next_page_url = response.css('.paginationLinks a::attr(href)').extract_first()
        if next_page_url:
            return Request(url=response.urljoin(next_page_url), callback=self.parse_pagination)

    def parse_brands(self, response):
        brands = clean(response.css('.alpha-list a::text'))
        self.brand_list += sorted(brands, key=len, reverse=True)
        yield reset_cookies(Request(self.start_urls[0]))

    def start_requests(self):
        yield Request("http://www.bonton.com/sc1/brands/", callback=self.parse_brands)
