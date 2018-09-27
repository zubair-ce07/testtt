import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from scrapy.spiders import Request, Rule
from w3lib.url import add_or_replace_parameter, url_query_parameter, url_query_cleaner

from .base import BaseParseSpider, BaseCrawlSpider, clean, Gender


class Mixin:
    market = 'US'
    retailer = 'loftoutlet-us'
    default_brand = 'Loft'
    gender = Gender.WOMEN.value
    outlet = True

    allowed_domains = ['outlet.loft.com', 's7d2.scene7.com']
    start_urls = ['https://outlet.loft.com']

    image_url_t = 'https://s7d2.scene7.com/is/image/{}'
    image_req_url_t = 'https://s7d2.scene7.com/is/image/LOS/{}_{}_IS?req=set,json'


class LoftOutletParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        raw_product = self.raw_product(response)
        pid = self.product_id(raw_product)
        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = self.product_name(raw_product)
        garment['brand'] = self.product_brand(response)
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['category'] = self.product_category(response)
        garment['merch_info'] = self.merch_info(raw_product)
        garment['image_urls'] = self.image_urls(raw_product)

        if self.is_out_of_stock(response):
            garment['out_of_stock'] = True
            garment.update(self.pricing(response, raw_product[0]))
            return garment

        garment['skus'] = self.skus(response, raw_product)
        garment['meta'] = {'requests_queue': self.image_requests(raw_product)}

        return self.next_request_or_garment(garment)

    def skus(self, response, raw_product):
        skus = {}

        for raw_sku in raw_product:
            common_sku = self.pricing(response, raw_sku)

            for colour in raw_sku['skucolors']['colors']:
                common_sku['colour'] = colour['colorName']

                for size in colour['skusizes']['sizes']:
                    sku = common_sku.copy()
                    sku['size'] = size['sizeAbbr']

                    if size['available'] != 'true':
                        sku['out_of_stock'] = True

                    sku_id = size['skuId']
                    skus[sku_id] = sku

        return skus

    def image_requests(self, raw_product):
        pid = self.product_id(raw_product)
        colours = [colour['colorCode'] for variant in raw_product for colour in variant['skucolors']['colors']]
        return [Request(url=self.image_req_url_t.format(pid, c), callback=self.parse_images) for c in colours]

    def parse_images(self, response):
        garment = response.meta['garment']
        raw_images = re.search('"item":(.*)}}', response.text).group(1)
        images = json.loads(raw_images)

        if not isinstance(images, list):
            images = [images]

        garment['image_urls'] += [self.image_url_t.format(im['i']['n']) for im in images]

        return self.next_request_or_garment(garment)

    def product_id(self, raw_product):
        return raw_product[0]['prodId']

    def raw_product(self, response):
        product_css = 'script:contains(__NEXT_DATA__)::text'
        raw_product = clean(response.css(product_css).re('"products":(\[{.+}\]),"ship'))[0]
        return json.loads(raw_product)

    def raw_description(self, raw_product):
        raw_product = raw_product[0]
        raw_description = raw_product['fabricationContent'].split(',') + [raw_product['garmentCare']]
        raw_description += [v for k, v in raw_product.items() if 'bulletPoint' in k]

        return clean(raw_description)

    def product_name(self, raw_product):
        return clean(raw_product[0]['displayName'])

    def product_category(self, response):
        return clean(response.css('div[data-slnm-id="breadcrumb"] ::text'))[1:-1]

    def merch_info(self, raw_product):
        return clean([promo for promo in raw_product[0]['promoMessages'] if '$' not in promo])

    def clean_money(self, money_strs):
        return [ms for ms in money_strs if 'free' not in ms.lower()]

    def currency(self, response):
        currency_css = 'script:contains(__NEXT_DATA__)::text'
        return clean(response.css(currency_css).re('"currency":"(.+?)"'))[0]

    def pricing(self, response, raw_sku):
        currency = self.currency(response)
        money_strs = [currency, raw_sku['listPrice'], raw_sku.get('salePrice')] + raw_sku['promoMessages']
        return self.product_pricing_common(None, money_strs=money_strs, post_process=self.clean_money)

    def image_urls(self, raw_product):
        return [url_query_cleaner(raw_product[0]['prodImageURL'])]

    def is_out_of_stock(self, response):
        return response.css('[data-slnm-id=outOfStockText]')


class PaginationLE(LinkExtractor):

    def extract_links(self, response):
        if '/cat' not in response.url:
            return []

        current_page = int(url_query_parameter(response.url, 'goToPage', 1))
        pagination_css = 'script:contains(__NEXT_DATA__)::text'
        total_pages = clean(response.css(pagination_css).re('paginationCount":(\d+),'))[0]

        if current_page < int(total_pages):
            return [Link(add_or_replace_parameter(response.url, 'goToPage', current_page+1))]

        return []


class LoftOutletCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = LoftOutletParseSpider()

    listings_css = [
        '#megaMenuLinks',
        '.left-nav-list>li>a'
    ]
    products_css = '.itemAnchorWrapper'

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(PaginationLE(), callback='parse'),
     )
