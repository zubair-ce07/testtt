import re
import json
from urllib.parse import urlencode, urljoin

from scrapy import Request, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from whiteStuff import items


class WhiteStuffSpider(CrawlSpider):
    DOWNLOAD_DELAY = 1
    name = 'white_stuff'
    start_urls = ['https://www.whitestuff.com/global']
    rules = (Rule(LinkExtractor(restrict_css='.navbar__item', allow='.*(mens|kids|gift).*/.+'),
                  callback='parse_find_category'),)

    skus_request_url = "https://www.whitestuff.com/global/action/GetProductData-FormatProduct?"
    category_page_request_url = 'https://fsm.attraqt.com/zones-js.aspx?'
    currency = ''
    genders = {"womens": "female", "mens": "male", "boys": "boy", "girls": "girl"}
    category_page_request_parameters = {
        'siteId': 'c7439161-d4f1-4370-939b-ef33f4c876cc',
        'pageurl': '',
        'zone0': 'banner',
        'zone1': 'category',
        'facetmode': 'data',
        'mergehash': 'true',
        'config_category': '',
    }
    skus_request_parameters = {"Format": "JSON", "ReturnVariable": "true"}

    def parse_find_category(self, response):
        try:
            config_category = re.findall(r"category\s?\=\s?\"(.*)\";", response.css('script::text').extract()[-1])[0]
        except:
            return
        category_page_request_parameters = self.category_page_request_parameters.copy()
        category_page_request_parameters['config_category'] = config_category
        category_page_request_parameters['pageurl'] = response.url
        category_page_request = Request(
            url=f'{self.category_page_request_url}{urlencode(category_page_request_parameters)}',
            callback=self.parse_category_page)
        category_page_request.meta['url'] = response.url
        category_page_request.meta['config_category'] = config_category
        yield category_page_request

    def parse_category_page(self, response):
        category_page_url = response.meta.get('url')
        category = response.meta.get('config_category')
        try:
            response = response.text.replace(r'\"', '"')
            html_response = re.findall("html\":\"(.*>)", response)[-1]
        except:
            return
        selector = Selector(text=html_response)
        product_urls = [urljoin(category_page_url, url) for url in
                        selector.css('.product-tile__title a::attr(href)').extract()]
        for url in product_urls:
            yield Request(url=url, callback=self.parse_item)
        total_pages = int(selector.css('#TotalPages::attr(value)').extract_first() or '1')
        if total_pages > 1 and category_page_url:
            self.handle_pagination(total_pages, category_page_url, category)

    def handle_pagination(self, total_pages, url, category):
        category_page_request_parameters = self.category_page_request_parameters.copy()
        category_page_request_parameters['config_category'] = category
        for page_no in range(2, total_pages):
            next_url = url + f'/#esp_pg={page_no}'
            category_page_request_parameters['pageurl'] = next_url
            yield Request(url=f'{self.category_page_request_url}{urlencode(category_page_request_parameters)}',
                          callback=self.parse_category_page)

    def parse_item(self, response):
        item = items.WhiteStuffItem()
        item['name'] = self.get_title(response)
        item['retailer_sku'] = self.get_retailer_sku(response)
        item['gender'] = self.get_gender(response)
        item['brand'] = 'White Stuff'
        item['categories'] = self.get_categories(response)
        item['url'] = self.get_url(response)
        item['description'], item['care'] = self.get_description_and_care(response)
        self.currency = self.get_currency(response)
        raw_skus_request_url = self.make_skus_request_url(response)
        request = Request(url=raw_skus_request_url, callback=self.parse_skus)
        request.meta['item'] = item
        yield request

    def parse_skus(self, response):
        item = response.meta['item']
        json_response = json.loads(re.sub('\\\\\'', "",
                                          re.sub('\s//.*\n', "",
                                                 re.findall('(?<=\=)(.*?)(?=;)', response.text, flags=re.S)[0])))
        raw_skus = json_response['productVariations']
        image_urls = set()
        for raw_sku in raw_skus.values():
            sku_image_urls = [image['src'] for image in raw_sku['images'] if image['size'] == "ORI"]
            image_urls = image_urls.union(sku_image_urls)
        item['image_urls'] = image_urls
        item['skus'] = self.get_skus(raw_skus)
        return item

    def get_skus(self, raw_skus):
        skus = []
        sku_common = {'currency': self.currency}
        for raw_sku in raw_skus.values():
            sku = sku_common.copy()
            sku['sku_id'] = raw_sku['productUUID']
            sku['in_stock'] = raw_sku['inStock']
            sku['colour'] = raw_sku['colour']
            sku['size'] = raw_sku['size']
            sku['price'] = self.format_price(raw_sku['salePrice'])
            if self.format_price(raw_sku['salePrice']) < self.format_price(raw_sku['listPrice']):
                sku['old-price'] = self.format_price(raw_sku['listPrice'])
            skus.append(sku)
        return skus

    def make_skus_request_url(self, response):
        sku_id = response.css('.js-variation-attribute::attr(data-variation-master-sku)').extract_first()
        self.skus_request_parameters["ProductID"] = sku_id
        return f'{self.skus_request_url}{urlencode(self.skus_request_parameters)}'

    @staticmethod
    def format_price(price):
        price = price.translate(str.maketrans({u"\u20ac": ''}))
        return int(float(price) * 100)

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

    @staticmethod
    def get_description_and_care(response):
        types = response.css('.ish-productAttributes .ish-ca-type::text').extract()
        values = response.css('.ish-productAttributes .ish-ca-value::text').extract()
        description_care = list(zip(types, values))
        care = []
        description = []
        for line in description_care:
            line = f'{line[0]} {line[1]}'
            if 'Care' in line:
                care.append(line)
            else:
                description.append(line)
        return description, care

    @staticmethod
    def get_url(response):
        return response.url

    @staticmethod
    def get_currency(response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()
