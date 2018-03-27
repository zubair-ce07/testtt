from titlecase import titlecase
from scrapy import Request
from scrapy.spiders import Rule
from w3lib.url import url_query_cleaner
from .base import BaseParseSpider, BaseCrawlSpider, clean, LinkExtractor


class Mixin:
    retailer = 'orsay-de'
    allowed_domains = ['www.orsay.com']
    start_urls = ['http://www.orsay.com']
    market = 'DE'


class ParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '#product_main  span.price::text'
    care_css = 'div.product-care ::text'
    description_css = 'div.product-info ::text'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = 'women'
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)
        garment['meta'] = {'requests_queue': self.colour_requests(response)}
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        colour = clean(response.css('ul.product-colors li.active img ::attr(title)'))
        if colour:
            common_sku['colour'] = titlecase(colour[0])
        for size in response.css('div.sizebox-wrapper li.size-box'):
            sku = common_sku.copy()
            sku['size'] = clean(size.xpath('.//text()'))[0]
            if 'size-unavailable' in clean(size.xpath('.//@class'))[0]:
                sku['out_of_stock'] = True
            sku_id = '{}_{}'.format(sku['colour'], sku['size'])
            skus[sku_id] = sku
        return skus

    def colour_requests(self, response):
        urls = clean(response.css('ul.product-colors > li a::attr(href)'))
        urls.remove('#')
        return [Request(url=url, callback=self.parse_colour) for url in urls]

    def product_name(self, response):
        return clean(response.css('h1.product-name::text'))[0]

    def product_id(self, response):
        return clean(response.css('input[name="sku"]::attr(value)'))[0]

    def image_urls(self, response):
        return clean(response.css('div.product-image-gallery-thumbs > a::attr(href)'))

    def product_category(self, response):
        return clean(response.css('ul.breadcrumbs li[class*=category] a ::text'))


class CrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = ParseSpider()

    listing_css = [
        'ul#nav',
        'a.next'
    ]
    products_css = 'a.product-image'
    deny_re = '/de-de/specials'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_re), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css, process_value=url_query_cleaner), callback='parse_item')
    )
