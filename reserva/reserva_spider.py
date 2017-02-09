import json
import re
from scrapy.http.request import Request
from scrapy.http.request.form import FormRequest
from scrapy.http.response import Response
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.selector.unified import Selector
from scrapy.spiders import Rule
from scrapy.spiders.crawl import CrawlSpider

from skuscraper.spiders.base import BaseCrawlSpider, BaseParseSpider, CurrencyParser, clean


class Mixin:
    allowed_domains = ["www.usereserva.com"]
    start_urls = ['http://www.usereserva.com/usereserva/c/masculino/marcas']
    market = 'BR'
    retailer = 'reserva-br'


class ReservaParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    gender_map = [('MASCULINO', 'men'),
                  ('MENINO', 'boys'),
                  ('MENINA', 'girls'),
                  ('INFANTIL', 'unisex-kids')]
    care_materials = ['ALGODÃO', '%']
    sku_request_url = 'https://www.usereserva.com/usereserva/components/ProductDetails/fragments/product_price.jsp?productId={}&skuId={}'

    def parse(self, hxs):
        raw_product = self.raw_product(hxs)
        product_id = self.product_id(raw_product)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_minimal(garment, hxs)
        garment['name'] = self.product_name(hxs)
        garment['brand'] = self.product_brand(hxs, raw_product)
        garment['gender'] = self.product_gender(hxs)
        garment['image_urls'] = self.image_urls(hxs)
        garment['description'] = self.product_description(hxs, raw_product)
        garment['care'] = self.product_care(hxs, raw_product)
        garment['category'] = self.product_category(hxs)
        garment['skus'] = {}
        if self.out_of_stock(raw_product):
            garment['out_of_stock'] = True
            prev_price, price, currency = self.pricing(raw_product)
            garment['price'] = price
            garment['currency'] = currency
            if prev_price:
                garment['previous_prices'] = [prev_price]
        # garment['merch_info'] = self.merch_info(hxs)
        requests_queue = list(self.sku_requests(hxs, garment))
        garment['meta'] = {
            'requests_queue': requests_queue
        }
        return self.next_request_or_garment(garment)

    def parse_sku_price(self, hxs):
        garment = hxs.meta['garment']
        sku_id = hxs.meta['sku_id']
        # sku = hxs.meta['sku']
        sku = garment['skus'][sku_id]
        sku['currency'] = clean(hxs.css('meta[itemprop=priceCurrency]::attr(content)'))[0]
        sku['price'] = CurrencyParser.lowest_price(clean(hxs.css('span[itemprop=price]::text'))[0])
        garment['skus'][sku_id] = sku
        return self.next_request_or_garment(garment)

    def image_urls(self, hxs):
        return clean(hxs.css('.slider_image img::attr(src)'))

    def sku_requests(self, hxs, garment):
        s_s = hxs.css('#productSelectSize a')
        params_re = "updateProductPrice\('(\d+)',\s*'(\d+)',\s*'(\w+)',"
        sku_common = {}
        sku_common['colour'] = self.product_color(hxs)
        for s_e in s_s:
            sku = sku_common.copy()
            params = s_e.css('::attr(onclick)').re(params_re)
            if not params:
                continue
            product_id = params[0]
            sku_id = params[1]
            size = clean(s_e.xpath('text()'))[0]
            sku['size'] = size
            out_of_stock = params[2] is 'false'
            if out_of_stock:
                sku['out_of_stock'] = True
            request_url = self.sku_request_url.format(product_id, sku_id)
            garment['skus'][sku_id] = sku
            meta = {'garment': garment, 'sku_id': sku_id}
            formdata = {'productId': product_id, 'skuId': sku_id}
            yield FormRequest(url=request_url, formdata=formdata, meta=meta, callback=self.parse_sku_price)

    def product_id(self, raw_product):
        return raw_product['id']

    def raw_product(self, hxs):
        script_css = "script:contains('dataLayer.push({\"Product')::text"
        json_re = re.compile("dataLayer.push\((.*)\);\s*dataLayer", re.S)
        product_json = hxs.css(script_css).re_first(json_re)
        return json.loads(product_json)['Product']

    def product_brand(self, hxs, raw_product):
        return hxs.meta['brand'] if hxs.meta.get('brand') else raw_product['brand']

    def product_name(self, hxs):
        return clean(hxs.css('h1.name::text'))[0]

    def product_description(self, hxs, raw_product):
        return [d for d in self.raw_description(hxs, raw_product)
                if not self.care_criteria(d)]

    def raw_description(self, hxs, raw_product):
        desc_css = "meta[property='og:description']::attr(content)"
        desc = clean(hxs.css(desc_css))
        desc = sum((d.split('. ') for d in desc), [])
        desc += [raw_product['description']]
        return desc

    def product_care(self, hxs, raw_product):
        return [d for d in self.raw_description(hxs, raw_product)
                if self.care_criteria(d)]

    def product_category(self, hxs):
        categories = clean(hxs.xpath("//div[contains(@class,'breadcrumb')]//text()"))
        if 'HOME' in categories:
            categories.remove('HOME')
        return categories

    def product_gender(self, hxs):
        categories = self.product_category(hxs)
        for label, raw_gender in self.gender_map:
            if label in categories:
                return raw_gender
        return 'unisex-adults'

    def out_of_stock(self, raw_product):
        return raw_product['availability'] is not '1'

    def pricing(self, raw_product):
        sale_price = CurrencyParser.conversion(raw_product['salePrice'])
        price = CurrencyParser.conversion(raw_product['listPrice'])
        currency = raw_product['currency']
        return (sale_price, price, currency) if sale_price != price \
            else (None, price, currency)

    def care_criteria(self, line):
        return any(x in self.care_materials for x in line)

    def product_color(self, hxs):
        return clean(hxs.css('#productSelectColor li.active img::attr(alt)'))[0]

    def merch_info(self, response):
        pass


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

    def parse_brand_listing(self, hxs):
        brand = clean(hxs.css('meta[name=name]::attr(content)'))[0]
        for request in self.parse_listing(hxs):
            request.meta['brand'] = brand
            yield request

    def parse_listing(self, hxs):
        for request in self.parse(hxs):
            yield request
        request = self.see_more_request(hxs)
        if request:
            yield request

    def see_more_request(self, response):
        see_more = response.css('.wrap.gallery > a')
        if not see_more:
            return None
        on_click = see_more.css('::attr(onclick)')
        url = on_click.re_first("common.initScroll\(this,\s*'(.*)'\);")
        return Request(url=response.urljoin(url), callback=self.parse_see_more)

    def parse_see_more(self, response):
        json_data = response.text
        raw_json = json.loads(json_data)
        content = raw_json['content']
        html = self.unescape(content)
        html_response = HtmlResponse(body=html.encode(), url=response.url, request=response.request)
        for request in super(BaseCrawlSpider, self).parse(html_response):
            if response.meta.get('brand'):
                request.meta['brand'] = response.meta['brand']
            yield request

        if raw_json['nextPage'] is 'true':
            url = response.urljoin(raw_json['pageUrl'])
            return Request(url=url, callback=self.parse_see_more)

