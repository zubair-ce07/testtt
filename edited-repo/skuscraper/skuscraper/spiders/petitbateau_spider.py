import re
import json
from urllib.parse import urljoin

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean, soupify, Gender


class Mixin:
    market = 'UK'
    retailer = 'petitbateau'
    allowed_domains = ['petit-bateau.co.uk']
    start_urls = [
        'https://www.petit-bateau.co.uk'
    ]


class PetitBateauParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    raw_description_css = '[itemprop="description"] ::text'
    care_css = '.maintenance-guide .tooltip ::text'

    variant_url = 'https://www.petit-bateau.co.uk/WebServices/CatalogService.asmx/GetVariant'
    variant_payload_t = '{{"productId": "{}","variantId":"{}", "selectedSize":"{}"}}'
    headers = {'content-type': 'application/json; charset=UTF-8'}

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = {}
        garment['image_urls'] = []
        garment['gender'] = self.product_gender(garment)
        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colours(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['meta']['requests_queue'] += self.size_requests(response)

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = '::attr(data-productid)'
        return clean(response.css(css))[0]

    def product_gender(self, garment):
        gender_soup = soupify([garment['name']] + garment['description']).lower()
        return self.gender_lookup(gender_soup) or Gender.ADULTS.value

    def colour_requests(self, response):
        colour_requests = []
        image_source_url = self.image_source_url(response)

        for url in self.colour_urls(response):
            request_body = self.request_colour_body(url)
            request = FormRequest(url=self.variant_url, callback=self.parse_colours,
                                  method="POST", headers=self.headers, body=request_body)
            request.meta['image_source_url'] = image_source_url
            colour_requests.append(request)

        return colour_requests

    def image_urls(self, response):
        image_urls = []
        raw_product = self.raw_variants(response)['CurrentVariant']
        image_source_url = response.meta['image_source_url']

        for image in raw_product:

            if "Image" not in image:
                continue

            image_url = urljoin(image_source_url, raw_product[image])
            image_urls.append(image_url)

        return image_urls

    def size_requests(self, response):
        raw_variants = self.raw_variants(response)
        product_id = raw_variants['CurrentVariant']['ProductID']
        variant_id = raw_variants['CurrentVariant']['ID']
        sizes = [size['Libelle'] for size in raw_variants['ListingSizes']]
        size_requests = []

        for size in sizes:
            request_body = self.variant_payload_t.format(product_id, variant_id, size)
            request = FormRequest(url=self.variant_url, callback=self.parse_skus,
                                  method="POST", headers=self.headers, body=request_body)
            size_requests.append(request)

        return size_requests

    def skus(self, response):
        raw_product = self.raw_variants(response)['CurrentVariant']
        money_strs = [raw_product['DisplayPrice'], raw_product['PrivilegePrice']]
        skus = {}
        sku = self.product_pricing_common(response=None, money_strs=money_strs)
        sku['size'] = raw_product['Size']

        if raw_product['OutOfStock']:
            sku['out_of_stock'] = raw_product['OutOfStock']

        skus[raw_product['CurrentVariantIdWithoutCatalogName']] = sku
        return skus

    def request_colour_body(self, url):
        pattern = r"\d+.*?\)"
        ids = re.findall(pattern, url, re.M)[:2]
        return self.variant_payload_t.format(*ids, "")

    def product_category(self, response):
        css = '.breadcrum a ::text'
        return clean(response.css(css))[1:]

    def colour_urls(self, response):
        css = '.list-colors ::attr(data-actionurl)'
        return clean(response.css(css))

    def image_source_url(self, response):
        css = '.visu-mobile ::attr(data-src)'
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = '.title-product ::text'
        return clean(response.css(css))[0]

    def raw_variants(self, response):
        return json.loads(response.text)['d']


class PetitBateauCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = PetitBateauParseSpider()

    listing_url = 'https://www.petit-bateau.co.uk/WebServices/MerchService.asmx/Listing'
    request_body_t = '{{"refiningId":"{}","category":"{}","allowVp":false,"filters":null}}'
    headers = {'content-type': 'application/json; charset=UTF-8'}

    listing_css = [
        '.link-nav-univers-content'
    ]

    product_css = [
        '.product-page-link'
    ]

    deny_r = [
        'soft-toys'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_r), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse(self, response):
        yield from super().parse(response)

        category = clean(response.css('::attr(data-categoryid)'))
        refining_id = clean(response.css('.slider ::attr(data-refiningid)'))

        if category and refining_id:
            yield self.pagination_request(response, category[0], refining_id[0])

    def parse_pagination(self, response):
        listing = json.loads(response.text)['d']
        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        for item in listing['Items']:
            url = urljoin(self.start_urls[0], item['Url'])
            yield Request(url=url, callback=self.parse_item, meta=meta.copy())

        next_refining_id = listing['Pager']['NextPage']

        if next_refining_id:
            category = listing['Infos']['Id']
            yield self.pagination_request(response, category, next_refining_id)

    def pagination_request(self, response, category, refining_id):
        request_body = self.request_body_t.format(refining_id, category)
        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        return FormRequest(url=self.listing_url, callback=self.parse_pagination, meta=meta.copy(),
                           method="POST", headers=self.headers, body=request_body)
