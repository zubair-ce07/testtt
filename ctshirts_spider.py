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
    gender = 'men'


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
        garment['image_urls'] = self.image_urls(response)

        pprice, price = self.product_price(response)
        colour = self.detect_colour(garment['name'])

        requests = self.size_requests(response)
        garment['meta'] = {'requests_queue': requests, 'pprice':pprice, 'price': price, 'colour': colour}

        if not requests:
            garment['skus'].update(self.sku(response, pprice, price, colour))

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

    def sku(self, response, prod_pprice=None, prod_price=None, prod_colour=None):
        sku = {}
        colour, size, length, custom_length = self.sku_color_size(response)

        colour = colour[0] if colour else prod_colour if prod_colour else response.meta.get('garment', {}).get('meta', {}).get('colour', "")
        length = length[0] if length else custom_length[0] if custom_length else ""
        size = size[0] if size else self.one_size

        size = size.replace("\"", "")
        sku_id = size + ("_" + length if length else "")
        size = size + ("/" + length if length else "")

        prices = self.sku_price(response, custom_length, prod_pprice, prod_price)

        sku[sku_id] = {'size': size}
        sku[sku_id].update(prices)
        if colour:
            sku[sku_id].update({'colour': colour})
        return sku

    def sku_price(self, response, custom_length, prod_pprice ,prod_price):
        custom_length_price = 0
        if custom_length:
            custom_length_price = float(clean(response.css('a.js-custom-sleeve-option::attr(data-price)'))[0][1:])
        price_str = prod_price if prod_price else response.meta['garment']['meta']['price']
        pprice_str = prod_pprice if prod_pprice else response.meta['garment']['meta']['pprice']
        price, currency = float(price_str[1:]), price_str[0]
        price_str = currency + str(round(price + custom_length_price, 2))
        return self.product_pricing_common_new(response, [price_str, pprice_str])

    def sku_color_size(self, response):
        selected_colour_css = '.colour-swatching .swatch--name::text'
        selected_size_css = '.attribute__variants-group:first-child .attribute__swatch--selected ::text'
        selected_length_css = '.attribute__variants-group:first-child + li .attribute__swatch--selected ::text'
        selected_custom_length_css = '.js-custom-option-swatch.attribute__swatch--selected::attr(data-value)'

        colour = clean(response.css(selected_colour_css))
        size = clean(response.css(selected_size_css))
        length = clean(response.css(selected_length_css))
        custom_length = clean(response.css(selected_custom_length_css))

        return colour, size, length, custom_length

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

    def image_urls(self, response):
        return clean(response.css('.pdp-main__image_thumbnail::attr(src)'))

    def product_price(self, response):
        currency = clean(response.css('#productPriceCurrency::attr(value)'))[0]
        price = clean(response.css('#productNowPrice::attr(value)'))[0]
        pprice = clean(response.css('#productWasPrice::attr(value)'))[0]
        return currency + price, currency + pprice


class CtshirtsCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer + '-crawl'
    parse_spider = CtshirtsParseSpider()

    menu_css = ['.js-maincat']
    category_css = ['#category-level-1']
    product_css = ['.product-image.tile__image']

    rules = (
        Rule(LinkExtractor(restrict_css=menu_css, tags=('span'), attrs=('data-link'), deny='sale'), callback='parse'),
        Rule(LinkExtractor(restrict_css=category_css, tags=('a'), attrs=('search-link')), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=product_css, ), callback='parse_item')
    )

    def parse_pagination(self, response):

        yield from self.parse(response)

        product_css = '.product-image.tile__image a.thumb-link::attr(href)'
        pagination_css = '.infinite-scroll-placeholder[data-loading-state="unloaded"]::attr(data-grid-url)'
        product_urls = clean(response.css(product_css))

        if not product_urls:
            return

        pagination_url = clean(response.css(pagination_css))[0]
        yield Request(pagination_url, callback=self.parse_pagination)
