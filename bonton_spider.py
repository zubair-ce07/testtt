import json
import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter
from w3lib.url import url_query_cleaner

from .base import BaseParseSpider, BaseCrawlSpider, clean, reset_cookies


class Mixin:
    retailer = 'bonton-us'
    market = 'US'
    allowed_domains = ['www.bonton.com', 's7d4.scene7.com']
    start_urls = ['https://www.bonton.com/']
    images_url_t = '{path}{color}_IMAGESET?req=set%2Cjson%2CUTF-8&handler=s7sdkJSONResponse'
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
            return self.out_of_stock_item(response, response, self.product_id(response))

        self.boilerplate_normal(garment, response)

        garment['industry'] = self.product_industry(garment)
        if not garment['industry']:
            garment['gender'] = self.product_gender(garment)

        garment['skus'] = self.skus(response)

        garment['image_urls'] = self.image_urls(response)
        garment['meta'] = {'requests_queue': self.image_requests(response)}
        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']
        image_urls = garment.get('image_urls', [])
        raw_images = self.raw_images(response)

        for image in raw_images:
            height = image['dy']
            width = image['dx']
            image = image.get('s')
            if image:
                image_url = self.image_url(response, image['n'])
                self.remove_duplicate_image_url(image_url, image_urls)
                image_urls.append(self.add_image_params(image_url, height, width))

        garment['image_urls'] = image_urls

        return self.next_request_or_garment(garment)

    def image_url(self, response, image):
        image_url = response.urljoin(image)
        return re.sub('BonTon/', '', image_url, 1)

    def add_image_params(self, image_url, height, width):
        image_url = add_or_replace_parameter(image_url, 'wid', width)
        return add_or_replace_parameter(image_url, 'hei', height)

    def remove_duplicate_image_url(self, image_url, image_urls):
        if image_url in image_urls:
            image_urls.remove(image_url)

        colorless_image_url = re.sub('_nocolor', '', image_url, 1)
        if colorless_image_url in image_urls:
            image_urls.remove(colorless_image_url)

    def raw_images(self, response):
        images_text = re.search(r'(\{"set":.*\})', response.text)
        raw_images = json.loads(images_text.groups()[0])
        images = raw_images['set']['item']

        if type(images) is dict:
            images = [images]

        return images

    def image_requests(self, response):
        image_requests = []
        image_path = response.css('#imagePath::attr(value)').extract()[0]

        colors = response.css('[data-swatchName=Color]::attr(data-scene7path)').extract()
        for color in colors:
            image_requests.append(self.image_request(image_path, color))

        if not colors:
            color = self.product_id(response) + '_' + 'nocolor'
            image_requests.append(self.image_request(image_path, color))

        return image_requests

    def image_request(self, image_path,  color):
        images_url = self.images_url_t.format(path=image_path, color=color)
        return Request(url=images_url, callback=self.parse_images)

    def out_of_stock(self, response):
        return not clean(response.css(self.price_css))

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
        return [d for d in description if not self.care_criteria_simplified(d)]

    def product_care(self, response):
        description = self.raw_description(response)
        return [c for c in description if self.care_criteria_simplified(c)]

    def image_urls(self, response):
        image_urls = []
        raw_skus = self.raw_skus(response)
        for raw_sku in raw_skus:
            image = url_query_cleaner(raw_sku.get('ItemImage'))
            if image and image not in image_urls:
                image_urls.append(image)
        return image_urls

    def skus(self, response):
        skus = {}
        colors = response.css('[data-attrName=Color]::attr(data-attrvalue)').extract()
        sizes = response.css('[data-attrName=Size]::attr(data-attrvalue)').extract() or [self.one_size]
        raw_skus = self.raw_skus(response)
        common = {'currency': 'USD'}

        if not colors:
            colors = [None]

        for size in sizes:
            common['size'] = size
            size_id = self.sku_attribute_id(response, size)
            for color in colors:
                sku = common.copy()
                sku_id = size
                sku_pricing = self.sku_pricing(response, raw_skus, size_id, color)
                if not sku_pricing:
                    continue

                previous_price, price = sku_pricing
                sku['price'] = price
                if previous_price:
                    sku['previous_prices'] = previous_price

                if color:
                    sku_id = color + '_' + str(size_id)
                    sku['colour'] = color

                skus[sku_id] = sku

        return skus

    def sku_pricing(self, response, raw_skus, size_id, color=None):
        color_id = self.sku_attribute_id(response, color)

        if not size_id:
            return self.sku_prices(raw_skus[0])

        for raw_sku in raw_skus:
            sku_size = raw_sku['Attributes'].get('Size_{}'.format(size_id))
            if sku_size:
                if color_id and not raw_sku['Attributes'].get('Color_{}'.format(color_id)):
                    continue
                return self.sku_prices(raw_sku)

    def sku_prices(self, raw_sku):
        previous_prices = list({int(float(raw_sku["minListPrice_USD"])), int(float(raw_sku["maxListPrice_USD"]))})
        current_price = int(float(raw_sku["maxPrice_USD"]))
        return previous_prices if current_price not in previous_prices else [], current_price

    def sku_attribute_id(self, response, attribute):
        css = '[data-swatch-size="{}"]::attr(data-swatchvalueid)'.format(attribute)
        return response.css(css).extract_first()

    def raw_skus(self, response):
        css = '#entitledItem_{}::text'.format(self.product_composite_id(response))
        skus_text = response.css(css).extract()[0]
        return json.loads(skus_text)

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
        'toys-games-toys',
        'toys-games-playroom-storage-accessories',
    ]
    rules = [
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_r)),
        Rule(LinkExtractor(restrict_xpaths=products_x), callback='parse_item'),
    ]

    def parse_brands(self, response):
        brands = clean(response.css('.alpha-list a::text'))
        yield {'brands': sorted(brands, key=len, reverse=True)}
        yield reset_cookies(Request(self.start_urls[0]))

    def start_requests(self):
        yield Request("http://www.bonton.com/sc1/brands/", callback=self.parse_brands)
