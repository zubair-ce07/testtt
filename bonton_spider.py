import json
import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, reset_cookies


class Mixin:
    retailer = 'bonton-us'
    market = 'US'
    allowed_domains = ['www.bonton.com', 's7d4.scene7.com']
    start_urls = ['https://www.bonton.com/']
    images_url_t = '{path}{color}_IMAGESET?req=set%2Cjson%2CUTF-8&handler=s7sdkJSONResponse'
    brand_list = []
    homeware_categories = ['home', 'bed-bath']
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

        if self.out_of_stock(response):
            return self.out_of_stock_garment(response, self.product_id(response))

        self.boilerplate_normal(garment, response)

        garment['industry'] = self.product_industry(garment)
        if not garment['industry']:
            garment['gender'] = self.product_gender(garment)

        garment['skus'] = self.skus(response)

        garment['image_urls'] = self.image_urls(response)
        garment['meta'] = {'requests_queue': self.image_requests(response), 'request_attempt': 1}

        return self.next_request_or_garment(garment, drop_meta=False)

    def parse_image_urls(self, response):
        garment = response.meta['garment']
        image_urls = []

        images_text = re.search(r'(\{"set":.*\})', response.text)
        raw_images = json.loads(images_text.groups()[0])
        images = raw_images['set']['item']

        if type(images) is dict:
            images = [images]

        for image in images:
            image = image.get('s')
            if image:
                image_url = re.sub('BonTon/', '', image['n'])
                image_urls.append(response.urljoin(image_url))

        if image_urls:
            if garment['meta'].pop('request_attempt', 0):
                garment['image_urls'] = image_urls
            else:
                garment['image_urls'].extend(image_urls)

        return self.next_request_or_garment(garment)

    def image_requests(self, response):
        image_requests = []
        image_path = response.css('#imagePath::attr(value)').extract()[0]

        colors = response.css('[data-swatchName=Color]::attr(data-scene7path)').extract()
        for color in colors:
            images_url = self.images_url_t.format(path=image_path, color=color)
            image_requests.append(Request(url=images_url, callback=self.parse_image_urls))

        if not colors:
            images_url = self.images_url_t.format(path=image_path, color=self.product_id(response) + '_' + 'nocolor')
            image_requests.append(Request(url=images_url, callback=self.parse_image_urls))

        return image_requests

    def out_of_stock(self, response):
        if not clean(response.css(self.price_css)):
            return True
        return False

    def product_id(self, response):
        return response.css('[itemprop="sku"]::text').extract()[0]

    def product_composite_id(self, response):
        return response.css('#compositeProductId::attr(value)').extract()[0]

    def product_name(self, response):
        name = response.css('title::text').extract()
        return re.sub('{}®*\s*'.format(self.product_brand(response)), '', name[0])

    def product_brand(self, response):
        return response.css('[itemprop="brand"]::text').extract()[0]

    def product_category(self, response):
        return clean(response.css('.categoryBreadcrumb ::text'))

    def raw_description(self, response):
        return clean(response.css('#summarycontent ::text'))

    def product_description(self, response):
        description = self.raw_description(response)
        return [rd for rd in description if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        description = self.raw_description(response)
        return [rd for rd in description if self.care_criteria_simplified(rd)]

    def image_urls(self, response):
        image_urls = []
        raw_skus = self.raw_skus(response)
        for raw_sku in raw_skus:
            image = raw_sku.get('ItemImage')
            if image and image not in image_urls:
                image_urls.append(image)
        return image_urls

    def skus(self, response):
        skus = {}
        colors = response.css('[data-attrName=Color]::attr(data-attrvalue)').extract()
        sizes = response.css('[data-attrName=Size]::attr(data-attrvalue)').extract() or [self.one_size]
        raw_skus = self.raw_skus(response)
        common = {'currency': 'USD'}

        for size in sizes:
            common['size'] = size
            size_id = self.sku_attribute_id(response, size)
            if colors:
                for color in colors:
                    sku = common.copy()
                    previous_price, price = self.sku_pricing(response, raw_skus, size_id, color)
                    sku['price'] = price
                    sku['colour'] = color

                    if previous_price:
                        sku['previous_prices'] = previous_price

                    if self.is_in_stock(response, raw_skus, size_id, color):
                        skus[color + '_' + str(size_id)] = sku
            else:
                sku = common.copy()
                previous_price, price = self.sku_pricing(response, raw_skus, size_id)
                sku['price'] = price

                if previous_price:
                    sku['previous_prices'] = previous_price

                if not size_id or all([size_id and self.is_in_stock(response, raw_skus, size_id)]):
                    skus[size] = sku

        return skus

    def sku_pricing(self, response, raw_skus, size_id, color=None):
        color_id = self.sku_attribute_id(response, color)
        for raw_sku in raw_skus:
            sku_size = raw_sku['Attributes'].get('Size_{}'.format(size_id))
            if sku_size:
                if color_id:
                    if raw_sku['Attributes'].get('Color_{}'.format(color_id)):
                        return self.sku_prices(raw_sku)
                else:
                    return self.sku_prices(raw_sku)

        return self.sku_prices(raw_skus[0])

    def sku_prices(self, raw_sku):
        previous_prices = list({raw_sku["minListPrice_USD"], raw_sku["maxListPrice_USD"]})
        current_price = raw_sku["maxPrice_USD"]
        return previous_prices if current_price not in previous_prices else [], current_price

    def sku_attribute_id(self, response, attribute):
        css = '[data-swatch-size="{}"]::attr(data-swatchvalueid)'.format(attribute)
        return response.css(css).extract_first()

    def raw_skus(self, response):
        css = '#entitledItem_{}::text'.format(self.product_composite_id(response))
        skus_text = response.css(css).extract()[0]
        return json.loads(skus_text)

    def is_in_stock(self, response, raw_skus, size_id, color=None):
        color_id = self.sku_attribute_id(response, color)
        for raw_sku in raw_skus:
            sku_size = raw_sku['Attributes'].get('Size_{}'.format(size_id))
            if sku_size:
                if color_id:
                    if raw_sku['Attributes'].get('Color_{}'.format(color_id)):
                        return True
                else:
                    return True

    def product_gender(self, garment):
        soup = ' '.join(garment['category'] + [garment['name'], garment['url_original']]).lower()

        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'

    def product_industry(self, garment):
        soup = ' '.join(garment['category'] + [garment['url_original']]).lower()

        for homeware in self.homeware_categories:
            if homeware in soup:
                return 'homeware'


class BenettonCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = BontonParseSpider()

    listing_css = [
        '.next-arrow',
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
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_r)),
        Rule(LinkExtractor(restrict_xpaths=products_x), callback='parse_item'),
    ]

    def parse_brands(self, response):
        brands = clean(response.css('.alpha-list a::text'))
        self.brand_list += sorted(brands, key=len, reverse=True)
        yield reset_cookies(Request(self.start_urls[0]))

    def start_requests(self):
        yield Request("http://www.bonton.com/sc1/brands/", callback=self.parse_brands)
