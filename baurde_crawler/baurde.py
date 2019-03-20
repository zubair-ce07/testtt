import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from baurde_crawler.items import BaurdeCrawlerItem


class BaurdeCrawler(CrawlSpider):

    GENDER_MAP = {
        'dam': 'men',
        'men': 'men',
        'boy': 'boy',
        'girl': 'girl',
        'jungen': 'boy',
        'herren': 'men',
        'herr': 'women',
        'women': 'women',
        'damen': 'women',
        'mädchen': 'girl',
        'kid': 'unisex-kids',
        'barn': 'unisex-kids',
        'kinder': 'unisex-kids',
    }

    name = 'baur-de-crawl'
    allowed_domains = ['baur.de']
    start_urls = ['https://www.baur.de/']

    listings_css = ['#nav-main-list']
    products_css = ['.plp-area1']

    rules = (Rule(LinkExtractor(restrict_css=listings_css), callback='parse_category'),
             Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'))

    product_url_t = 'https://www.baur.de/p/{}'
    category_url = 'https://www.baur.de/suche/mba/magellan'

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://www.baur.de',
        'content-type': 'application/json; charset=UTF-8'}

    formdata = {
        'start': 0,
        'clientId': 'BaurDe',
        'version': 44,
        'channel': 'web',
        'locale': 'de_DE',
        'count': 72,
        'personalization': '$$-2$$web$'}

    def parse_category(self, response):
        category_r = 'CatalogCategoryID=(.*?)&'
        css = '.layernavi-loading-cont ::attr(data-pagelet-url)'

        formdata = self.formdata.copy()
        for category in response.css(css).extract():
            formdata['category'] = re.findall(category_r, str(category))[0]

            yield Request(url=self.category_url, callback=self.parse_pagination, headers=self.headers,
                          meta={'formdata': formdata}, body=json.dumps(formdata), method='POST')

    def parse_pagination(self, response):
        page_size = 72
        formdata = response.meta['formdata']
        raw_product = json.loads(response.text)
        products = raw_product['searchresult']['result']['count']

        for product in raw_product['searchresult']['result']['styles']:
            yield Request(url=self.product_url_t.format(product['masterSku']), callback=self.parse_product)

        if 'Page=P' not in response.url and products > page_size:
            for page, per_page_products in enumerate(range(0, int(products), page_size), start=1):
                yield Request(url=add_or_replace_parameter(self.category_url, 'Page', 'P'+str(page)),
                              callback=self.parse_pagination, headers=self.headers, meta={'formdata': formdata},
                              body=json.dumps(formdata), method='POST')

    def parse_product(self, response):
        item = BaurdeCrawlerItem()
        raw_product = self.raw_product(response)

        item['lang'] = 'de'
        item['market'] = 'DE'
        item['skus'] = self.skus(raw_product)
        item['url'] = self.product_url(response)
        item['name'] = self.product_name(raw_product)
        item['brand'] = self.product_brand(raw_product)
        item['category'] = self.product_category(response)
        item['image_urls'] = self.product_image_urls(response)
        item['gender'] = self.product_gender(response, raw_product)
        item['description'] = self.product_description(raw_product)
        item['retailer_sku'] = self.product_retailer_sku(raw_product)

        return item

    def product_url(self, response):
        return response.url

    def product_name(self, raw_product):
        return raw_product['name']

    def product_market(self, raw_product):
        return raw_product['country']

    def product_retailer_sku(self, raw_product):
        return raw_product['sku']

    def product_image_urls(self, response):
        css = '.product-gallery-item > img::attr(src)'
        return response.css(css).extract()

    def product_category(self, response):
        css = 'div.nav-breadcrumb .display-name ::text'
        return [response.css(css).extract()[1]]

    def product_brand(self, raw_product):
        return raw_product.get('brandLinkName') or 'BAUR'

    def product_description(self, raw_product):
        return [raw_product.get('longDescription')] or []

    def raw_product(self, response):
        css = 'script:contains("variations") ::text'
        return json.loads(response.css(css).extract_first())

    def clean(self, raw_text):
        if type(raw_text) is list:
            return [re.sub('(\r*)(\t*)(\n*)', '', i) for i in raw_text]
        return re.sub('(\r*)(\t*)(\n*)', '', raw_text)

    def product_gender(self, response, raw_product):
        css = 'div.nav-breadcrumb .display-name ::text'
        gender_soup = ' '.join([self.product_name(raw_product)] +
                               self.product_description(raw_product) +
                               [response.css(css).extract()[2]] or []).lower()

        for gender_str, gender in self.GENDER_MAP.items():
            if gender_str in gender_soup:
                return gender

        return 'unisex-adults'

    def product_pricing(self, key, raw_sku):
        pricing = {'price': raw_sku[key]['currentPrice']['value']}
        pricing['currency'] = raw_sku[key]['currentPrice']['currency']

        if 'oldPrice' in raw_sku.keys():
            pricing['previous_price'] = raw_sku[key]['oldPrice']['value']

        return pricing

    def skus(self, raw_skus):
        skus = {}

        for key in raw_skus['variations'].keys():
            sku = self.product_pricing(key, raw_skus['variations'])

            if not raw_skus['variations'][key]['productRef']['available']:
                sku['out_of_stock'] = True

            if 'Var_Size' in raw_skus['variations'][key]['variationValues'].keys():
                sku['size'] = raw_skus['variations'][key]['variationValues']['Var_Size']
            else:
                sku['size'] = 'one_size'

            if 'Var_Article' in raw_skus['variations'][key]['variationValues'].keys():
                sku['colour'] = raw_skus['variations'][key]['variationValues']['Var_Article']

            if 'Var_Dimension3' in raw_skus['variations'][key]['variationValues'].keys():
                length = raw_skus['variations'][key]['variationValues']['Var_Dimension3']
                skus[f'{raw_skus["variations"][key]["sku"]}/{length}'] = sku
            else:
                skus[f'{raw_skus["variations"][key]["sku"]}'] = sku

        return skus
