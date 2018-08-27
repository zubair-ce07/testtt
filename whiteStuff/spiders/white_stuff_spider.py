import re
import json
from urllib.parse import urlencode, urljoin, urlparse, parse_qs

import js2xml
import js2xml.utils.objects
import js2xml.utils.vars
from scrapy import Request, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from whiteStuff.items import Item


class WhiteStuffSpider(CrawlSpider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }
    name = 'white_stuff'
    allowed_categories = '.*(mens|kids|gift).*/.+'
    navigation_css = '.navbar__item'
    start_urls = ['https://www.whitestuff.com/global']
    rules = (Rule(LinkExtractor(restrict_css=navigation_css, allow=allowed_categories),
                  callback='parse_category_parameters'),)

    skus_url_t = "https://www.whitestuff.com/global/action/GetProductData-FormatProduct?"
    category_url_t = 'https://fsm.attraqt.com/zones-js.aspx?'
    genders = [
        ("womens", "female"),
        ("mens", "male"),
        ("boys", "boy"),
        ("girls", "girl")
    ]
    category_parameters = {
        'siteId': 'c7439161-d4f1-4370-939b-ef33f4c876cc',
        'zone0': 'banner',
        'zone1': 'category',
        'facetmode': 'data',
        'mergehash': 'true',
    }
    skus_parameters = {
        "Format": "JSON",
        "ReturnVariable": "true"
    }

    def parse_category_parameters(self, response):
        script = self.category_script(response)
        parameters = js2xml.utils.vars.get_vars(js2xml.parse(script))
        config_category = parameters.get('attraqt.config.category')

        if not config_category:
            return

        category_parameters = self.category_parameters.copy()
        category_parameters['config_category'] = config_category
        category_parameters['config_categorytree'] = parameters.get('attraqt.config.categorytree')
        category_parameters['pageurl'] = response.url

        yield Request(url=f'{self.category_url_t}{urlencode(category_parameters)}', callback=self.parse_category)

    def parse_category(self, response):
        selector = self.selector_from_response(response)
        request_parameters = self.request_parameters(response)

        yield from self.item_requests(selector, request_parameters['pageurl'])

        return self.pagination_requests(response)

    def item_requests(self, selector, page_url):
        css = '.product-tile__title a::attr(href)'
        return [Request(url=urljoin(page_url, url), callback=self.parse_item) for url in selector.css(css).extract()]

    def pagination_requests(self, response):
        request_parameters = self.request_parameters(response)

        if 'esp_pg' in request_parameters['pageurl']:
            return

        selector = self.selector_from_response(response)
        total_pages = int(selector.css('#TotalPages::attr(value)').extract_first() or '1')

        if total_pages <= 1:
            return

        category_parameters = self.category_parameters.copy()
        category_parameters['config_category'] = request_parameters['category']
        category_parameters['config_categorytree'] = request_parameters['category_tree']

        for page_no in range(2, total_pages):
            next_url = urljoin(request_parameters['pageurl'], f'/#esp_pg={page_no}')
            category_parameters['pageurl'] = next_url
            yield Request(url=f'{self.category_url_t}{urlencode(category_parameters)}', callback=self.parse_category)

    def parse_item(self, response):
        item = Item()

        item['name'] = self.title(response)
        item['retailer_sku'] = self.retailer_sku(response)
        item['gender'] = self.gender(response)
        item['brand'] = 'White Stuff'
        item['categories'] = self.categories(response)
        item['url'] = response.url
        item['description'] = self.description(response)
        item['care'] = self.care(response)
        skus_request = self.make_skus_request(response)
        skus_request.meta['item'] = item
        skus_request.meta['currency'] = self.currency(response)

        yield skus_request

    def parse_skus(self, response):
        item = response.meta['item']
        currency = response.meta['currency']

        raw_skus = self.raw_skus(response)
        item['image_urls'] = self.image_urls(raw_skus)
        item['skus'] = self.skus(raw_skus, currency)

        return item

    @staticmethod
    def request_parameters(response):
        query_string = urlparse(response.url).query
        parsed_query_string = parse_qs(query_string)
        request_parameters = dict()

        request_parameters['pageurl'] = parsed_query_string['pageurl'][0]
        request_parameters['category'] = parsed_query_string['config_category'][0]
        request_parameters['category_tree'] = parsed_query_string['config_categorytree'][0]

        return request_parameters

    @staticmethod
    def raw_skus(response):
        return js2xml.utils.objects.getall(js2xml.parse(response.text), [dict])[0]['productVariations']

    @staticmethod
    def category_script(response):
        return "".join(response.css('script::text').re('.*attraqt.config.category.*'))

    @staticmethod
    def image_urls(raw_skus):
        image_urls = set()

        for raw_sku in raw_skus.values():
            sku_image_urls = [image['src'] for image in raw_sku['images'] if image['size'] == "ORI"]
            image_urls = image_urls.union(sku_image_urls)

        return image_urls

    def skus(self, raw_skus, currency):
        skus = []

        for raw_sku in raw_skus.values():
            sku = dict()
            sku['sku_id'] = raw_sku['productUUID']
            sku['colour'] = raw_sku['colour']
            sku['size'] = raw_sku['size']
            sku.update(self.pricing(raw_sku, currency))

            if not raw_sku['inStock']:
                sku['is_out_of_stock'] = True

            skus.append(sku)

        return skus

    def pricing(self, raw_sku, currency):
        pricing = {'price': self.format_price(raw_sku['salePrice'])}
        pricing['currency'] = currency

        if self.format_price(raw_sku['salePrice']) < self.format_price(raw_sku['listPrice']):
            pricing['previous_prices'] = self.format_price(raw_sku['listPrice'])
        else:
            pricing['previous_prices'] = []

        return pricing

    def make_skus_request(self, response):
        self.skus_parameters["ProductID"] = self.product_id(response)
        skus_request_url = f'{self.skus_url_t}{urlencode(self.skus_parameters)}'
        return Request(url=skus_request_url, callback=self.parse_skus)

    @staticmethod
    def selector_from_response(response):
        html = json.loads(re.findall(r"LM.buildZone\((.+)\)", response.text)[1])['html']
        return Selector(text=html)

    @staticmethod
    def product_id(response):
        return response.css('.js-variation-attribute::attr(data-variation-master-sku)').extract_first()

    @staticmethod
    def format_price(price):
        return int(''.join(re.findall(r"(\d+)", price)))

    @staticmethod
    def title(response):
        return response.css('.product-info__heading::text').extract_first()

    @staticmethod
    def retailer_sku(response):
        return response.css('[itemprop="sku"]::text').extract_first()

    @staticmethod
    def categories(response):
        return response.css('.breadcrumb-list__item-link::text').extract()[1:]

    def gender(self, response):
        for gender_token, gender in self.genders:
            if gender_token in response.url:
                return gender

    def description(self, response):
        return [line for line in self.raw_description(response) if 'Care' not in line]

    def care(self, response):
        return [line for line in self.raw_description(response) if 'Care' in line]

    @staticmethod
    def raw_description(response):
        types = response.css('.ish-ca-type::text').extract()
        values = response.css('.ish-ca-value::text').extract()
        return [f'{attribute} {value}' for attribute, value in zip(types, values)]

    @staticmethod
    def currency(response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()
