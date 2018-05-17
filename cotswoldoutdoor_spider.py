import json

from scrapy.spiders import Request
from w3lib.url import add_or_replace_parameter, url_query_parameter

from skuscraper.parsers.jsparser import JSParser
from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify


class Mixin:
    retailer = 'cotswoldoutdoor'
    allowed_domains = ['cotswoldoutdoor.com']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = [
        'https://www.cotswoldoutdoor.com/c/mens.html',
        'https://www.cotswoldoutdoor.com/c/womens.html',
        'https://www.cotswoldoutdoor.com/c/childrens.html',
        'https://www.cotswoldoutdoor.com/c/footwear.html',
        'https://www.cotswoldoutdoor.com/c/equipment/rucksacks.html'
    ]


class CotswoldOutdoorParseSpider(BaseParseSpider):
    description_css = '#sticky-container-productInformationId :not(strong)::text,' \
                      '#sticky-container-productFeaturesId div::text'
    deny_care = ['Product information', 'Product Code']

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(response, garment['category'])
        garment['image_urls'] = self.image_urls(response)
        garment['merch_info'] = self.merch_info(response, garment['description'] + garment['care'])
        garment['skus'] = self.skus(response)

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = '.product-information__description--features--product-code a::text'
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = '.product-details__info-wrapper .product-details__title--product-detail::text'
        return clean(response.css(css))[0]

    def product_brand(self, response):
        css = '.product-details__info-wrapper .product-details__title--product-detail span::text'
        return clean(response.css(css))[0]

    def raw_description(self, response):
        css = '#sticky-container-productFeaturesId li'
        return [''.join(clean(rd_s.css('::text'))) for rd_s in response.css(css)]

    def product_category(self, response):
        breadcrumbs = clean(response.css('span[itemprop="itemListElement"] span::text'))
        return [text for text in breadcrumbs if text not in ['Home', self.product_name(response)]]

    def product_gender(self, response, category):
        soup = soupify([self.product_name(response)] + category)
        gend = self.gender_lookup(soup)
        return gend or 'unisex-adults'

    def merch_info(self, response, description):
        merch_info = []
        raw_skus = self.raw_skus(response)

        for text in description:
            if 'limited edition' in text.lower():
                merch_info.append('Limited Edition')

        if all([sku['is_merch'] for _, sku in raw_skus.items()]):
            merch_info.append('Exclusive')

        return merch_info

    def image_urls(self, response):
        raw_product = self.raw_product(response)
        raw_images = [raw_product['selectedProductColorVariation']] \
                     + (raw_product['otherProductColorVariation'] or [])
        images = [img['bigImageUrl'] for raw_img in raw_images for img in raw_img['images']]
        return images

    def raw_product(self, response):
        raw_product_css = 'script:contains(productInfo)::text'
        return JSParser(clean(response.css(raw_product_css))[0])['productInfo']

    def raw_prices(self, response, product_id):
        raw_prices_re = f'SITE.data.productPrices\["{product_id}"] = SITE.dataImporter\((.*?)\);'
        return json.loads(response.css('script').re_first(raw_prices_re))

    def sku_price_map(self, response, product_id):
        raw_prices = self.raw_prices(response, product_id)
        currency = raw_prices['currencyCode']
        sku_price_map = {}

        for color in raw_prices['colours']:
            for sku in color['skus']:
                sku_price_map[str(sku['skuId'])] = [
                    sku['rrpPrice'], sku['standardPrice'], sku['sellPrice'], currency]

        return sku_price_map

    def sku_stock_map(self, response, product_id):
        raw_stock_re = f'SITE.data.productAvailabilities\["{product_id}"] = SITE.dataImporter\((.*?)\);'
        raw_stock = json.loads(response.css('script').re_first(raw_stock_re))
        sku_stock_map = {}

        for color in raw_stock['colorAvailabilities']:
            for sku in color['skuAvailabilities']:
                sku_stock_map[sku['skuCode']] = sku['stock']

        return sku_stock_map

    def sku_merch_map(self, response, product_id):
        raw_prices = self.raw_prices(response, product_id)
        sku_merch_map = {}

        for color in raw_prices['colours']:
            is_merch = True if 'exclusive' in (color.get('webThumbOverlayCode') or '').lower() else False
            for sku in color['skus']:
                sku_merch_map[str(sku['skuId'])] = is_merch

        return sku_merch_map

    def raw_skus(self, response):
        skus = {}

        raw_product = self.raw_product(response)
        product_id = raw_product['productId']

        sku_price_map = self.sku_price_map(response, product_id)
        sku_stock_map = self.sku_stock_map(response, product_id)
        sku_merch_map = self.sku_merch_map(response, product_id)

        raw_skus = [raw_product['selectedProductColorVariation']] \
                   + (raw_product['otherProductColorVariation'] or [])

        for raw_sku in raw_skus:
            for raw_size in raw_sku['sizes']:
                sku_id = raw_size['sku']

                if sku_id not in sku_price_map:
                    break

                sku = self.product_pricing_common(response, sku_price_map[sku_id])
                sku['size'] = raw_size['code']
                color = clean(raw_sku['description'] or [])
                sku['is_merch'] = sku_merch_map[sku_id] or []

                if color:
                    sku['colour'] = color

                if not sku_stock_map[sku_id]:
                    sku['out_of_stock'] = True

                skus[sku_id] = sku

        return skus

    def skus(self, response):
        skus = self.raw_skus(response)
        for _, sku in skus.items():
            del sku['is_merch']
        return skus


class CotswoldOutdoorCrawlSpider(BaseCrawlSpider):
    listing_url_template = 'https://www.cotswoldoutdoor.com/api/aem/search?' \
                           'mainWebShop=cotswold&fictiveWebShop=62&anaLang=en&locale=en&' \
                           'page={}&size=48&platform=public_site&filter={}'

    products_deny_re = [
        'bottle',
        'wash',
        'go-hydro',
        'electrolyte',
        'tablets',
        'energy',
        'protein',
        'wax',
        'first-aid-kit',
        'mug',
        'trangia',
        'harness',
        'goggle',
        'crampon'
    ]

    def parse(self, response):
        category_filter = response.css('script').re_first('"defaultSearchFilter":"(.*?)",')
        listing_url = self.listing_url_template.format(0, category_filter)

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)
        yield Request(url=listing_url, callback=self.parse_listings, meta=meta)

    def parse_listings(self, response):
        yield from self.product_requests(response)

        if url_query_parameter(response.url, 'page') != '0':
            return

        listing = json.loads(response.text)
        total_pages = listing['totalPages']

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        for page_index in range(1, total_pages):
            pagination_url = add_or_replace_parameter(response.url, 'page', page_index)
            yield Request(url=pagination_url, callback=self.parse_listings, meta=meta.copy())

    def product_requests(self, response):
        listing = json.loads(response.text)
        requests = []

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        for item in listing['items']:

            if item['impression']['category'].lower() in ['toys']:
                continue

            if any([True for text in self.products_deny_re if text in item['seoUrl']]):
                continue

            product_url = f"/p{item['seoUrl']}.html"
            request = response.follow(product_url, callback=self.parse_item, meta=meta.copy())
            requests.append(request)

        return requests


class CotswoldOutdoorUKParseSpider(MixinUK, CotswoldOutdoorParseSpider):
    name = MixinUK.retailer + '-parse'


class CotswoldOutdoorUKCrawlSpider(MixinUK, CotswoldOutdoorCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = CotswoldOutdoorUKParseSpider()
