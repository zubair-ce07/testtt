import json

import base64
import re
from scrapy.http import Request, FormRequest

from .base import BaseParseSpider, BaseCrawlSpider, clean
from ..utils.encodings import rot47


class UniversalMixin:
    retailer = 'new-universal-at'
    brand = "UNIVERSAL"
    market = 'AT'

    allowed_domains = ['www.universal.at']
    start_urls = [
        'https://www.universal.at/',
    ]

    products_url_t = 'https://www.universal.at/suche/mba/magellan'
    p_details_url_t = 'https://www.universal.at/p/'

    image_url_t = 'https://media.universal.at/i/empiriecom/{}'
    availability_url_t = '{}INTERSHOP/rest/WFS/EmpirieCom-UniversalAT-Site/-;loc=de_AT;' \
                         'cur=EUR/inventories/{}/master?'
    garbage_categories = ['...']


class ParseSpider(BaseParseSpider, UniversalMixin):
    one_sizes = ['one size', 'none']
    brand_css = '.product-manufacturer-logo img::attr(alt)'

    def parse(self, response):
        raw_product = self.raw_product(response)
        pid = raw_product['sku']

        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(raw_product)
        garment["gender"] = self.product_gender(response)
        garment['meta'] = {'requests_queue': self.availability_request(pid)}

        return self.next_request_or_garment(garment)

    def availability_request(self, product_id):
        url = self.availability_url_t.format(self.start_urls[0], product_id)
        return [Request(url, callback=self.parse_availability)]

    def parse_availability(self, response):
        skus = json.loads(response.text)['variants']
        garment = response.meta['garment']
        for sku in skus:
            if 'NOT' in sku['deliveryStatus']:
                sku_id = sku['sku']
                garment['skus'][sku_id]['out_of_stock'] = True

        return self.next_request_or_garment(garment)

    def skus(self, raw_product):
        skus = {}

        for variation in raw_product['variations'].values():

            currency = variation['currentPrice']['currency']
            price = variation['currentPrice']['value']
            p_price = variation.get('oldStartPrice')
            if p_price:
                previous_price = p_price['value']
            else:
                previous_price = []

            money_strs = [price, previous_price, currency]

            sku = skus[variation["sku"]] = self.product_pricing_common(None, money_strs=money_strs)
            colour = variation['variationValues'].get('Var_Article')
            if colour:
                sku['colour'] = colour

            size = variation['variationValues'].get('Var_Size', self.one_size)
            size = self.one_size if size in self.one_sizes else size
            sku["size"] = size

            dimension = variation['variationValues'].get("Var_Dimension3")
            if dimension:
                sku['size'] = f'{size}/{dimension}'

        return skus

    def raw_product(self, response):
        raw_skus = clean(response.css('.data-product-detail::text'))[0]
        return json.loads(raw_skus)

    def raw_name(self, response):
        return clean(response.css('.headline::text'))[0]

    def product_name(self, response):
        name = self.raw_name(response)
        brand = self.product_brand(response)
        name = re.sub(brand, '', name, flags=re.I).strip()
        return re.sub('^[,\.]\s*', '', name)

    def product_category(self, response):
        raw_categories = clean(response.css('.nav-bc-path ::text'))
        return [category for category in raw_categories if category not in self.garbage_categories]

    def raw_description(self, response, **kwargs):
        css_1 = '.sellingpoints-wrapper .rendered-data ::text'
        css_2 = '.tmpArticleDetailTable tr'

        xpath = '//*[contains(@class,"product-description")]//*[contains(@class,"rendered-data")]' \
                '//text()[not(ancestor::*[contains(@class,"tmpArticleDetailTable")])]'

        raw_description = clean(response.css(css_1)) + [' '.join(clean(response.xpath(xpath)))]
        raw_description += [' '.join(clean(rd_s.css('::text'))) for rd_s in response.css(css_2)]
        return raw_description + [' '.join(clean(response.css('.long-description ::text')))]

    def product_gender(self, response):
        navigation_cat = clean(response.css('.active.customdelay > a::text'))
        tokens = self.product_category(response) + [self.raw_name(response)] + navigation_cat
        return self.gender_lookup(' '.join(tokens)) or "unisex-adults"

    def image_urls(self, raw_product):
        return [self.image_url_t.format(image['image']) for image in raw_product["imageList"]["i0"]]


class CrawlSpider(BaseCrawlSpider, UniversalMixin):

    def parse(self, response):
        meta = {'trail': self.add_trail(response)}
        category_names = clean(response.css('.customdelay a::text'))
        categories_css = ['a[data-lm-attr-2*=\"{}\"] + ul'.format(name) for name in category_names]
        encoded_listings_css = [css + ' span::attr(data-src)' for css in categories_css]
        encoded_listings_css = ','.join(encoded_listings_css)

        for url in response.css(encoded_listings_css).extract():
            b64_decoded = base64.b64decode(url)
            rot47_decoded = rot47(b64_decoded.decode())
            sub_cat_url = response.urljoin(rot47_decoded)

            yield Request(sub_cat_url, meta=meta, callback=self.parse_sub_categories)

    def parse_sub_categories(self, response):
        form_data_xpath = '//script[contains(text(),"LocaleID")]/text()'
        form_data_text = clean(response.xpath(form_data_xpath))[0]
        meta = {'trail': self.add_trail(response)}

        form_data = {
            "category": re.findall('category.:"(.*?)"', form_data_text)[0],
            "channel": "web",
            "clientId": "UniversalAt",
            "count": 72,
            "locale": re.findall('LocaleID.:"(.*?)"', form_data_text)[0],
            "minAvailCode": 2,
            "sessionId": re.findall('sid.\s?:"(.*?)"', form_data_text)[0],
            "start": 0,
            "version": 42,
        }

        body = json.dumps(form_data)
        yield FormRequest(url=self.products_url_t, method='POST', body=body,
                          meta=meta, callback=self.parse_pagination)

    def parse_pagination(self, response):
        meta = {'trail': self.add_trail(response)}
        raw_body = json.loads(response.request.body)
        total_count_text = json.loads(response.text)
        products_text = total_count_text["searchresult"]["result"]["styles"]

        for text in products_text:
            product_url = f"{self.p_details_url_t}{text.get('masterSku', '')}"

            yield Request(url=product_url, meta=meta, callback=self.parse_item)

        total_count = total_count_text["searchresult"]["result"]["count"]

        for start_value in range(72, total_count + 1, 72):
            raw_body["start"] = start_value
            body = json.dumps(raw_body)

            yield FormRequest(url=self.products_url_t, method='POST', meta=meta,
                              body=body, callback=self.parse_pagination)


class UniversalParseSpider(ParseSpider, UniversalMixin):
    name = UniversalMixin.retailer + '-parse'


class UniversalCrawlSpider(CrawlSpider, UniversalMixin):
    name = UniversalMixin.retailer + '-crawl'
    parse_spider = UniversalParseSpider()
