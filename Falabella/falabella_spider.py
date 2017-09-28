import re
import json

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'falabella-cl'
    lang = 'es'
    market = 'CL'
    allowed_domains = ['falabella.com', 'falabella.scene7.com']
    start_urls = [
        'http://www.falabella.com/falabella-cl/category/cat6930003/Hombre?id=cat6930003',
        'http://www.falabella.com/falabella-cl/category/cat6930168/Mujer?id=cat6930168',
        'http://www.falabella.com/falabella-cl/category/cat6930347/Ninos?id=cat6930347',
        'http://www.falabella.com/falabella-cl/category/cat4320009/Ver-Todo-Zapatillas',
        'http://www.falabella.com/falabella-cl/category/cat5620004/Vestuario',
    ]


class FalabellaParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    main_image_re = re.compile('(=\d+)')
    image_id_re = re.compile('Falabella/(\d+_\d)')

    gender_map = [
        ('mujer', 'women'),
        ('hombre', 'men'),
        ('niño', 'boys'),
        ('niña', 'girls'),
        ('unisex', 'unisex-adults')
    ]

    raw_product_re = 'fbra_browseMainProductConfig\s*=\s*(.*);'
    colour_re = 'Color:\s*(.*)'

    image_url_t = 'http://falabella.scene7.com/is/image/Falabella/' \
                  '{image_id}?$producto308$&wid=924&hei=924'

    image_request_url_t = 'http://falabella.scene7.com/is/image/Falabella/' \
                          '{product_id}/?req=set,json&id=PDP'

    def parse(self, response):
        raw_product = self.raw_product(response)
        garment = self.new_unique_garment(raw_product['id'])

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['brand'] = raw_product['brand']
        garment['name'] = raw_product['displayName']
        garment['care'] = self.product_care(response)
        garment['skus'] = self.skus(raw_product, response)
        garment['category'] = self.product_category(response)
        garment['description'] = self.product_description(response)
        garment['gender'] = self.product_gender(response, garment['name'])

        garment['image_urls'] = [self.main_image(response)]

        garment['meta'] = {
            'requests_queue': self.image_requests(raw_product)
        }

        return self.next_request_or_garment(garment)

    def parse_image(self, response):
        garment = response.meta['garment']
        garment['image_urls'] = self.image_urls(response, garment['image_urls'])

        return self.next_request_or_garment(garment)

    def main_image(self, response):
        css = '[data-content-type="image"]::attr(src)'
        image = clean(response.css(css))[0]

        return self.main_image_re.sub('=924', image)

    def image_urls(self, response, main_image):
        image_ids = set(self.image_id_re.findall(response.text))

        image_urls = main_image + [self.image_url_t.format(image_id=image_id)
                                   for image_id in image_ids]

        return sorted(set(image_urls), key=image_urls.index)

    def image_requests(self, raw_product):
        visited_colours = set()
        requests = []

        for raw_sku in raw_product['skus']:
            colour = raw_sku.get('color', 'default')

            if colour in visited_colours:
                continue

            visited_colours.add(colour)
            media_asset_id = raw_sku['mediaAssetId'] if 'color' in raw_sku else raw_product['mediaAssetId']
            url = self.image_request_url_t.format(product_id=media_asset_id)

            requests += [Request(url=url, callback=self.parse_image)]

        return requests

    def clean_product_pricing(self, response, raw_sku):
        nested_raw_pricing = [[price_soup['originalPrice'], price_soup['symbol']]
                              for price_soup in raw_sku['price']
                              if price_soup['label'] != 'CMR Puntos']

        raw_pricing = sum(nested_raw_pricing, [])

        return self.product_pricing_common_new(response, money_strs=raw_pricing)

    def skus(self, raw_product, response):
        skus = {}
        visitied_variants = set()
        product_colour = self.product_colour(response)

        for raw_sku in raw_product['skus']:
            sku = self.clean_product_pricing(response, raw_sku)
            sku['size'] = raw_sku.get('size', self.one_size)
            sku['size'] = self.one_size if sku['size'] == 'TU' else sku['size']

            if (raw_sku.get('color', ''), sku['size']) in visitied_variants:
                continue

            visitied_variants.add((raw_sku.get('color', ''), sku['size']))

            if 'color' in raw_sku or product_colour:
                sku['colour'] = raw_sku.get('color', product_colour)

            skus[raw_sku['skuId']] = sku

        return skus

    def product_colour(self, response):
        xpath = '//*[@data-panel="longDescription"]' \
                '//li[contains(text(), "Color")]/text()'
        colour = response.xpath(xpath).re(self.colour_re)

        return clean(colour)[0] if colour else colour

    def raw_description(self, response):
        css = '[data-panel="longDescription"] li::text,' \
              ' [data-panel="longDescription"] h4::text'

        specification_css = '.fb-product-information__specification__table__row-data'

        raw_description = clean(response.css(css))

        raw_description = [desc for desc in raw_description
                           if 'Atención al Cliente al' not in desc]

        raw_description += [self.merge_column_text(specification_row_sel)
                            for specification_row_sel in response.css(specification_css)]

        return raw_description

    def merge_column_text(self, row_sel):
        return ' '.join(clean(row_sel.css(' ::text')))

    def product_description(self, response):
        return [rd for rd in self.raw_description(response)
                if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response)
                if self.care_criteria_simplified(rd)]

    def product_gender(self, response, name):
        xpath = '//*[contains(text(), "Género")]/parent::*[th or li]//text()'

        soup = clean(response.xpath(xpath)) + [name]
        soup = ' '.join(soup).lower()

        for gender_key, gender in self.gender_map:
            if gender_key in soup:
                return gender

        return 'unisex-adults'

    def product_category(self, response):
        css = '.fb-masthead__breadcrumb__links ::text'

        return [c.replace('/ ', '') for c in clean(response.css(css))][1:]

    def raw_product(self, response):
        xpath = '//script[contains(text(), "skus")]'
        raw_product = response.xpath(xpath).re(self.raw_product_re)[0]

        return json.loads(raw_product)['state']['product']


class FalabellaCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = FalabellaParseSpider()

    listing_xpath = [
        '//div[@data-menu-panel>=5]',
        '//*[@rel="next"]'
    ]

    product_css = '#fbra_browseProductList .fb-pod-group__item'

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listing_xpath, tags=('link', 'a',)), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css, deny=Mixin.start_urls),
             callback='parse_item'),
    )
