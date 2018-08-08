import re
import json
from urllib.parse import urlencode, urljoin, urlparse, parse_qs

from scrapy import Request, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from whiteStuff import items


class WhiteStuffSpider(CrawlSpider):
    DOWNLOAD_DELAY = 1
    name = 'white_stuff'
    start_urls = ['https://www.whitestuff.com/global']
    rules = (Rule(LinkExtractor(restrict_css='.navbar__item', allow='.*(mens|kids|gift).*/.+'),
                  callback='parse_category_name'),)

    skus_url_t = "https://www.whitestuff.com/global/action/GetProductData-FormatProduct?"
    category_url_t = 'https://fsm.attraqt.com/zones-js.aspx?'
    genders = {"womens": "female",
               "mens": "male",
               "boys": "boy",
               "girls": "girl"}
    category_parameters = {
        'siteId': 'c7439161-d4f1-4370-939b-ef33f4c876cc',
        'zone0': 'banner',
        'zone1': 'category',
        'facetmode': 'data',
        'mergehash': 'true',
    }
    skus_parameters = {"Format": "JSON", "ReturnVariable": "true"}

    def parse_category_name(self, response):
        script = self.get_category_script(response)
        config_category = re.findall(r"category\s?\=\s?\"(.*)\";", script)[0] or ''
        config_category_tree = re.findall(r"tree\s?\=\s?\"(.*)\";", script)[0] or ''
        if not config_category:
            return
        category_parameters = self.category_parameters.copy()
        category_parameters['config_category'] = config_category
        category_parameters['config_categorytree'] = config_category_tree
        category_parameters['pageurl'] = response.url
        yield Request(url=f'{self.category_url_t}{urlencode(category_parameters)}', callback=self.parse_category)

    def parse_category(self, response):
        query_string = urlparse(response.url).query
        parsed_query_string = parse_qs(query_string)
        page_url = parsed_query_string['pageurl'][0]
        html_response = self.extract_html_from_response(response)
        if not html_response:
            return
        selector = Selector(text=html_response)
        for request in self.get_item_requests(selector, page_url):
            yield request
        return self.get_pagination_requests(response)

    def get_item_requests(self, selector, page_url):
        css = '.product-tile__title a::attr(href)'
        return [Request(url=urljoin(page_url, url), callback=self.parse_item) for url in selector.css(css).extract()]

    def get_pagination_requests(self, response):
        query_string = urlparse(response.url).query
        parsed_query_string = parse_qs(query_string)
        url = parsed_query_string['pageurl'][0]
        if 'esp_pg' in url:
            return
        category = parsed_query_string['config_category'][0]
        category_tree = parsed_query_string['config_categorytree'][0]

        html_response = self.extract_html_from_response(response)
        selector = Selector(text=html_response)
        total_pages = int(selector.css('#TotalPages::attr(value)').extract_first() or '1')

        if total_pages <= 1:
            return
        category_parameters = self.category_parameters.copy()
        category_parameters['config_category'] = category
        category_parameters['config_categorytree'] = category_tree
        for page_no in range(2, total_pages):
            next_url = urljoin(url, f'/#esp_pg={page_no}')
            category_parameters['pageurl'] = next_url
            yield Request(url=f'{self.category_url_t}{urlencode(category_parameters)}', callback=self.parse_category)

    def parse_item(self, response):
        item = items.WhiteStuffItem()
        item['name'] = self.get_title(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['gender'] = self.get_gender(response)
        item['brand'] = 'White Stuff'
        item['categories'] = self.get_categories(response)
        item['url'] = response.url
        item['description'] = self.get_description(response)
        item['care'] = self.get_care(response)
        skus_request = self.make_skus_request(response)
        skus_request.meta['item'] = item
        skus_request.meta['currency'] = self.get_currency(response)
        yield skus_request

    def parse_skus(self, response):
        item = response.meta['item']
        currency = response.meta['currency']
        raw_skus = self.get_raw_skus(response)
        item['image_urls'] = self.get_image_urls(raw_skus)
        item['skus'] = self.get_skus(raw_skus, currency)
        return item

    @staticmethod
    def get_raw_skus(response):
        response = re.findall('(?<=\=)(.*?)(?=;)', response.text, flags=re.S)[0]
        response = re.sub('\s//.*\n', "", response)
        response = re.sub('\\\\\'', "", response)
        raw_skus = json.loads(response)
        return raw_skus['productVariations']

    @staticmethod
    def get_category_script(response):
        scripts = response.css('script::text').extract()
        for script in scripts:
            if 'attraqt.config.category' in script:
                return script

    @staticmethod
    def get_image_urls(raw_skus):
        image_urls = set()
        for raw_sku in raw_skus.values():
            sku_image_urls = [image['src'] for image in raw_sku['images'] if image['size'] == "ORI"]
            image_urls = image_urls.union(sku_image_urls)
        return image_urls

    def get_skus(self, raw_skus, currency):
        skus = []
        sku_common = dict()
        for raw_sku in raw_skus.values():
            sku = sku_common.copy()
            pricing = self.get_pricing(raw_sku, currency)
            sku['sku_id'] = raw_sku['productUUID']
            sku['in_stock'] = raw_sku['inStock']
            sku['colour'] = raw_sku['colour']
            sku['size'] = raw_sku['size']
            sku['price'] = pricing['price']
            sku['old-price'] = pricing['old-price']
            sku['currency'] = pricing['currency']
            skus.append(sku)
        return skus

    def get_pricing(self, raw_sku, currency):
        pricing = dict()
        pricing['price'] = self.format_price(raw_sku['salePrice'])
        if self.format_price(raw_sku['salePrice']) < self.format_price(raw_sku['listPrice']):
            pricing['old-price'] = self.format_price(raw_sku['listPrice'])
        else:
            pricing['old-price'] = []
        pricing['currency'] = currency
        return pricing

    def make_skus_request(self, response):
        sku_id = response.css('.js-variation-attribute::attr(data-variation-master-sku)').extract_first()
        self.skus_parameters["ProductID"] = sku_id
        skus_request_url = f'{self.skus_url_t}{urlencode(self.skus_parameters)}'
        return Request(url=skus_request_url, callback=self.parse_skus)

    @staticmethod
    def extract_html_from_response(response):
        # json.loads(re.findall(r"LM.buildZone\((.+)\)", html_response)[1])
        # (JSONDecodeError)Expecting ',' delimiter: line 1 column 113 (char 112)
        html_response = response.text.replace(r'\"', '"')
        return re.findall("html\":\"(.*>)", html_response)[-1]

    @staticmethod
    def format_price(price):
        prices = re.findall(r"\D*(\d+)\D*", price)
        price = prices[0] + prices[1] or '00'
        return int(price)

    @staticmethod
    def get_title(response):
        return response.css('.product-info__heading::text').extract_first()

    @staticmethod
    def get_retailer_sku(response):
        return response.css('[itemprop="sku"]::text').extract_first()

    @staticmethod
    def get_categories(response):
        return response.css('.breadcrumb-list__item-link::text').extract()[1:]

    def get_gender(self, response):
        for gender in self.genders.keys():
            if gender in response.url:
                return self.genders.get(gender)

    def get_description(self, response):
        return [line for line in self.get_raw_description(response) if 'Care' not in line]

    def get_care(self, response):
        return [line for line in self.get_raw_description(response) if 'Care' in line]

    @staticmethod
    def get_raw_description(response):
        types = response.css('.ish-productAttributes .ish-ca-type::text').extract()
        values = response.css('.ish-productAttributes .ish-ca-value::text').extract()
        raw_description = list(zip(types, values))
        return [f'{line[0]} {line[1]}' for line in raw_description]

    @staticmethod
    def get_currency(response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()
