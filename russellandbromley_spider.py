import json
import re

from scrapy import Request, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    retailer = 'russellandbromley'
    listing_request_url_t = "http://fsm.attraqt.com/zones-js.aspx?siteId=ba6279ce-57d8-4069-8651-04459b92bceb&" \
                            "zone0=category&mergehash=true&pageurl={}&config_categorytree={}&" \
                            "config_parentcategorytree={}&config_category={}"


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    allowed_domains = ['russellandbromley.co.uk']
    start_urls = ['http://www.russellandbromley.co.uk/']


class RussellAndBromleyParseSpider(BaseParseSpider):
    brand_css = '.logoBox a::attr(title)'
    care_css = '.detailsWrapper ::text'
    raw_description_css = '.invtdesc1 ::text'
    price_css = '.oneProduct .priceField ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = '#tag-invtref::text'
        return clean(response.css(css))[0][:4]

    def product_name(self, response):
        css = '#tag-invtname::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '.crumbtrail a::text'
        return clean(response.css(css))[1:]

    def product_gender(self, garment):
        soup = ' '.join(garment['category'])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def image_urls(self, response):
        css = '#productdetail-altview ~ script:contains(StoreImageSwaps)'
        raw_urls = clean(response.css(css).re(f'imgL: \[(.*?)\]'))[0].split(',')
        return [url.strip('"') for url in raw_urls if url != '""']

    def raw_skus(self, response):
        raw_skus = response.css('script:contains(StoreJSON)').re('{.*}')
        return [json.loads(f'[{raw_sku}]') for raw_sku in raw_skus]

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        colour_x = "//*[contains(@name, 'oitemxoixtcolour')]/@value"
        common_sku['colour'] = clean(response.xpath(colour_x))[0]

        for raw_sku in self.raw_skus(response):
            sku = common_sku.copy()
            size = raw_sku[0]['att1']
            sku['size'] = self.one_size if size == 'One Size Only' else size

            if not raw_sku[1]['atronhand']:
                sku['out_of_stock'] = True

            sku_id = raw_sku[1]['atrsku']
            skus[sku_id] = sku

        return skus

    def colour_requests(self, response):
        css = '#otherColoursMaterials a::attr(href)'
        urls = clean(response.css(css))
        return [response.follow(url, callback=self.parse_colour) for url in set(urls)]


class RussellAndBromleyCrawlSpider(BaseCrawlSpider):
    listing_css = [
        '#mm_ul',
    ]

    sub_listing_css = [
        '.categoryNavigation',
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=sub_listing_css), callback='parse_listing'),
    ]

    def parse_listing(self, response):
        category_values = self.exract_category(response)
        api_request_url = self.listing_request_url_t.format(response.url, category_values[0],
                                                            category_values[1], category_values[2])
        meta = {'request_url': api_request_url}
        return Request(api_request_url, callback=self.parse_products, meta=meta, dont_filter=True)

    def parse_products(self, response):
        raw_urls = json.loads(re.findall('{.*}', response.text)[1])
        raw_urls_s = Selector(text=raw_urls['html'])
        urls = clean(raw_urls_s.css('.image a::attr(href)'))
        meta = {'trail': self.add_trail(response)}

        requests = [Request(f'http://www.russellandbromley.co.uk{url}',
                            callback=self.parse_item, meta=meta.copy()) for url in urls]

        api_request_url = response.meta.get('request_url')
        css = ".pagnNumbers a[rel='next']::attr(href)"
        next_page_url = clean(raw_urls_s.css(css))

        if not all([next_page_url, api_request_url]):
            return requests

        page_url = f'http://www.russellandbromley.co.uk{next_page_url[0]}'
        api_request_url = add_or_replace_parameter(api_request_url, 'pageurl', page_url)
        return requests + [Request(api_request_url, callback=self.parse_products, dont_filter=True)]

    def exract_category(self, response):
        css = 'script:contains(config)'
        raw_category = response.css(css)
        return raw_category.re(r'"categorytree","(.*?)"')[0], \
               raw_category.re(r'"parentcategorytree","(.*?)"')[0], \
               raw_category.re(r'"category","(.*?)"')[0]


class RussellAndBromleyUKParseSpider(MixinUK, RussellAndBromleyParseSpider):
    name = MixinUK.retailer + '-parse'


class RussellAndBromleyUKCrawlSpider(MixinUK, RussellAndBromleyCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = RussellAndBromleyUKParseSpider()
