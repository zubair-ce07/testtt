import json

from scrapy import Selector, FormRequest
from scrapy.http import Response
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, LinkExtractor, BaseParseSpider, clean


class Mixin:
    retailer = 'garcia-nl'
    allowed_domains = ['wearegarcia.com']
    market = 'NL'
    start_urls = ['https://www.wearegarcia.com/nl_NL/']


class GraciaParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.product-price [class*="price"]::text'
    raw_description_css = '.product-description>p::text'

    def parse(self, response):
        details = self.product_details(response)
        garment = self.new_unique_garment(details['sku'])
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['brand'] = self.product_brand(details)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(details)

        if len(response.css(".variant-group:not(.hidden)")) == 2:
            requests = self.size_requests(response)
            garment['meta'] = {'requests_queue': requests}
        else:
            garment['skus'] = self.skus(response)

        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'] = garment.get('skus', {})
        garment['skus'].update(self.jeans_skus(response))
        return self.next_request_or_garment(garment)

    def product_details(self, response):
        product_text = clean(response.css('[type="application/ld+json"]::text'))[0]
        return json.loads(product_text)['@graph'][0]

    def product_brand(self, detail):
        return clean(detail['brand']['name']) if not isinstance(detail, Response) else None

    def product_name(self, response):
        return clean(response.css('.section-title::text'))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumb a>span::text'))[1:]

    def product_gender(self, response):
        gender_css = '.panel-body img::attr(src)'
        soup = " ".join(clean(response.css(gender_css))).lower()
        for gender_string, gender in self.GENDER_MAP:
            if gender_string in soup:
                return gender
        return 'unisex-adults'

    def product_colour(self, response):
        description = self.product_description(response)
        table_tokens = clean(response.css('.table-striped ::text'))
        detected_from_table = clean(" ".join([self.detect_colour(x) for x in table_tokens]))
        detected_from_description = clean(" ".join([self.detect_colour(x) for x in description]))
        return detected_from_table or detected_from_description

    def jeans_skus(self, response):
        waist = response.meta['waist']
        common_sku = response.meta['common_sku']
        raw_sub_skus = json.loads(response.body)
        css_selector = Selector(text=raw_sub_skus['html'])

        sizes_s = css_selector.css('.variant-filter-item')
        skus = {
            f'{waist}_{clean(size_s.css("::text"))[0]}': self.make_sku(size_s, common_sku)
            for size_s in sizes_s
        }

        return skus

    def skus(self, response):
        common_sku = self.common_sku(response)

        sizes_s = response.css('.variant-filter-item')
        skus = {
            f'{clean(size_s.css("::text"))[0]}': self.make_sku(size_s, common_sku)
            for size_s in sizes_s
        }

        return skus

    def image_urls(self, details):
        return details["image"] if isinstance(details["image"], list) else [details["image"]]

    def size_requests(self, response):
        api_endpoint = 'https://www.wearegarcia.com/nl_NL/xhr/product/get_filter_attributes/'
        url = api_endpoint + response.url.split('/')[-2]
        headers = {"Content-Type": "application/json"}
        params = {"attribute": "19"}
        meta = {'common_sku': self.common_sku(response)}
        requests = []

        sizes_s = response.css('[data-attribute="19"]>.variant-filter-item:not([class*="disabled"])')
        for size_s in sizes_s:
            params["filters"] = {"19": int(clean(size_s.css('::attr(data-value)'))[0])}
            meta['waist'] = clean(size_s.css('::text'))[0]
            request = FormRequest(url=url, method='POST', meta=meta, body=json.dumps(params),
                                  headers=headers, callback=self.parse_size, dont_filter=True)
            requests.append(request)

        return requests

    def common_sku(self, response):
        colour = self.product_colour(response)
        common_sku = self.product_pricing_common(response)

        if colour:
            common_sku['colour'] = colour

        return common_sku

    def make_sku(self, size_sel, common_sku):
        sku = common_sku.copy()
        sku['size'] = clean(size_sel.css('::text'))[0]

        if size_sel.css('[class*="disabled"]'):
            sku['out_of_stock'] = True

        return sku


class GraciaCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    listings_css = ['.list-unstyled', '.pagination']
    products_css = ['.product']
    parse_spider = GraciaParseSpider()

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
