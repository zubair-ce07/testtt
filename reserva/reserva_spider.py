import json

import re
from scrapy.http.request import Request
from scrapy.http.request.form import FormRequest
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, CurrencyParser, clean


class Mixin:
    allowed_domains = ["www.usereserva.com"]
    start_urls = ['http://www.usereserva.com/usereserva/c/masculino/marcas']
    market = 'BR'
    retailer = 'reserva-br'
    lang = 'pt'


class ReservaParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    gender_map = [('MASCULINO', 'men'),
                  ('MENINO', 'boys'),
                  ('MENINA', 'girls'),
                  ('INFANTIL', 'unisex-kids')]
    sku_request_url = 'https://www.usereserva.com/usereserva/components/ProductDetails/fragments/product_price.jsp?productId={}&skuId={}'
    product_re = re.compile("dataLayer.push\((.*)\);\s*dataLayer", re.S)

    def parse(self, response):
        product = self.raw_product(response)
        product_id = self.product_id(product)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_minimal(garment, response)
        garment['name'] = self.product_name(response)
        garment['brand'] = self.product_brand(response, product)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['description'] = self.product_description(response, product)
        garment['care'] = self.product_care(response, product)
        garment['category'] = self.product_category(response)
        if self.out_of_stock(product):
            garment['out_of_stock'] = True
            prev_price, price, currency = self.product_pricing(product)
            garment['price'] = price
            garment['currency'] = currency
            if prev_price:
                garment['previous_prices'] = [prev_price]

        garment['skus'] = self.skus(response)
        requests_queue = self.price_requests(garment)
        garment['meta'] = {
            'requests_queue': requests_queue
        }
        return self.next_request_or_garment(garment)

    def parse_sku_price(self, response):
        garment = response.meta['garment']
        sku_id = response.meta['sku_id']
        currency = clean(response.css('meta[itemprop=priceCurrency]::attr(content)'))[0]
        price = CurrencyParser.lowest_price(clean(response.css('span[itemprop=price]::text'))[0])
        garment['skus'][sku_id].update({'price': price, 'currency': currency})
        return self.next_request_or_garment(garment)

    def image_urls(self, response):
        return clean(response.css('.slider_image img::attr(src)'))

    def skus(self, response):
        skus = {}
        sku_common = {'colour': self.product_color(response)}
        s_s = response.css('#productSelectSize a')
        params_re = "updateProductPrice\('(\d+)',\s*'(\d+)',\s*'(\w+)',"
        for s_e in s_s:
            size = clean(s_e.xpath('text()'))[0]
            params = s_e.css('::attr(onclick)').re(params_re)
            if not params:
                continue
            sku_id = params[1]
            sku = sku_common.copy()
            sku['size'] = size
            if params[2] is 'false':
                sku['out_of_stock'] = True
            skus[sku_id] = sku
        return skus

    def price_requests(self, garment):
        requests = []
        for sku in garment['skus']:
            product_id = garment['retailer_sku']
            request_url = self.sku_request_url.format(product_id, sku)
            meta = {'garment': garment, 'sku_id': sku}
            formdata = {'productId': product_id, 'skuId': sku}
            requests.append(FormRequest(url=request_url, formdata=formdata, meta=meta, callback=self.parse_sku_price))
        return requests

    def product_id(self, raw_product):
        return raw_product['id']

    def raw_product(self, response):
        script_css = "script:contains('dataLayer.push({\"Product')::text"
        product_json = response.css(script_css).re_first(self.product_re)
        return json.loads(product_json)['Product']

    def product_brand(self, response, product):
        return response.meta['brand'] if response.meta.get('brand') else product['brand']

    def product_name(self, response):
        return clean(response.css('h1.name::text'))[0]

    def product_description(self, response, product):
        return [d for d in self.raw_description(response, product)
                if not self.care_criteria(d)]

    def raw_description(self, response, product):
        desc = clean(response.css("meta[property='og:description']::attr(content)"))
        desc = sum((d.split('. ') for d in desc), []) + [product['description']]
        return desc

    def product_care(self, response, product):
        return [d for d in self.raw_description(response, product) if self.care_criteria(d)]

    def product_category(self, response):
        return clean(response.css(".breadcrumb li:not(li:first-child) *::text"))

    def product_gender(self, response):
        categories = self.product_category(response)
        for label, raw_gender in self.gender_map:
            if label in categories:
                return raw_gender

    def out_of_stock(self, product):
        return product['availability'] is not '1'

    def product_pricing(self, product):
        sale_price = CurrencyParser.conversion(product['salePrice'])
        price = CurrencyParser.conversion(product['listPrice'])
        currency = product['currency']
        return (sale_price, price, currency) if sale_price != price else (None, price, currency)

    def product_color(self, response):
        return clean(response.css('#productSelectColor li.active img::attr(alt)'))[0]


class ReservaCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = ReservaParseSpider()
    listing_css = [".menu"]
    product_css = ["#product_box"]
    deny_css = ['/cartao-presente', '/faca-voce']
    rules = (Rule(LinkExtractor(allow='/marcas'), callback='parse_brand_listing'),
             Rule(LinkExtractor(restrict_css=listing_css, deny=deny_css), callback='parse_listing'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
             )

    def parse_brand_listing(self, response):
        brand = clean(response.css('meta[name=name]::attr(content)'))[0]
        for request in self.parse_listing(response):
            request.meta['brand'] = brand
            yield request

    def parse_listing(self, response):
        for request in self.parse(response):
            yield request
        see_more = response.css('.wrap.gallery > a')
        if not see_more:
            return None
        on_click = see_more.css('::attr(onclick)')
        url = on_click.re_first("common.initScroll\(this,\s*'(.*)'\);")
        pagination_request = Request(url=response.urljoin(url), callback=self.parse_pagination)
        if pagination_request:
            yield pagination_request

    def parse_pagination(self, response):
        json_response = json.loads(response.text)
        content = json_response['content']
        html = self.unescape(content)
        html_response = HtmlResponse(body=html.encode(), url=response.url, request=response.request)
        for request in self.parse(html_response):
            if response.meta.get('brand'):
                request.meta['brand'] = response.meta['brand']
            yield request

        if json_response['nextPage'] is 'true':
            url = response.urljoin(json_response['pageUrl'])
            return Request(url=url, callback=self.parse_pagination)

