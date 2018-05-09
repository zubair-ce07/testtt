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
    raw_description_css = '.product-information__description ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(response, garment['category'])
        garment['image_urls'] = self.image_urls(response)
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

    def product_category(self, response):
        breadcrumbs = clean(response.css('span[itemprop="itemListElement"] span::text'))
        return [text for text in breadcrumbs if text not in ['Home', self.product_name(response)]]

    def product_gender(self, response, category):
        soup = soupify([self.product_name(response)] + category)
        return self.gender_lookup(soup) or 'unisex-adults'

    def raw_product(self, response):
        raw_product_css = 'script:contains(productInfo)::text'
        return JSParser(clean(response.css(raw_product_css))[0])['productInfo']

    def image_urls(self, response):
        raw_product = self.raw_product(response)
        raw_images = [raw_product['selectedProductColorVariation']] \
                     + raw_product['otherProductColorVariation']
        images = [img['bigImageUrl'] for raw_img in raw_images for img in raw_img['images']]
        return images

    def skus(self, response):
        skus = {}

        raw_product = self.raw_product(response)
        product_id = raw_product['productId']

        raw_prices_re = f'SITE.data.productPrices\["{product_id}"] = SITE.dataImporter\((.*?)\);'
        raw_prices = json.loads(response.css('script').re_first(raw_prices_re))
        currency = raw_prices['currencyCode']

        color_price_map = {}
        for color in raw_prices['colours']:
            color_price_map[str(color['colourId'])] = [
                color['rrpPrice'], color['standardPrice'], color['sellPrice'], currency]

        raw_skus = [raw_product['selectedProductColorVariation']] \
                   + raw_product['otherProductColorVariation']

        for raw_sku in raw_skus:
            for raw_size in raw_sku['sizes']:
                sku_id = raw_size['sku']
                sku = self.product_pricing_common(response, color_price_map[raw_sku['colorId']])
                sku['size'] = raw_size['code']
                sku['colour'] = clean(raw_sku['description'])

                if not raw_size['active']:
                    sku['out_of_stock'] = True

                skus[sku_id] = sku

        return skus


class CotswoldOutdoorCrawlSpider(BaseCrawlSpider):

    listing_url_template = 'https://www.cotswoldoutdoor.com/api/aem/search?' \
                           'mainWebShop=cotswold&fictiveWebShop=62&anaLang=en&locale=en&' \
                           'page={}&size=48&platform=public_site&filter={}'

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
            product_url = f"/p{item['seoUrl']}.html"
            request = response.follow(product_url, callback=self.parse_item, meta=meta.copy())
            requests.append(request)

        return requests


class CotswoldOutdoorUKParseSpider(MixinUK, CotswoldOutdoorParseSpider):
    name = MixinUK.retailer + '-parse'


class CotswoldOutdoorUKCrawlSpider(MixinUK, CotswoldOutdoorCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = CotswoldOutdoorUKParseSpider()

