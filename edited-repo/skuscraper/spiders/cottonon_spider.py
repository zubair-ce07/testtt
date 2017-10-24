from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'cottonon-us'
    allowed_domains = ['cottonon.com']
    lang = 'en'
    market = 'US'
    start_urls_with_meta = [
        ('https://cottonon.com/AU/men/', {'gender': 'men'}),
        ('https://cottonon.com/AU/women/', {'gender': 'women'}),
        ('https://cottonon.com/AU/men/?prefn1=isSale&prefv1=Yes', {'gender': 'men'}),
        ('https://cottonon.com/AU/women/?prefn1=isSale&prefv1=Yes', {'gender': 'women'}),
    ]


class CottononParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.product-price span[class*="price"]::text'

    def parse(self, response):
        p_id = self.product_id(response)
        garment = self.new_unique_garment(p_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)
        garment['meta'] = {'requests_queue': self.colour_request(response)}
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def colour_request(self, response):
        colour_requests = []
        requests_urls = clean(response.css('.color li:not([class*="selected"]) a[title*="Colour"]::attr(href)'))
        for r_url in requests_urls:
            colour_requests.append(Request(r_url, callback=self.parse_colour))
        return colour_requests

    def skus(self, response):
        skus = {}
        common = self.product_pricing_common_new(response)
        colour_css = '.color a[href*="{c_code}"] img::attr(alt)'
        colour_code = clean(response.css('.product-code ::text'))[0].split("-")[1]
        common['colour'] = clean(response.css(colour_css.format(c_code=colour_code)))[0]

        size_selector = response.css('.size li a')
        for size_s in size_selector:
            sku = common.copy()
            sku['size'] = clean(size_s.css('span::text'))[0]
            if not size_s.css(' ::attr(href)'):
                sku['out_of_stock'] = True
            skus["{}_{}".format(common['colour'], sku['size'])] = sku
        return skus

    def product_care(self, response):
        return []

    def product_category(self, response):
        return clean(response.css('.breadcrumbs a::text'))

    def product_id(self, response):
        return clean(response.css('.product-code ::text'))[0].split("-")[0]

    def product_name(self, response):
        return clean(response.css('.product-detail .product-name ::text'))[0]

    def product_description(self, response):
        return clean(response.css('div#details-description-container .product-content ::text'))

    def image_urls(self, response):
        img_urls = clean(response.css('.product-thumbnails img::attr(src)'))
        return [url_query_cleaner(url, ()) for url in img_urls]

    def product_brand(self, response):
        return clean(response.xpath('//div[contains(@class,"product-col-2")]/div[1]/text()'))[0]


class CottononCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = CottononParseSpider()
    products_css = '.search-result-items'

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse(self, response):
        yield from super(CottononCrawlSpider, self).parse(response)
        next_url = clean(response.css('.show-for-large .pagination .page-next::attr(href)'))
        if not next_url:
            return
        response.meta['trail'] = self.add_trail(response)
        yield Request(next_url[0], meta=response.meta, callback=self.parse)
