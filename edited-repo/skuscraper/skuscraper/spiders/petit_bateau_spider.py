import re
import json
from urllib.parse import urljoin

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest

from .base import BaseCrawlSpider, BaseParseSpider

class Mixin:
    market = 'UK'
    retailer = 'petit_bateau'
    allowed_domains = ['petit-bateau.co.uk']
    start_urls = ['https://www.petit-bateau.co.uk/']


class PetitBateauParseSpider(BaseParseSpider, Mixin):
    name = f"{Mixin.retailer}-parse"

    description_css = '[itemprop="description"] ::text'
    care_css = '.maintenance-guide .tooltip ::text'

    request_url = 'https://www.petit-bateau.co.uk/WebServices/CatalogService.asmx/GetVariant'
    payload = '{{"productId": "{}","variantId":"{}", "selectedSize":"{}"}}'
    headers = {'content-type': 'application/json; charset=UTF-8'}
    image_source = None

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)
        if not garment:
            return
        
        response.meta['gender'] = self.detect_gender(self.product_name(response))
        self. boilerplate_normal(garment, response)

        self.image_source = self.image_data_source(response)
        garment['skus'] = {}
        garment['image_urls'] = []
        garment['meta'] = {'colour_requests': self.colour_requests(response)}
        return self.next_colour_request_or_sizes(garment)

    def parse_colours(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        self.skus_requests(response, garment)
        colour_request = self.next_colour_request_or_sizes(garment)

        if colour_request:
            return colour_request

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        current_variant = json.loads(response.text)['d']['CurrentVariant']

        money_strs = [current_variant['DisplayPrice'], current_variant['PrivilegePrice']]
        sku = self.product_pricing_common(response=None, money_strs=money_strs).copy()
        sku['size'] = current_variant['Size']

        if current_variant['OutOfStock']:
            sku['out_of_stock'] = current_variant['OutOfStock']

        garment['skus'][current_variant['CurrentVariantIdWithoutCatalogName']] = sku

        return self.next_request_or_garment(garment)

    def request_payloads(self, url):
        pattern = r"\d+.*?\)"
        return self.payload.format(re.findall(pattern, url, re.M)[0],
                                   re.findall(pattern, url, re.M)[1], "")

    def colour_requests(self, response):
        colour_requests = []
        for url in self.colour_urls(response):
            request_body = self.request_payloads(url)
            request = FormRequest(url=self.request_url, callback=self.parse_colours,
                                  method="POST", headers=self.headers,
                                  body=request_body)
            colour_requests.append(request)

        return colour_requests

    @staticmethod
    def next_colour_request_or_sizes(garment):
        if 'meta' not in garment:
            return

        if garment['meta']['colour_requests']:
            request = garment['meta']['colour_requests'].pop()
            request.meta.setdefault('garment', garment)
            return request

    def image_urls(self, response):
        image_urls = []
        current_variant = json.loads(response.text)['d']['CurrentVariant']
        for image in current_variant:

            if "Image" not in image:
                continue

            image_url = urljoin(self.image_source, current_variant[image])
            image_urls.append(image_url)

        return image_urls

    def skus_requests(self, response, garment):
        sku_deatils = json.loads(response.text)['d']
        sizes = [size['Libelle'] for size in sku_deatils['ListingSizes']]
        product_id = sku_deatils['CurrentVariant']['ProductID']
        variant_id = sku_deatils['CurrentVariant']['ID']

        requests_queue = garment['meta'].get('requests_queue', [])
        requests_queue += self.skus_request(sizes, product_id, variant_id)
        garment['meta']['requests_queue'] = requests_queue

    def skus_request(self, sizes, product_id, variant_id):
        skus_request = []
        for size in sizes:
            request_body = self.payload.format(product_id, variant_id, size)
            request = FormRequest(url=self.request_url, callback=self.parse_skus,
                                  method="POST", headers=self.headers,
                                  body=request_body)
            skus_request.append(request)

        return skus_request

    @staticmethod
    def product_id(response):
        css = '::attr(data-productid)'
        return response.css(css).extract_first()

    @staticmethod
    def product_name(response):
        css = '.title-product ::text'
        return response.css(css).extract_first()

    def product_category(self, response):
        css = '.breadcrum a:nth-child(n+2) ::text'
        return response.css(css).extract()

    @staticmethod
    def colour_urls(response):
        css = '.list-colors ::attr(data-actionurl)'
        return response.css(css).extract()

    @staticmethod
    def image_data_source(response):
        css = '.visu-mobile ::attr(data-src)'
        return response.css(css).extract_first()


class PetitBateauCrawlSpider(BaseCrawlSpider, Mixin):
    name = f"{Mixin.retailer}-crawl"
    parse_spider = PetitBateauParseSpider()

    absolute_url = 'https://www.petit-bateau.co.uk{}'
    request_url = 'https://www.petit-bateau.co.uk/WebServices/MerchService.asmx/Listing'
    payload = '{{"refiningId":"{}","category":"{}","allowVp":false,"filters":null}}'
    headers = {'content-type': 'application/json; charset=UTF-8'}

    listing_css = [
        '.link-nav-univers-content'
    ]

    product_css = [
        '.product-page-link'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_request_items'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
        )

    def parse_request_items(self, response):
        category = self.payload_category(response)
        refining_id = self.payload_refining_id(response)

        if category and refining_id:
            return self.request_lisitng(category, refining_id)

    def parse_listings(self, response):
        links = response.meta['links']
        listing = json.loads(response.text)['d']

        for item in listing['Items']:
            links.append(Request(url=self.absolute_url.format(item['Url']),
                                 callback=self.parse_item))

        next_refining_id = listing['Pager']['NextPage']
        if next_refining_id:
            category = listing['Infos']['Id']
            return self.request_lisitng(category, next_refining_id, links)

        return self.process_links(links)

    def request_lisitng(self, category, refining_id, links=[]):
        request_body = self.payload.format(refining_id, category)
        request = FormRequest(url=self.request_url, callback=self.parse_listings,
                              method="POST", headers=self.headers,
                              body=request_body)
        request.meta['links'] = links
        return request

    @staticmethod
    def payload_category(response):
        css = '::attr(data-categoryid)'
        return response.css(css).extract_first()

    @staticmethod
    def payload_refining_id(response):
        css = '.slider ::attr(data-refiningid)'
        return response.css(css).extract_first()
