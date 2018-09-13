import json
from urllib.parse import urlencode

from scrapy import FormRequest
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, LinkExtractor, BaseParseSpider, clean, Gender


class Mixin:
    retailer = 'lindex-uk'
    allowed_domains = ['lindex.com']
    market = 'UK'
    start_urls = ['https://www.lindex.com/uk/']


class LindexParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    brand_css = '#ProductPage>[data-style]::attr(data-product-brand)'
    description_css = '.description ::text'
    care_css = '.more_info ::text'
    color_request_url = 'https://www.lindex.com/WebServices/ProductService.asmx/GetProductData'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_retailer_sku(response))
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = []
        garment['skus'] = {}
        requests = self.color_requests(response)
        garment['meta'] = {'requests_queue': requests}
        if self.product_status(response) == 'Coming soon':
            garment['merch_info'] = ['coming soon']
        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        raw_skus = json.loads(response.body)
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(raw_skus)
        garment['skus'].update(self.skus(raw_skus))

        return self.next_request_or_garment(garment)

    def image_urls(self, raw_skus):
        return [image["Standard"] for image in raw_skus["d"]["Images"]]

    def skus(self, raw_skus):
        skus = {}
        common_sku = self.common_sku(raw_skus)
        raw_sizes = [size['Text'] for size in raw_skus['d']['SizeInfo'][1:]]

        for raw_size in raw_sizes:
            sku = common_sku.copy()

            if 'out of stock' in raw_size:
                sku['out_of_stock'] = True
                sku['size'] = raw_size[:raw_size.find('-')]
            else:
                sku['size'] = raw_size[:raw_size.find('(')] if raw_size.find('(') != -1 else raw_size

            if sku['size'] == '0':
                sku['size'] = self.one_size

            skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        return skus

    def common_sku(self, raw_skus):
        money_strs = [raw_skus['d']['Price'], raw_skus['d']['NormalPrice']]
        common_sku = self.product_pricing_common(response=None, money_strs=money_strs)
        common_sku['colour'] = self.product_colour(raw_skus)
        return common_sku

    def color_requests(self, response):
        color_ids = clean(response.css('.product .colors [data-colorid]::attr(data-colorid)'))
        headers = {"Content-Type": "application/json"}
        params = {
            "productIdentifier": self.product_retailer_sku(response),
            "isMainProductCard": True,
            "nodeId": clean(response.css('#ProductPage::attr(data-pageid)'))[0],
            "primaryImageType": 0
        }

        requests = []
        for color_id in color_ids:
            params["colorId"] = color_id
            request = FormRequest(url=self.color_request_url, method="POST", body=json.dumps(params),
                                  headers=headers, callback=self.parse_color)
            requests.append(request)

        return requests

    def product_retailer_sku(self, response):
        return clean(response.css('.product_placeholder::attr(data-product-identifier)'))[0]

    def product_name(self, response):
        return clean(response.css('.name::text'))[0]

    def product_category(self, response):
        category_css = '#ProductPage>[data-style]::attr(data-product-category)'
        return clean(clean(response.css(category_css))[0].split('/'))

    def product_gender(self, response):
        return self.gender_lookup(response.url) or Gender.WOMEN.value

    def product_colour(self, raw_skus):
        return raw_skus['d']['Color']

    def product_status(self, response):
        return clean(response.css('.product .status::text'))[0]


class LindexCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    listing_css = ['.mainMenu']
    product_css = ['.info .productCardLink']
    parse_spider = LindexParseSpider()
    page_request_url = 'https://www.lindex.com/uk/SiteV3/Category/GetProductGridPage?{}'
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'),
    )

    def parse(self, response):
        for i, request in enumerate(super(LindexCrawlSpider, self).parse(response)):
            request.meta['cookiejar'] = i
            yield request

    def parse_pagination(self, response):
        no_of_pages = clean(response.css('.gridPages::attr(data-page-count)'))
        if no_of_pages:
            params = {
                'nodeId': clean(response.css('body::attr(data-page-id)'))[0],
                'pageIndex': 0
            }
            for page_no in range(1, int(no_of_pages[0])):
                params['pageIndex'] = page_no
                request = response.follow(url=self.page_request_url.format(urlencode(params)),
                                          meta=response.meta, callback=self.parse_pages)

                request.meta['trail'] = self.add_trail(response)
                for meta in ('gender', 'category', 'industry', 'outlet', 'brand'):
                    request.meta[meta] = request.meta.get(meta) or response.meta.get(meta)

                yield self.elevate_request_priority(request)

        yield from self.parse(response)

    def parse_pages(self, response):
        yield from super(LindexCrawlSpider, self).parse(response)
