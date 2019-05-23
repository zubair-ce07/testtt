import json

from urllib.parse import urljoin
from scrapy.spiders import Request

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'nnnow-in'
    market = 'IN'

    allowed_domains = ['nnnow.com']
    start_urls = ['https://api.nnnow.com/d/api/footerlinks']

    site_url = 'https://www.nnnow.com'
    product_listing_url = 'https://api.nnnow.com/d/apiV2/listing/products'

    headers = {
        "Content-Type": "application/json",
        "module": "odin"
    }


class NnnowParseSpider(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        raw_variants = self.variants(response)['PdpData']['mainStyle']

        sku_id = raw_variants['styleId']
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['name'] = raw_variants['name']
        garment['description'] = self.product_description(raw_variants)
        garment['care'] = self.product_care(raw_variants)
        garment['brand'] = raw_variants['brandName']
        garment['category'] = self.product_category(response)
        garment['image_urls'] = self.image_urls(raw_variants)
        garment['gender'] = raw_variants['gender']
        garment['skus'] = self.skus(raw_variants, response)

        garment['meta'] = {'requests_queue': self.colour_requests(response)}
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        raw_variants = self.variants(response)['PdpData']['mainStyle']
        garment['skus'].update(self.skus(raw_variants, response))

        return self.next_request_or_garment(garment)

    def variants(self, response):
        xpath = '//script[contains(., "window.DATA=")]/text()'
        script = response.xpath(xpath).re_first('=(.*)')
        return json.loads(script)['ProductStore']

    def product_category(self, response):
        return clean(response.css('.nw-breadcrumb-listitem::text'))

    def product_description(self, raw_variant):
        return [desc for desc in raw_variant['finerDetails']['specs']['list']]

    def product_care(self, raw_variant):
        return [care for care in raw_variant['finerDetails']['compositionAndCare']['list']]

    def image_urls(self, raw_variant):
        return [raw_image['large'] for raw_image in raw_variant['images']]

    def colour_requests(self, response):
        xpath = '//div[@class="nw-color-chips"]/a[not(contains(@class,"nw-color-item  selected"))]/@href'
        colour_urls = clean(response.xpath(xpath))

        return [Request(urljoin(self.site_url, url), callback=self.parse_colour) for url in colour_urls]

    def skus(self, raw_variant, response):
        price = raw_variant['skus'][0]['price']
        previous_price = raw_variant['skus'][0]['mrp']
        currency = clean(response.css('[itemprop="priceCurrency"]::text'))[0]

        common_sku = self.product_pricing_common(None, money_strs=[price, previous_price, currency])
        common_sku['colour'] = raw_variant['colorDetails']['secondaryColor']

        skus = {}

        for variant in raw_variant['skus']:
            sku = common_sku.copy()
            sku['size'] = variant['size']

            if not variant['inStock']:
                sku['out-of-stock'] = True

            skus[variant['skuId']] = sku

        return skus


class NnnowCrawlSpider(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = NnnowParseSpider()

    def parse(self, response):
        raw_json = json.loads(response.text)
        raw_product = raw_json['data'][1]['children']

        for product in raw_product[0]['children']:
            if '/all-categories' not in product['url']:
                yield Request(product['url'], callback=self.parse_category)

    def parse_category(self, response):
        raw_category = self.parse_spider.variants(response)

        category_id = raw_category['collectionId']
        category_name = response.url.split('/')[3]

        params = {
            'deeplinkurl': f"/{category_name}?p=1&cid={category_id}",
        }
        trail = self.add_trail(response)
        response.meta.update({'trail': trail, 'category_name': category_name, 'category_id': category_id})

        yield Request(self.product_listing_url, method='POST', body=json.dumps(params),
                      callback=self.parse_product_pagination,
                      headers=self.headers, meta=response.meta)

    def parse_product_pagination(self, response):
        if response.meta.get('pagination'):
            return

        trail = self.add_trail(response)

        category_name = response.meta.get('category_name')
        category_id = response.meta.get('category_id')

        raw_listing = json.loads(response.text)['data']
        raw_product = raw_listing['styles']['styleList']

        total_page_count = raw_listing['totalPages']

        for page in range(2, total_page_count, 1):
            params = {
                'deeplinkurl': f"/{category_name}?p={page}&cid={category_id}",
            }
            yield Request(self.product_listing_url, method='POST', body=json.dumps(params),
                          callback=self.parse_product_pagination, headers=self.headers,
                          meta={'trail': trail, 'pagination': True})

        yield from self.parse_product_request(raw_product, trail)

    def parse_product_request(self, raw_product, trail):
        for product in raw_product:
            url = urljoin(self.site_url, product['url'])
            yield Request(url, callback=self.parse_item, meta={'trail': trail})
