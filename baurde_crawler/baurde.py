import json
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request
from w3lib.url import add_or_replace_parameter

from baurde_crawler.items import BaurdeCrawlerItem


class BaurdeCrawler(CrawlSpider):
    GENDER_MAP = {
        'dam': 'men',
        ' men': 'men',
        ' Men': 'men',
        " Men's": 'men',
        " men's": 'men',
        'herren': 'men',
        'herr': 'women',
        'women': 'women',
        'damen': 'women',
        'boy': 'boy',
        'jungen': 'boy',
        'girl': 'girl',
        'mädchen': 'girl',
        'kid': 'unisex-kids',
        'Kid': 'unisex-kids',
        'barn': 'unisex-kids',
        'kinder': 'unisex-kids',
        'herr, dam': 'unisex-adults',
    }

    name = 'baur-de-crawl'
    allowed_domains = ['baur.de']
    start_urls = ['https://www.baur.de/']

    listings_css = ['#nav-main-list']
    products_css = ['.plp-area1']

    rules = (Rule(LinkExtractor(restrict_css=listings_css), callback='parse_sub_category'),
             Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'))

    def parse_sub_category(self, response):
        css = '.layernavi-loading-cont ::attr(data-pagelet-url)'
        pattern = 'CatalogCategoryID=(.*?)&'

        for category in response.css(css).extract():
            category_id = re.findall(pattern, str(category))[0]

            headers = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                               Chrome/71.0.3578.98 Safari/537.36',
                'authority': 'www.baur.de',
                'accept': 'application/json',
                'x-requested-with': 'XMLHttpRequest',
                'origin': 'https://www.baur.de',
                'content-type': 'application/json; charset=UTF-8',
            }

            formdata = {
                'start': 0,
                'clientId': 'BaurDe',
                "version": 44,
                "channel": "web",
                'locale': 'de_DE',
                'count': 72,
                'category': category_id,
                'personalization': '$$-2$$web$',
            }

            next_url = 'https://www.baur.de/suche/mba/magellan'
            yield Request(url=next_url, callback=self.parse_pagination,
                          headers=headers, body=json.dumps(formdata),
                          meta={'headers': headers, 'formdata': formdata}, method='POST')

    def parse_pagination(self, response):
        page_size = 72
        headers = response.meta['headers']
        formdata = response.meta['formdata']
        json_raw_product = json.loads(response.text)
        products = json_raw_product['searchresult']['result']['count']
        product_ids = [i['masterSku'] for i in json_raw_product['searchresult']['result']['styles']]

        for product_id in product_ids:
            nex_url = f'https://www.baur.de/p/{product_id}'
            yield Request(url=nex_url, callback=self.parse_product)

        if 'Page=P' not in response.url and products > page_size:
            for page, per_page_products in enumerate(range(0, int(products), page_size), start=1):
                next_url = 'https://www.baur.de/suche/mba/magellan'
                next_url = add_or_replace_parameter(next_url, 'Page', 'P'+str(page))
                yield Request(url=next_url, callback=self.parse_pagination,
                              headers=headers, body=json.dumps(formdata),
                              meta={'headers': headers, 'formdata': formdata}, method='POST')

    def parse_product(self, response):
        item = BaurdeCrawlerItem()
        raw_product = self.raw_product(response)

        item['lang'] = 'de'
        item['market'] = 'DE'
        item['url'] = self.product_url(response)
        item['skus'] = self.product_skus(response)
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

    def product_brand(self, raw_product):
        return raw_product['brandLinkName']

    def product_market(self, raw_product):
        return raw_product['country']

    def product_gender(self, response, raw_product):
        gender = 'unisex-adults'
        css = 'div.nav-breadcrumb .display-name ::text'

        sub_category = response.css(css).extract()
        description = self.product_description(raw_product)
        name = self.product_name(raw_product)

        for key, value in self.GENDER_MAP.items():
            if key in description:
                return value
            if key in sub_category[2]:
                return value
            if key in name:
                return value
        return gender

    def product_name(self, raw_product):
        return raw_product['name']

    def product_description(self, raw_product):
        return raw_product['longDescription']

    def product_retailer_sku(self, raw_product):
        return raw_product['sku']

    def product_category(self, response):
        css = 'div.nav-breadcrumb .display-name ::text'
        breadcrumb = response.css(css).extract()
        return breadcrumb[1]

    def product_image_urls(self, response):
        css = '.product-gallery-item > img::attr(src)'
        return response.css(css).extract()

    def raw_product(self, response):
        css = 'script:contains("axisTree") ::text'
        raw_product = response.css(css).extract_first()
        return json.loads(raw_product)

    def raw_sku(self, response):
        css = 'script:contains("axisTree") ::text'
        raw_product = response.css(css).re_first('"axisTree":(.*?),"variations"')
        return json.loads(raw_product)

    def clean(self, raw_text):
        return raw_text.replace('\r', '').replace('\t', '').replace('\n', '')

    def product_pricing(self, response):
        price_css = '.price-wrapper .price ::text'
        prev_price_css = '.price-wrapper .price-strike ::text'

        price = self.clean(response.css(price_css).extract_first())
        prev_price = response.css(prev_price_css).extract_first()

        raw_product = self.raw_product(response)
        pricing = {'price': price}
        key = list(raw_product['variations'].keys())[0]
        pricing['currency'] = raw_product['variations'][key]['currentPrice']['currency']

        if prev_price:
            prev_price = self.clean(prev_price)
            if prev_price:
                pricing['previous_price'] = prev_price
        return pricing

    def product_skus(self, response):
        item_skus = {}
        raw_sku = self.raw_sku(response)
        colours = raw_sku['rootNode']['subTree'].keys()

        for colour in colours:
            if raw_sku['rootNode']['subTree'][colour]['subTree']:
                for size in raw_sku['rootNode']['subTree'][colour]['subTree'].keys():
                    lengths = raw_sku['rootNode']['subTree'][colour]['subTree'][size]['subTree'].keys()
                    item_skus.update(self.skus(response, colour, size, lengths))
            else:
                item_skus.update(self.skus(response, colour))
        return item_skus

    def skus(self, response, colour, size=0, lengths=None):
        skus = {}
        common_sku = self.product_pricing(response)

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
