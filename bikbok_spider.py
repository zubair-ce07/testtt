import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import FormRequest

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'bikbok'
    allowed_domains = ['bikbok.com']
    gender = 'women'


class MixinSE(Mixin):
    retailer = Mixin.retailer + "-se"
    market = "SE"
    start_urls = ['https://www.bikbok.com/sv/']
    default_brand = 'Bik Bok'


class BikBokParseSpider(BaseParseSpider):
    price_css = '.product-info-container .product-price span::text'
    raw_description_css = ".accordion-navigation:contains('Produktinformation')"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['merch_info'] = self.merch_info(response)
        garment['category'] = [text for text, _ in garment['trail']]
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)
        garment['description'].insert(0, clean(response.css('.product-info-container p::text')))
        garment['care'] += clean(response.css(self.raw_description_css).css('img::attr(alt)'))

        garment['meta'] = {
            'requests_queue': self.colour_requests(response)
        }

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        urls = clean(response.css('.color-item:not(.active) a::attr(href)'))
        return [response.follow(u, callback=self.parse_colour, dont_filter=True) for u in urls]

    def product_id(self, response):
        return re.search('/(\d+)_', response.url).group(1)

    def product_name(self, response):
        return clean(response.css('.product-title::text'))[0]

    def merch_info(self, response):
        return clean(response.css('.product-info-container .product-campaign::text'))

    def image_urls(self, response):
        images = clean(response.css('.product .image-wrap img::attr(src)'))
        return [response.urljoin(img) for img in images]

    def skus(self, response):
        skus = {}

        colour = clean(response.css('.color-item.active a img::attr(alt)'))
        colour = colour[0] if colour else self.detect_colour_from_name(response)

        raw_skus = response.css('.product-property-list.size-picker button')

        for raw_sku in raw_skus:
            sku_id = clean(raw_sku.css('::attr(data-sku-id)'))[0]
            in_stock = clean(raw_sku.css('::attr(data-amount-in-stock)'))[0]

            sku = self.product_pricing_common(response)
            sku['size'] = clean(raw_sku.css('::text'))[0]
            sku['currency'] = response.css('script::text').re_first('currency:"(\w+)",')

            if colour:
                sku['colour'] = colour

            if in_stock == '0':
                sku['out_of_stock'] = True

            skus[sku_id] = sku

        return skus


class BikBokCrawlSpider(BaseCrawlSpider):
    listings_css = 'ul#main-navigation'
    post_request_url = 'https://bikbok.com/sv/api/product/post'
    page_size = 60

    deny_r = [
        'new-in',
        'view-all',
        'top-sellers',
        'coming-soon-items',
        'inspirationlook',
        'bikbokgallery'
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r),
             callback='parse')
    ]

    def parse(self, response):
        yield from super().parse(response)

        product_urls = response.css("script::text").re(',Url:"(.*?)"')
        yield from self.product_requests(response, product_urls)

        total_products = response.css('.enhanced-box .right::text').re_first('(\d+)') or '0'
        total_products = int(total_products)
        total_pages = int(total_products / self.page_size)

        params = self.get_params(response)

        for page_index in range(1, total_pages + 1):
            params['Page'] = str(page_index)
            pagination_request = FormRequest(url=self.post_request_url, headers={'Accept': ''},
                                             formdata=params, callback=self.parse_post_request)
            pagination_request.meta['trail'] = self.add_trail(response)
            yield pagination_request

    def parse_post_request(self, response):
        raw_products = json.loads(response.text)
        product_urls = [product['Url'] for product in raw_products['Products']]
        yield from self.product_requests(response, product_urls)

    def product_requests(self, response, products):
        requests = []

        for url in products:
            request = response.follow(url, callback=self.parse_item)
            request.meta['trail'] = self.add_trail(response)
            requests.append(request)

        return requests

    def get_params(self, response):
        scripts = response.css('script::text')
        return {
            'Language': clean(response.css('html::attr(lang)'))[0],
            'MarketId': scripts.re_first('marketId:"(.*?)"'),
            'CatalogNode': scripts.re_first('currentCatalogNode:"(.*?)"'),
            'FetchAllPages': 'false',
            'Sorting': scripts.re_first('sortOrder:"(.*?)"'),
            'ItemsPerPage': scripts.re_first('itemsPerPage:"(\d+)"'),
            'ProductSearchPageId': scripts.re_first('productSearchPageId:(\d+)')
        }


class BikBokSEParseSpider(MixinSE, BikBokParseSpider):
    name = MixinSE.retailer + '-parse'


class BikBokSECrawlSpider(MixinSE, BikBokCrawlSpider):
    name = MixinSE.retailer + '-crawl'
    parse_spider = BikBokSEParseSpider()
