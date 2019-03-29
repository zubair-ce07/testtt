import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from baur_crawler.items import BaurdeCrawlerItem


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
    products_css = ['.plp-area1 a']

    formdata = {
        'start': 0,
        'clientId': 'BaurDe',
        'version': 44,
        'channel': 'web',
        'locale': 'de_DE',
        'count': 72,
        'personalization': '$$-2$$web$'
    }

    product_url_t = 'https://www.baur.de/p/{}'
    category_url = 'https://www.baur.de/suche/mba/magellan'

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://www.baur.de',
        'content-type': 'application/json; charset=UTF-8'
    }

    rules = (Rule(LinkExtractor(restrict_css=listings_css), callback='parse_category'),)

    def parse_category(self, response):
        formdata = self.formdata.copy()
        category_r = 'CatalogCategoryID=(.*?)&'
        css = '.layernavi-loading-cont ::attr(data-pagelet-url)'

        for category in response.css(css).extract():
            formdata['category'] = re.findall(category_r, str(category))[0]
            yield Request(url=self.category_url, callback=self.parse_pagination, headers=self.headers,
                          meta={'formdata': formdata}, body=json.dumps(formdata), method='POST')

    def parse_pagination(self, response):
        page_size = 72
        formdata = response.meta['formdata']
        raw_product = json.loads(response.text)['searchresult']['result']
        total_pages = int(raw_product['count']/page_size)

        return [Request(url=add_or_replace_parameter(self.category_url, 'Page', f'P{page}'),
                        headers=self.headers, callback=self.parse_listings, body=json.dumps(formdata),
                        meta={'raw_product': raw_product}, method='POST') for page in range(1, total_pages)]

    def parse_listings(self, response):
        return [Request(url=self.product_url_t.format(product['masterSku']), callback=self.parse_product)
                for product in response.meta['raw_product']['styles']]

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
        return raw_product.get('name', '')

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

    def raw_product(self, response):
        css = 'script:contains("variations") ::text'
        return json.loads(response.css(css).extract_first())

    def product_description(self, raw_product):
        return self.clean([raw_product.get('longDescription')] or [])

    def clean(self, raw_text):
        if type(raw_text) is list:
            return [re.sub('(\r*)(\t*)(\n*)[<>/](<span>)*(<li>)*', '', i) for i in raw_text]
        return re.sub('(\r*)(\t*)(\n*)[<>/](<span>)*(<li>)*', '', raw_text)

    def product_gender(self, response, raw_product):
        css = 'div.nav-breadcrumb ul .display-name ::text'
        gender_soup = ' '.join([self.product_name(raw_product)] +
                               self.product_description(raw_product) +
                               response.css(css).extract()).lower()

        for gender_str, gender in self.GENDER_MAP.items():
            if gender_str in gender_soup:
                return gender

        return 'unisex-adults'

    def product_pricing(self, raw_sku):
        prev_price = raw_sku.get('oldPrice')
        pricing = {'price': raw_sku['currentPrice']['value']}
        pricing['currency'] = raw_sku['currentPrice']['currency']

        if prev_price:
            pricing['previous_price'] = prev_price['value']

        return pricing

    def skus(self, raw_product):
        skus = {}

        for raw_sku in raw_product['variations'].values():
            sku = self.product_pricing(raw_sku)
            size = raw_sku['variationValues'].get('Var_Size')
            colour = raw_sku['variationValues'].get('Var_Article')
            length = raw_sku['variationValues'].get('Var_Dimension3')

            if length and size:
                size += f'_{length}'

            if colour:
                sku['colour'] = colour

            if not raw_sku['productRef']['available']:
                sku['out_of_stock'] = True

            sku['size'] = size or 'One Size'
            skus[raw_sku['sku']] = sku

        return skus
