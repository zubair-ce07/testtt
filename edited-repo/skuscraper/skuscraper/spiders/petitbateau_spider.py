import re
import json
from urllib.parse import urljoin

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest

from .base import BaseCrawlSpider, BaseParseSpider, clean

class Mixin:
    market = 'UK'
    retailer = 'petitbateau'
    allowed_domains = ['petit-bateau.co.uk']
    start_urls = ['https://www.petit-bateau.co.uk/e-shop/bf-24/1/our-basics.html?refiningId=page%3D2%26nbResultsPerPage%3D18%26sorting%3DMY_SELECTION%26constraints%3Dzone%3AUK_%2F_category%3Abf-24']


class PetitBateauParseSpider(BaseParseSpider, Mixin):
    name = f"{Mixin.retailer}-parse"

    description_css = '[itemprop="description"] ::text'
    care_css = '.maintenance-guide .tooltip ::text'

    variant_url = 'https://www.petit-bateau.co.uk/WebServices/CatalogService.asmx/GetVariant'
    variant_payload_t = '{{"productId": "{}","variantId":"{}", "selectedSize":"{}"}}'
    headers = {'content-type': 'application/json; charset=UTF-8'}

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)

        if not garment:
            return
        
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.gender_lookup(self.product_name(response))
        garment['skus'] = {}
        garment['image_urls'] = []

        garment['meta'] = {'requests_queue' : self.colour_requests(response)}
        # garment['meta']['requests_queue'] += self.colour_requests(response)

        return self.next_request_or_garment(garment)

    def parse_colours(self, response):
        print("\033[92m-------------=-=-KSYS-=-=---------------------\033[0m")

        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['meta']['requests_queue'] += self.size_requests(response)

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        skus = self.skus(response)
        # print(skus)
        garment['skus'].update(self.skus(response))
        # garment['skus'][raw_product['CurrentVariantIdWithoutCatalogName']] = self.skus(raw_product)

        return self.next_request_or_garment(garment)

    def skus(self, response):
        raw_product = json.loads(response.text)['d']['CurrentVariant']
        money_strs = [raw_product['DisplayPrice'], raw_product['PrivilegePrice']]
        skus = {}
        sku = self.product_pricing_common(response=None, money_strs=money_strs)
        sku['size'] = raw_product['Size']

        if raw_product['OutOfStock']:
            sku['out_of_stock'] = raw_product['OutOfStock']

        skus[raw_product['CurrentVariantIdWithoutCatalogName']] = sku
        return skus

    def request_payloads(self, url):
        pattern = r"\d+.*?\)"
        ids = re.findall(pattern, url, re.M)[:2]
        return self.variant_payload_t.format(*ids, "")

    def colour_requests(self, response):
        # print("\033[92m-------------=-=-KSYS-=-=---------------------\033[0m")

        colour_requests = []
        image_source = self.image_data_source(response)

        for url in self.colour_urls(response):
            request_body = self.request_payloads(url)
            request = FormRequest(url=self.variant_url, callback=self.parse_colours,
                                  method="POST", headers=self.headers, body=request_body)
            request.meta['image_source'] = image_source
            colour_requests.append(request)

        return colour_requests

    def image_urls(self, response):
        image_urls = []
        raw_product = json.loads(response.text)['d']['CurrentVariant']

        for image in raw_product:
            if "Image" not in image:
                continue
            image_url = urljoin(response.meta['image_source'], raw_product[image])
            image_urls.append(image_url)

        return image_urls

    def size_requests(self, response):
        raw_skus = json.loads(response.text)['d']
        product_id = raw_skus['CurrentVariant']['ProductID']
        variant_id = raw_skus['CurrentVariant']['ID']
        sizes = [size['Libelle'] for size in raw_skus['ListingSizes']]
        size_requests = []

        for size in sizes:
            request_body = self.variant_payload_t.format(product_id, variant_id, size)
            request = FormRequest(url=self.variant_url, callback=self.parse_skus,
                                  method="POST", headers=self.headers, body=request_body,
                                  dont_filter=True)
            size_requests.append(request)

        return size_requests

    @staticmethod
    def product_id(response):
        css = '::attr(data-productid)'
        return clean(response.css(css))[0]

    @staticmethod
    def product_name(response):
        css = '.title-product ::text'
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = '.breadcrum a:nth-child(n+2) ::text'
        return clean(response.css(css))

    @staticmethod
    def colour_urls(response):
        css = '.list-colors ::attr(data-actionurl)'
        return clean(response.css(css))

    @staticmethod
    def image_data_source(response):
        css = '.visu-mobile ::attr(data-src)'
        return clean(response.css(css))[0]


class PetitBateauCrawlSpider(BaseCrawlSpider, Mixin):
    name = f"{Mixin.retailer}-crawl"
    parse_spider = PetitBateauParseSpider()

    main_url_t = 'https://www.petit-bateau.co.uk{}'
    listing_url = 'https://www.petit-bateau.co.uk/WebServices/MerchService.asmx/Listing'
    listing_payload_t = '{{"refiningId":"{}","category":"{}","allowVp":false,"filters":null}}'
    headers = {'content-type': 'application/json; charset=UTF-8'}

    listing_css = [
        '.link-nav-univers-content'
    ]

    product_css = [
        '.product-page-link'
    ]

    rules = (
        # Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
        )

    # def parse(self, response):
    #     yield from super().parse(response)
    #
    #     category = clean(response.css('::attr(data-categoryid)'))
    #     refining_id = clean(response.css('.slider ::attr(data-refiningid)'))
    #
    #     if category and refining_id:
    #         yield self.request_listing(category[0], refining_id[0])
    #
    # def parse_listings(self, response):
    #     links = response.meta['links']
    #     listing = json.loads(response.text)['d']
    #
    #     links += [Request(url=self.main_url_t.format(item['Url']), callback=self.parse_item)
    #              for item in listing['Items']]
    #
    #     next_refining_id = listing['Pager']['NextPage']
    #
    #     if next_refining_id:
    #         category = listing['Infos']['Id']
    #         return  self.request_listing(category, next_refining_id, links)
    #
    #     return self.process_links(links)
    #
    # def request_listing(self, category, refining_id, links=[]):
    #     request_body = self.listing_payload_t.format(refining_id, category)
    #     request = FormRequest(url=self.listing_url, callback=self.parse_listings,
    #                           method="POST", headers=self.headers,
    #                           body=request_body)
    #     request.meta['links'] = links
    #     return request

