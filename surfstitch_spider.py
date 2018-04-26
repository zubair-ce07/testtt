import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule
from w3lib.url import url_query_cleaner

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'surfstitch'
    allowed_domains = ['surfstitch.com']


class MixinAU(Mixin):
    retailer = Mixin.retailer + "-au"
    market = "AU"
    start_urls = ['https://www.surfstitch.com/']
    default_brand = 'SurfStitch'

    homeware_categories = [
        'homeware',
        'beach accessories',
        'towels'
    ]


class SurfStitchParseSpider(BaseParseSpider):
    price_css = '#product-content > .product-price .price-to-convert::text'
    raw_description_css = '.tab-switch[checked] ~ .tab-content ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['image_urls'] = []
        garment['merch_info'] = self.merch_info(response)

        if self.is_homeware(garment['category']):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(garment['category'])

        requests = self.colour_requests(response)
        garment['meta'] = {
            'requests_queue': requests
        }

        if not requests:
            garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        requests = self.sku_requests(response)
        garment['meta']['requests_queue'] += requests

        if not requests:
            garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def sku_requests(self, response):
        url_css = '.swatches.size .selectable a::attr(href)'
        sku_requests = [Request(url=url, callback=self.parse_skus)
                        for url in clean(response.css(url_css))]
        return sku_requests

    def colour_requests(self, response):
        url_css = '.swatches.swatchcolour .selectable a::attr(href)'
        colour_requests = [Request(url=url, callback=self.parse_colour)
                           for url in clean(response.css(url_css))]
        return colour_requests

    def product_id(self, response):
        return clean(response.css('[itemprop="productID"]::attr(data-masterid)'))[0]

    def product_name(self, response):
        return clean(response.css('.product-name::text'))[0]

    def product_brand(self, response):
        brand = clean(response.css('.brand-name::text'))[0]
        return brand.title()

    def product_category(self, response):
        return clean(response.css('a.breadcrumb-element ::text'))

    def product_gender(self, category):
        return self.detect_gender(category) or 'unisex-adults'

    def merch_info(self, response):
        promos = response.css('.promotion-accordion span')
        return [''.join(promo.css('::text').extract()) for promo in promos]

    def is_homeware(self, category):
        soup = ' '.join(category).lower()
        return any(category in soup for category in self.homeware_categories)

    def image_urls(self, response):
        images = clean(response.css('.thumbnail-link::attr(href)'))
        return [response.urljoin(img) for img in images]

    def skus(self, response):
        raw_sku = json.loads(clean(response.css('.product-variations::attr(data-attributes)'))[0])

        if not raw_sku:
            return {}

        sku_id = response.css("[itemprop='productID']::text").extract_first()
        out_of_stock = response.css('button#add-to-cart[disabled]')

        sku = self.product_pricing_common(response)

        colour = raw_sku['swatchColour']['value'] if 'swatchColour' in raw_sku else None
        colour = colour if colour else self.detect_colour_from_name(response)
        if colour:
            sku['colour'] = colour.title()

        sku['size'] = raw_sku['size']['value'] if 'size' in raw_sku else self.one_size

        if out_of_stock:
            sku['out_of_stock'] = True

        return {f'{sku_id}': sku}


class SurfStitchCrawlSpider(BaseCrawlSpider):
    listings_css = '.menu-category'
    products_css = '.product-name'

    page_size = 20

    deny_r = [
        'audio',
        'beach-accessories',
        'cameras',
        'camping-gear',
        'dvds',
        'general-accessories',
        'swim-accessories',
        'phone-cases-accessories',
        'tablet-cases-accessories',
        'hardware',
        'wax',
        'board-racks',
        'surfboards',
        'softboards',
        'bodyboards',
        'skate',
        'sups/boards',
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css, process_value=url_query_cleaner),
             callback='parse_item')
    ]

    def parse(self, response):
        yield from super().parse(response)

        total_products = response.css('.results-hits::text').re_first(r'(.+?) Results') or '0'
        total_products = int(total_products.replace(',', ''))

        for page_index in range(0, total_products, self.page_size):
            products_page = response.urljoin('?start={}'.format(page_index))
            request = Request(products_page, callback=self.parse)
            request.meta['trail'] = self.add_trail(response)
            yield request


class SurfStitchAUParseSpider(MixinAU, SurfStitchParseSpider):
    name = MixinAU.retailer + '-parse'


class SurfStitchAUCrawlSpider(MixinAU, SurfStitchCrawlSpider):
    name = MixinAU.retailer + '-crawl'
    parse_spider = SurfStitchAUParseSpider()
