import json

from scrapy.spiders import Request
from skuscraper.parsers.jsparser import JSParser

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify


class Mixin:
    retailer = 'cotswold'
    allowed_domains = ['cotswoldoutdoor.com']


class MixinUK(Mixin):
    retailer = Mixin.retailer + "-uk"
    market = "UK"
    start_urls = [
        'https://www.cotswoldoutdoor.com/c/mens.html',
        'https://www.cotswoldoutdoor.com/c/womens.html',
        'https://www.cotswoldoutdoor.com/c/childrens.html',
        'https://www.cotswoldoutdoor.com/c/footwear.html',
        'https://www.cotswoldoutdoor.com/c/equipment/rucksacks.html'
    ]


class CotswoldParseSpider(BaseParseSpider):
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
        id_css = '.product-information__description--features--product-code a::text'
        return clean(response.css(id_css))[0]

    def product_name(self, response):
        name_css = '.product-details__info-wrapper .product-details__title--product-detail::text'
        return clean(response.css(name_css))[0]

    def product_brand(self, response):
        brand_css = '.product-details__info-wrapper .product-details__title--product-detail ' \
                    'span::text'
        return clean(response.css(brand_css))[0]

    def product_category(self, response):
        breadcrumbs = clean(response.css('span[itemprop="itemListElement"] span::text'))
        return [text for text in breadcrumbs if text not in ['Home', self.product_name(response)]]

    def product_gender(self, response, category):
        soup = soupify([self.product_name(response)] + category)
        return self.gender_lookup(soup) or 'unisex-adults'

    def image_urls(self, response):
        raw_product_css = 'script:contains(productInfo)::text'
        raw_product = JSParser(clean(response.css(raw_product_css))[0])['productInfo']

        images = [image_urls['bigImageUrl']
                  for image_urls in raw_product['selectedProductColorVariation']['images']]

        images += [image_urls['bigImageUrl']
                   for variation in raw_product['otherProductColorVariation']
                   for image_urls in variation['images']]

        return images

    def skus(self, response):
        skus = {}

        raw_product_css = 'script:contains(productInfo)::text'
        raw_product = JSParser(clean(response.css(raw_product_css))[0])['productInfo']

        product_id = raw_product['productId']

        raw_prices_re = f'SITE.data.productPrices\["{product_id}"] = SITE.dataImporter\((.*?)\);'
        raw_prices = json.loads(response.css('script').re_first(raw_prices_re))

        currency = raw_prices['currencyCode']

        colors_map = {
            clean(raw_product['selectedProductColorVariation']['description']):
                raw_product['selectedProductColorVariation']['colorId']
        }
        for each in raw_product['otherProductColorVariation']:
            colors_map[clean(each['description'])] = each['colorId']

        for raw_size in raw_product['selectedProductColorVariation']['sizes']:
            sku_id = raw_size['sku']
            sku = {}
            sku['size'] = raw_size['code']
            sku['colour'] = clean(raw_product['selectedProductColorVariation']['description'])

            if not raw_size['active']:
                sku['out_of_stock'] = True

            skus[sku_id] = sku

        for variation in raw_product['otherProductColorVariation']:
            for raw_size in variation['sizes']:
                sku_id = raw_size['sku']
                sku = {}
                sku['size'] = raw_size['code']
                sku['colour'] = clean(variation['description'])

                if not raw_size['active']:
                    sku['out_of_stock'] = True

                skus[sku_id] = sku

        for _, sku in skus.items():
            for color in raw_prices['colours']:
                if str(color['colourId']) == colors_map[sku['colour']]:
                    money_str = [
                        color['rrpPrice'], color['standardPrice'], color['sellPrice'], currency
                    ]
                    sku.update(self.product_pricing_common(response, money_str))
                    break

        return skus


class CotswoldCrawlSpider(BaseCrawlSpider):

    listing_url_template = 'https://www.cotswoldoutdoor.com/api/aem/search?' \
                           'mainWebShop=cotswold&fictiveWebShop=62&anaLang=en&locale=en&' \
                           'page={}&size=48&platform=public_site&filter={}'

    def parse(self, response):
        yield from super().parse(response)

        category_filter = response.css('script').re_first('"defaultSearchFilter":"(.*?)",')
        listing_url = self.listing_url_template.format(0, category_filter)

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)
        meta['filter'] = category_filter
        yield Request(url=listing_url, callback=self.parse_listings, meta=meta)

    def parse_listings(self, response):
        yield from self.product_requests(response)

        listing = json.loads(response.text)
        total_pages = listing['totalPages']
        category_filter = response.meta['filter']

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        for page_index in range(1, total_pages):
            pagination_url = self.listing_url_template.format(page_index, category_filter)
            yield Request(url=pagination_url, callback=self.parse_products, meta=meta)

    def parse_products(self, response):
        yield from self.product_requests(response)

    def product_requests(self, response):
        listing = json.loads(response.text)
        requests = []

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        for item in listing['items']:
            if item['impression']['category'].lower() not in ['toys']:
                product_url = f"/p{item['seoUrl']}.html"
                request = response.follow(product_url, callback=self.parse_item, meta=meta)
                requests.append(request)

        return requests


class CotswoldUKParseSpider(MixinUK, CotswoldParseSpider):
    name = MixinUK.retailer + '-parse'


class CotswoldUKCrawlSpider(MixinUK, CotswoldCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = CotswoldUKParseSpider()
