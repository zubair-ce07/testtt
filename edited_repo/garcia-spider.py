import json

from scrapy import Selector, FormRequest
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, LinkExtractor, BaseParseSpider, clean


class Mixin:
    retailer = 'garcia-nl'
    default_brand = 'GARCIA'
    allowed_domains = ['wearegarcia.com']
    market = 'NL'
    start_urls = ['https://www.wearegarcia.com/nl_NL/']


class GraciaParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.product-price ::text'
    raw_description_css = '.product-description ::text'
    size_request_url = 'https://www.wearegarcia.com/nl_NL/xhr/product/get_filter_attributes/'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_retailer_sku(response))
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        if len(response.css(".variant-group:not(.hidden)")) == 2:
            requests = self.size_requests(response)
            garment['meta'] = {'requests_queue': requests}
        else:
            garment['skus'] = self.skus(response)

        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.jeans_skus(response))
        return self.next_request_or_garment(garment)

    def product_name(self, response):
        return clean(response.css('.section-title::text'))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumb a>span::text'))[1:]

    def product_gender(self, response):
        gender_css = '.panel-body img::attr(src)'
        raw_gender = clean(response.css(gender_css))[0].lower()
        return self.detect_gender(raw_gender) or 'unisex-adults'

    def product_colour(self, response):
        color_soup = ' '.join(self.raw_description(response))
        color_soup = color_soup + ' '.join(clean(response.css('.table-striped ::text')))
        return self.detect_colour(color_soup)

    def jeans_skus(self, response):
        skus = {}
        waist = response.meta['waist']
        common_sku = response.meta['common_sku']
        raw_sub_skus = json.loads(response.body)
        css_selector = Selector(text=raw_sub_skus['html'])

        sizes_s = css_selector.css('.variant-filter-item')
        for size_s in sizes_s:
            sku = common_sku.copy()
            sku['size'] = clean(size_s.css('::text'))[0]

            if size_s.css('[class*="disabled"]'):
                sku['out_of_stock'] = True

            skus[f'{waist}_{clean(size_s.css("::text"))[0]}'] = sku

        return skus

    def skus(self, response):
        skus = {}
        common_sku = self.common_sku(response)
        sizes_s = response.css('.variant-filter-item')

        for size_s in sizes_s:
            sku = common_sku.copy()
            sku['size'] = clean(size_s.css('::text'))[0]

            if size_s.css('[class*="disabled"]'):
                sku['out_of_stock'] = True

            skus[f'{clean(size_s.css("::text"))[0]}'] = sku

        return skus

    def image_urls(self, response):
        image_paths = clean(response.css('.carousel-inner img::attr(src)'))
        return [response.urljoin(path) for path in image_paths]

    def size_requests(self, response):
        url = self.size_request_url + self.product_retailer_sku(response)
        headers = {"Content-Type": "application/json"}
        params = {"attribute": "19"}
        meta = {'common_sku': self.common_sku(response)}
        requests = []

        sizes_s = response.css('[data-attribute="19"]>.variant-filter-item:not([class*="disabled"])')
        for size_s in sizes_s:
            params["filters"] = {"19": int(clean(size_s.css('::attr(data-value)'))[0])}
            meta['waist'] = clean(size_s.css('::text'))[0]
            request = FormRequest(url=url, meta=meta, body=json.dumps(params), headers=headers,
                                  callback=self.parse_size, dont_filter=True)
            requests.append(request)

        return requests

    def common_sku(self, response):
        colour = self.product_colour(response)
        common_sku = self.product_pricing_common(response)

        if colour:
            common_sku['colour'] = colour

        return common_sku

    def product_retailer_sku(self, response):
        return clean(response.css('[name="product"]::attr(value)'))[0]


class GraciaCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    listings_css = ['.list-unstyled', '.pagination']
    products_css = ['.product']
    parse_spider = GraciaParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
