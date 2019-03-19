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
        css = '.layernavi-loading-cont ::attr(data-pagelet-url)'
        category_r = 'CatalogCategoryID=(.*?)&'

        for category in response.css(css).extract():
            category_id = re.findall(category_r, str(category))[0]
            formdata = self.formdata.copy()
            formdata['category'] = category_id

            yield Request(url=self.category_url, callback=self.parse_pagination,
                          meta={'headers': self.headers, 'formdata': formdata},
                          headers=self.headers, body=json.dumps(formdata), method='POST')

    def parse_pagination(self, response):
        page_size = 72
        headers = response.meta['headers']
        formdata = response.meta['formdata']
        raw_product = json.loads(response.text)
        products = raw_product['searchresult']['result']['count']
        product_ids = [i['masterSku'] for i in raw_product['searchresult']['result']['styles']]

        for product_id in product_ids:
            yield Request(url=self.product_url_t.format(product_id), callback=self.parse_product)

        if 'Page=P' not in response.url and products > page_size:
            for page, per_page_products in enumerate(range(0, int(products), page_size), start=1):
                next_url = add_or_replace_parameter(self.category_url, 'Page', 'P'+str(page))
                yield Request(url=next_url, callback=self.parse_pagination,
                              headers=headers, body=json.dumps(formdata),
                              meta={'headers': headers, 'formdata': formdata}, method='POST')

    def parse_product(self, response):
        item = BaurdeCrawlerItem()
        raw_product = self.raw_product(response)

        item['lang'] = 'de'
        item['market'] = 'DE'
        item['skus'] = self.skus(response)
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

    def product_brand(self, raw_product):
        return raw_product['brandLinkName']

    def product_description(self, raw_product):
        return [raw_product['longDescription']]

    def product_retailer_sku(self, raw_product):
        return raw_product['sku']

    def product_category(self, response):
        css = 'div.nav-breadcrumb .display-name ::text'
        return response.css(css).extract()[1]

    def product_image_urls(self, response):
        css = '.product-gallery-item > img::attr(src)'
        return response.css(css).extract()

    def raw_product(self, response):
        css = 'script:contains("axisTree") ::text'
        return json.loads(response.css(css).extract_first())

    def product_gender(self, response, raw_product):
        gender = 'unisex-adults'
        css = 'div.nav-breadcrumb .display-name ::text'

        category = response.css(css).extract()
        description = self.product_description(raw_product)
        name = self.product_name(raw_product)

        raw_description = ' '.join([name] + description + [category[2]])

        for key, value in self.GENDER_MAP.items():
            if key in raw_description.lower():
                return value

        return gender

    def raw_sku(self, response):
        css = 'script:contains("axisTree") ::text'
        return json.loads(response.css(css).re_first('"axisTree":(.*?),"variations"'))

    def clean(self, raw_text):
        if raw_text:
            if type(raw_text) is list:
                return [i.replace('\r', '').replace('\t', '').replace('\n', '') for i in raw_text]
            return raw_text.replace('\r', '').replace('\t', '').replace('\n', '')
        return raw_text

    def product_pricing(self, response):
        price_css = '.price-wrapper .price ::text'
        prev_price_css = '.price-wrapper .price-strike ::text'

        raw_product = self.raw_product(response)['variations']
        price = self.clean(response.css(price_css).extract_first())
        prev_price = self.clean(response.css(prev_price_css).extract_first())

        pricing = {'price': price}
        pricing['currency'] = raw_product[list(raw_product.keys())[0]]['currentPrice']['currency']

        if prev_price:
            pricing['previous_price'] = prev_price

        return pricing

    def skus(self, response):
        skus = {}
        raw_sku = self.raw_sku(response)
        common_sku = self.product_pricing(response)
        colours = raw_sku['rootNode']['subTree'].keys()

        for colour in colours:
            if raw_sku['rootNode']['subTree'][colour]['subTree']:
                for size in raw_sku['rootNode']['subTree'][colour]['subTree'].keys():
                    lengths = raw_sku['rootNode']['subTree'][colour]['subTree'][size]['subTree'].keys()

                    if lengths and size:
                        for length in lengths:
                            sku = common_sku.copy()
                            sku['colour'] = colour
                            sku['size'] = size
                            skus[f'{colour}_{size}/{length}'] = sku
                    elif size:
                        sku = common_sku.copy()
                        sku['size'] = size
                        skus[f'{colour}_{size}'] = sku
            else:
                sku = common_sku.copy()
                skus[f'{colour}'] = sku

        return skus

