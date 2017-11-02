import matplotlib
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

        price = clean(response.css('#productNowPrice::attr(value)'))[0]
        currency = clean(response.css('#productPriceCurrency::attr(value)'))[0]
        price = currency + price

        requests = self.size_requests(response)
        if requests:
            garment['meta'] = {'requests_queue': requests, 'price':price}
        else:
            garment['meta'] = {'requests_queue': [], 'price': price}
            response.meta['garment'] = garment
            garment['skus'].update(self.sku(response))

        return self.next_request_or_garment(garment)

    def size_requests(self, response):
        available_sizes = clean(response.css('.attribute__variants-group:first-child .attribute__swatch--available .swatchanchor::attr(data-link)'))
        return [Request(add_or_replace_parameter(size_url, 'format', 'ajax'), self.parse_size) for size_url in available_sizes]

    def parse_size(self, response):
        garment = response.meta['garment']
        requests = self.length_or_width_requests(response)
        if requests:
            garment['meta']['requests_queue'] += requests
        else:
            garment['skus'].update(self.sku(response))

        return self.next_request_or_garment(garment)

    def length_or_width_requests(self, response):
        available_lengths = clean(response.css('.attribute__variants-group:first-child + li .attribute__swatch--available .swatchanchor::attr(data-link)'))
        available_custom_lenghts = clean(response.css('.attribute__variants-group:first-child + li .js-custom-option-swatch::attr(data-link)'))
        return [Request(add_or_replace_parameter(length_url, 'format', 'ajax'), self.parse_length_or_width_requests) for length_url in available_lengths+available_custom_lenghts]

    def parse_length_or_width_requests(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.sku(response))
        return self.next_request_or_garment(garment)

    def sku(self, response):
        sku = {}
        custom_length_price = 0
        colour = clean(response.css('.colour-swatching .swatch--name::text'))
        if not colour:
            colour += [c_name for c_name, _ in matplotlib.colors.cnames.items() if c_name in response.meta['garment']['url']]
        colour = ' '.join(colour) if colour else "No_Colour"
        size = clean(response.css('.attribute__variants-group:first-child .attribute__swatch--selected .swatchanchor::text'))
        length = clean(response.css('.attribute__variants-group:first-child + li .attribute__swatch--selected .swatchanchor::text'))
        custom_length = clean(response.css('.js-custom-option-swatch.attribute__swatch--selected::attr(data-value)'))

        size = size[0] if size else self.one_size
        length = length[0] if length else ""

        if custom_length:
            length = custom_length[0]
            custom_length_price = float(clean(response.css('a.js-custom-sleeve-option::attr(data-price)'))[0][1:])

        size = size.replace("\"", "")
        size = size + ("/" + length if length else "")
        price, currency = float(response.meta['garment']['meta']['price'][1:]), response.meta['garment']['meta']['price'][0]
        price_str = currency + str(round(price + custom_length_price, 2))
        prices = self.product_pricing_common_new(response, [price_str])

        sku_id = size + ("_" + length if length else "")
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


class CtshirtsCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer + '-crawl'
    parse_spider = CtshirtsParseSpider()

    menu_css = ['.js-maincat']
    rules = (
        Rule(LinkExtractor(restrict_css=menu_css, attrs=('data-link'), tags=('span'), deny='sale'), callback='parse_category'),
    )

    def parse_category(self, response):
        total_product_count = clean(response.css('.sorting__results-total::text'))[0].strip()
        category_products_url = add_or_replace_parameter(response.url, 'sz', total_product_count)
        return Request(category_products_url, callback=self.parse_products)

    def parse_products(self, response):
        product_urls = clean(response.css('.product-image.tile__image a.thumb-link::attr(href)'))
        for product_url in product_urls:
            yield Request(product_url, callback=self.parse_item)
