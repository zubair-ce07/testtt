from scrapy.spiders import Rule
from scrapy.http import Request
from w3lib.url import add_or_replace_parameter
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'ctshirts-uk'
    market = 'UK'
    allowed_domains = ['ctshirts.com']
    start_urls = ['http://www.ctshirts.com/uk/homepage']


class CtshirtsParseSpider(BaseParseSpider, Mixin):

    name = Mixin.retailer + '-parse'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        is_suit = clean(response.css('#product-set-list'))
        if is_suit:
            return

        self.boilerplate_normal(garment, response)
        garment['skus'] = {}
        garment['gender'] = self.product_gender()
        garment['image_urls'] = self.image_urls(response)

        price = self.product_price(response)
        colour = self.detect_colour(garment['name'])

        requests = self.size_requests(response)
        garment['meta'] = {'requests_queue': requests, 'price': price, 'colour': colour}

        if not requests:
            garment['skus'].update(self.sku(response, price, colour))

        return self.next_request_or_garment(garment)

    def size_requests(self, response):
        size_css = '.attribute__variants-group:first-child .attribute__swatch--available ::attr(data-link)'
        sizes = clean(response.css(size_css))
        return [Request(add_or_replace_parameter(size_url, 'format', 'ajax'), self.parse_size) for size_url in sizes]

    def parse_size(self, response):
        garment = response.meta['garment']
        requests = self.length_or_width_requests(response)
        garment['meta']['requests_queue'] += requests
        if not requests:
            garment['skus'].update(self.sku(response))

        return self.next_request_or_garment(garment)

    def length_or_width_requests(self, response):
        length_css = '.attribute__variants-group:first-child + li .attribute__swatch--available ::attr(data-link)'
        custom_length_css = '.attribute__variants-group:first-child + li .js-custom-option-swatch::attr(data-link)'

        lengths = clean(response.css(length_css))
        custom_lenghts = clean(response.css(custom_length_css))

        return [Request(add_or_replace_parameter(length_url, 'format', 'ajax'), self.parse_length_or_width) for length_url in lengths+custom_lenghts]

    def parse_length_or_width(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.sku(response))
        return self.next_request_or_garment(garment)

    def sku(self, response, sku_price=None, prod_colour=None):
        sku = {}
        custom_length_price = 0

        slctd_colour_css = '.colour-swatching .swatch--name::text'
        slctd_size_css = '.attribute__variants-group:first-child .attribute__swatch--selected .swatchanchor::text'
        slctd_len_css = '.attribute__variants-group:first-child + li .attribute__swatch--selected .swatchanchor::text'
        slctd_cus_len_css = '.js-custom-option-swatch.attribute__swatch--selected::attr(data-value)'

        colour = clean(response.css(slctd_colour_css))
        size = clean(response.css(slctd_size_css))
        length = clean(response.css(slctd_len_css))
        custom_length = clean(response.css(slctd_cus_len_css))

        colour = colour[0] if colour else prod_colour if prod_colour else response.meta['garment']['meta']['colour']
        length = length[0] if length else custom_length[0] if custom_length else ""
        size = size[0] if size else self.one_size

        if custom_length:
            custom_length_price = float(clean(response.css('a.js-custom-sleeve-option::attr(data-price)'))[0][1:])

        size = size.replace("\"", "")
        sku_id = size + ("_" + length if length else "")
        size = size + ("/" + length if length else "")

        sk_price = sku_price if sku_price else response.meta['garment']['meta']['price']
        price, currency = float(sk_price[1:]), sk_price[0]
        price_str = currency + str(round(price + custom_length_price, 2))

        prices = self.product_pricing_common_new(response, [price_str])

        sku[sku_id] = {'colour': colour, 'size': size}
        sku[sku_id].update(prices)
        return sku

    def product_id(self, response):
        return clean(response.css('[itemprop="productID"]::text'))[0]

    def product_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]

    def product_description(self, response):
        return clean(response.css('.pdp-main__slot-signature::text'))

    def product_care(self, response):
        return clean(response.css('.pdp-main__slot.pdp-main__slot--left-group.desktop-only .pdp-main__p-feature::text'))

    def product_category(self, response):
        return clean(response.css('.breadcrumb__link a::text, .breadcrumb__link::text'))[1:]

    def product_gender(self):
        return 'Men'

    def image_urls(self, response):
        return clean(response.css('.pdp-main__image_thumbnail::attr(src)'))

    def product_price(self, response):
        price = clean(response.css('#productNowPrice::attr(value)'))[0]
        currency = clean(response.css('#productPriceCurrency::attr(value)'))[0]
        return currency + price


class CtshirtsCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer + '-crawl'
    parse_spider = CtshirtsParseSpider()

    menu_css = ['.js-maincat']

    rules = (
        Rule(LinkExtractor(restrict_css=menu_css, attrs=('data-link'), tags=('span'), deny='sale'), callback='parse_products'),
    )

    def parse_products(self, response):
        product_css = '.product-image.tile__image a.thumb-link::attr(href)'
        pagination_css = '.infinite-scroll-placeholder[data-loading-state="unloaded"]::attr(data-grid-url)'

        product_urls = clean(response.css(product_css))
        for product_url in product_urls:
            yield Request(product_url, callback=self.parse_item, dont_filter=True)

        if not product_urls:
            return

        pagination_url = clean(response.css(pagination_css))[0]
        yield Request(pagination_url, callback=self.parse_products, dont_filter=True)

