import re
import json

from scrapy.spiders import Request

from .base import BaseParseSpider, BaseCrawlSpider, clean


class MixinLoftOutlet:
    market = 'US'
    retailer = 'loft-outlet-us'
    lang = 'en'
    gender = 'women'
    brand = 'Loft'
    currency = 'USD'

    allowed_domains = ['outlet.loft.com', 's7d2.scene7.com']
    start_urls = [
        'https://outlet.loft.com',
    ]


class ParseSpiderLoftOutlet(BaseParseSpider, MixinLoftOutlet):
    name = MixinLoftOutlet.retailer + '-parse'
    image_url_t = 'https://s7d2.scene7.com/is/image/{}'
    images_url_t = 'https://s7d2.scene7.com/is/image/LOS/{}_{}_IS?req=set,json'

    def parse(self, response):
        raw_products = self.raw_products(response)
        raw_product = raw_products[0]
        sku_id = self.product_id(raw_product)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = self.product_name(raw_product)
        garment['gender'] = self.gender
        garment['skus'] = self.skus(response, raw_products)
        garment['brand'] = self.brand
        garment['description'] = self.product_description(raw_product)
        garment['care'] = self.product_care(raw_product)
        garment['category'] = self.product_category(response)
        garment['merch_info'] = self.merch_info(raw_product)
        garment['image_urls'] = []
        garment['meta'] = {'requests_queue': self.image_requests(response, raw_products)}

        return self.next_request_or_garment(garment)

    def skus(self, response, raw_products):
        skus = {}

        for raw_product in raw_products:
            money_strs = [raw_product['listPrice'], self.currency] + self.sale_price(raw_product)
            common_sku = self.product_pricing_common(response, money_strs=money_strs)

            for color in raw_product['skucolors']['colors']:
                common_sku['colour'] = color['colorName']

                for size in color['skusizes']['sizes']:
                    sku = common_sku.copy()
                    sku['size'] = size['sizeAbbr']

                    if size['available'] != 'true':
                        sku['out_of_stock'] = True

                    sku_id = size['skuId']
                    skus[sku_id] = sku

        return skus

    def image_requests(self, response, raw_products):
        sku_id = raw_products[0]['prodId']
        raw_colors = [product['skucolors']['colors'] for product in raw_products]
        colors = [c['colorCode'] for colors in raw_colors for c in colors]
        meta = {'trail': self.add_trail(response)}
        return [Request(url=self.images_url_t.format(sku_id, c), callback=self.parse_images,
                        meta=meta.copy()) for c in colors]

    def parse_images(self, response):
        garment = response.meta['garment']
        raw_images = re.search('"item":(.*)}}', response.text).group(1)
        images = json.loads(raw_images)

        if isinstance(images, list):
            garment['image_urls'] += [self.image_url_t.format(im['i']['n']) for im in images]
            return self.next_request_or_garment(garment)

        garment['image_urls'] += [self.image_url_t.format(images['i']['n'])]
        return self.next_request_or_garment(garment)

    def product_id(self, raw_product):
        return raw_product['prodId']

    def raw_products(self, response):
        raw_script = response.css('#__next-error+script+script::text').extract_first()
        raw_product = re.search('"products":(\[{.+}\]),"ship', raw_script).group(1)
        return json.loads(raw_product)

    def product_description(self, raw_product, **kwargs):
        return [v for k, v in raw_product.items() if 'bulletPoint' in k and v]

    def product_care(self, raw_product, **kwargs):
        return [raw_product['garmentCare']] + raw_product['fabricationContent'].split(',')

    def sale_price(self, raw_product):
        if 'salePrice' in raw_product:
            return [raw_product['salePrice']]

        raw_price = [promo for promo in raw_product['promoMessages'] if '$' in promo]
        return [re.search('(\$[\d\.?]+)', raw_price[0]).group(1)] if raw_price else []

    def product_name(self, raw_product):
        return raw_product['displayName']

    def product_category(self, response):
        category_css = '.undefined>a span[id]::text'
        return clean(response.css(category_css))[1:]

    def merch_info(self, raw_product):
        return [promo for promo in raw_product['promoMessages'] if '$' not in promo]


class CrawlSpiderLoftOutlet(BaseCrawlSpider, MixinLoftOutlet):
    name = MixinLoftOutlet.retailer + '-crawl'
    parse_spider = ParseSpiderLoftOutlet()
    cat_url_t = 'https://outlet.loft.com/model/services/endecaSimplifiedService?props=productInfo&catid={}{}'
    cat_page_url_t = '&goToPage={}'
    allow_cats = ['Accessories &amp; Shoes', 'Clothing', 'Petites']
    deny_cats = {'cat3950040', 'cat3950062', 'cat4150003', 'cat3950029', 'cat4150004', 'cat3950042'}

    def parse_start_url(self, response):
        raw_categories = response.css('#__next-error+script+script::text').extract_first()
        categories = re.search('"subNav":({.*})},"result"', raw_categories).group(1)
        category_ids = self.filter_category_ids(json.loads(categories).items())

        for cat_id in category_ids:
            url = self.cat_url_t.format(cat_id, '')
            meta = {'cat_id': cat_id, 'page': 1, 'trail': self.add_trail(response)}
            yield Request(url=url, callback=self.parse_category, meta=meta.copy())

    def parse_category(self, response):
        raw_products = json.loads(response.text)
        response.meta['trail'] = self.add_trail(response)

        yield from self.product_requests(response, raw_products)

        yield from self.page_requests(response, raw_products)

    def product_requests(self, response, raw_products):
        for product in raw_products['productInfo']['records']:

            if 'quickLookUrl' not in product:
                return

            url = response.urljoin(product['quickLookUrl'])
            yield Request(url=url, callback=self.parse_item, meta=response.meta.copy())

    def page_requests(self, response, raw_products):
        cat_page = response.meta['page']
        pagination_count = raw_products['productInfo']['paginationCount']

        if pagination_count >= cat_page:
            cat_id = response.meta['cat_id']
            meta = {'cat_id': cat_id, 'page': cat_page + 1, 'trail': response.meta['trail']}
            url = self.cat_url_t.format(cat_id, self.cat_page_url_t.format(cat_page + 1))
            yield Request(url=url, callback=self.parse_category, meta=meta.copy())

    def filter_category_ids(self, cats):
        return {v['catid'] for k, v in cats if self.is_required_category(k)} - self.deny_cats

    def is_required_category(self, category):
        if any(cat in category for cat in self.allow_cats):
            return True

        return False
