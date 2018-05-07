import json

from scrapy.spiders import Request
from skuscraper.parsers.jsparser import JSParser

from .base import BaseParseSpider, BaseCrawlSpider, clean


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
        return clean(response.css('.product-information__description--features--product-code '
                                  'a::text'))[0]

    def product_name(self, response):
        return clean(response.css('.product-details__info-wrapper '
                                  '.product-details__title--product-detail::text'))[0]

    def product_brand(self, response):
        return clean(response.css('.product-details__info-wrapper '
                                  '.product-details__title--product-detail span::text'))[0]

    def product_category(self, response):
        breadcrumbs =  clean(response.css('span[itemprop="itemListElement"] span::text'))
        return [text for text in breadcrumbs if text not in ['Home', self.product_name(response)]]

    def product_gender(self, response, category):
        return (self.detect_gender_from_name(response) or self.detect_gender(category)
                or 'unisex-adults')

    def image_urls(self, response):
        raw_product = JSParser(
            clean(response.css('script:contains(productInfo)::text'))[0]
        )['productInfo']

        images = [image_urls['bigImageUrl']
                  for image_urls in raw_product['selectedProductColorVariation']['images']]

        images += [image_urls['bigImageUrl']
                   for variation in raw_product['otherProductColorVariation']
                   for image_urls in variation['images']]

        return images

    def skus(self, response):
        skus = {}

        raw_product = JSParser(
            clean(response.css('script:contains(productInfo)::text'))[0]
        )['productInfo']

        id = raw_product['productId']

        raw_prices = response.css('script').re_first(
            r'SITE.data.productPrices\["{}"] = SITE.dataImporter\((.*?)\);'.format(id))
        raw_prices = json.loads(raw_prices)

        currency = raw_prices['currencyCode']

        for raw_size in raw_product['selectedProductColorVariation']['sizes']:
            sku_id = raw_size['sku']
            sku = {}
            sku['size'] = raw_size['code']
            sku['colour'] = clean(raw_product['selectedProductColorVariation']['description'])
            sku['currency'] = currency

            for color in raw_prices['colours']:
                if (str(color['colourId']) ==
                        raw_product['selectedProductColorVariation']['colorId']):
                    sku['price'] = round(color['sellPrice'] * 100)
                    if round(color['rrpPrice'] * 100) > sku['price']:
                        sku['previous_prices'] = [round(color['rrpPrice'] * 100)]
                    break

            if not raw_size['active']:
                sku['out_of_stock'] = True

            skus[sku_id] = sku

        for variation in raw_product['otherProductColorVariation']:
            for raw_size in variation['sizes']:
                sku_id = raw_size['sku']
                sku = {}
                sku['size'] = raw_size['code']
                sku['colour'] = clean(variation['description'])
                sku['currency'] = currency

                for color in raw_prices['colours']:
                    if str(color['colourId']) == variation['colorId']:
                        sku['price'] = round(color['sellPrice'] * 100)
                        if round(color['rrpPrice'] * 100) > sku['price']:
                            sku['previous_prices'] = [round(color['rrpPrice'] * 100)]
                        break

                if not raw_size['active']:
                    sku['out_of_stock'] = True

                skus[sku_id] = sku

        return skus


class CotswoldCrawlSpider(BaseCrawlSpider):

    listing_url_template = ('https://www.cotswoldoutdoor.com/api/aem/search?'
                            'mainWebShop=cotswold&fictiveWebShop=62&anaLang=en&locale=en&'
                            'page={}&size=48&platform=public_site&filter={}')

    def parse(self, response):
        yield from super().parse(response)

        category_filter = response.css('script').re_first('"defaultSearchFilter":"(.*?)",')
        listing_url = self.listing_url_template.format(0, category_filter)

        listing_request = Request(url=listing_url, callback=self.parse_listings)
        listing_request.meta['trail'] = self.add_trail(response)
        listing_request.meta['filter'] = category_filter
        yield listing_request

    def parse_listings(self, response):
        yield from self.product_requests(response)

        listing = json.loads(response.text)
        total_pages = listing['totalPages']
        category_filter = response.meta['filter']

        for page_index in range(1, total_pages):
            pagination_url = self.listing_url_template.format(page_index, category_filter)
            pagination_request = Request(url=pagination_url, callback=self.parse_products)
            pagination_request.meta['trail'] = self.add_trail(response)
            yield pagination_request

    def parse_products(self, response):
        yield from self.product_requests(response)

    def product_requests(self, response):
        listing = json.loads(response.text)
        requests = []

        for item in listing['items']:
            if item['impression']['category'].lower() not in ['toys']:
                product_url = '/p{}.html'.format(item['seoUrl'])
                request = response.follow(product_url, callback=self.parse_item, dont_filter=True)
                request.meta['trail'] = self.add_trail(response)
                requests.append(request)

        return requests


class CotswoldUKParseSpider(MixinUK, CotswoldParseSpider):
    name = MixinUK.retailer + '-parse'


class CotswoldUKCrawlSpider(MixinUK, CotswoldCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = CotswoldUKParseSpider()
