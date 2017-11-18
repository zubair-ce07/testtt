import re
import json

from scrapy import Request, Selector
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'tesco-uk'
    allowed_domains = ['tesco.com']
    lang = 'en'
    market = 'UK'
    currency = '£'
    stock_url_t = "https://www.tesco.com/direct/rest/inventory/product/{c_code}?format=standard"
    colour_url_t = "https://www.tesco.com/direct/rest/content/catalog/product/{c_code}?format=standard"
    pagination_url_t = ("https://www.tesco.com/direct/blocks/catalog/productlisting/infiniteBrowse.jsp?catId={"
                        "cat_id}&currentPageType=Category&offset={offset}")

    start_urls_with_meta = [
        ('https://www.tesco.com/direct/clothing-accessories/mens-clothing-shoes/cat38470010.cat?', {'gender': 'men'}),
        ('https://www.tesco.com/direct/clothing-accessories/womens-clothing-accessories/cat38310015.cat?',
         {'gender': 'women'}),
    ]


class TescoParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        p_id = self.product_id(response)
        garment = self.new_unique_garment(p_id)
        if not garment:
            return

        raw_skus = response.xpath('//script[contains(text(), "window.Data.PDP")]').extract_first()
        self.boilerplate(garment, response)
        garment['care'] = []
        garment['skus'] = {}
        garment['name'] = self.product_name(response, raw_skus)
        garment['brand'] = self.product_brand(raw_skus)
        garment['description'] = self.product_description(response)
        garment['category'] = self.product_category(response)
        garment['image_urls'] = self.image_urls(response, raw_skus)
        garment['meta'] = {'requests_queue': self.skus_requests(response, raw_skus)}
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus_colour(response))
        return self.next_request_or_garment(garment)

    def parse_stock(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus_stock(response))
        return self.next_request_or_garment(garment)

    def skus_colour(self, response):
        skus = response.meta['garment']['skus']
        res_json = json.loads(response.text)
        price_strings = self.sku_prices(res_json)
        common = self.product_pricing_common_new(None, money_strs=price_strings)
        common['colour'] = response.meta['colour']
        for sku_json in res_json['links']:
            if sku_json.get('rel') != "childSku":
                continue
            sku = skus.get(sku_json['id'], common.copy())
            sku['size'] = sku_json['options']['secondary'] if sku_json.get('options') else sku_json['id']
            skus[sku_json['id']] = sku
        return skus

    def sku_prices(self, res_json):
        price_json = res_json.get('prices')
        price_string = price_json.get('price', price_json.get('fromPrice')) + self.currency
        p_price_string = price_json.get('was', price_json.get('toPrice'))
        return price_string, p_price_string

    def skus_stock(self, response):
        skus = response.meta['garment']['skus']
        res_json = json.loads(response.text)
        for sku_json in res_json['products'][0]['skus']:
            sku = skus.get(sku_json['id'], {})
            if not sku_json.get('available', True):
                sku['out_of_stock'] = True
            skus[sku_json['id']] = sku
        return skus

    def colours_map(self, response, raw_skus):
        c_map = {}
        for c_sku_json in json.loads(re.findall('links" : (?s)(.+)},\nsku ', raw_skus)[0]):
            if c_sku_json.get("rel") not in ["colourAssociation", "self"]:
                continue
            if c_sku_json.get('options'):
                c_map[c_sku_json["id"]] = c_sku_json['options']['primary']
            else:
                c_map[c_sku_json["id"]] = self.detect_colour(self.product_name(response, raw_skus))
        return c_map

    def skus_requests(self, response, raw_skus):
        requests = []
        for c_code, c_name in self.colours_map(response, raw_skus).items():
            response.meta['colour'] = c_name
            requests.append(Request(self.stock_url_t.format(c_code=c_code), meta=response.meta,
                                    callback=self.parse_stock))
            requests.append(Request(self.colour_url_t.format(c_code=c_code), meta=response.meta,
                                    callback=self.parse_colour))
        return requests

    def product_category(self, response):
        return clean(response.css('div#breadcrumb-v2 li:not(.first) span::text'))

    def product_id(self, response):
        if response.css('.product-description-block .style-ref::text'):
            return clean(response.css('.product-description-block .style-ref::text'))[0].split('Ref: ')[1][:-2]
        return clean(response.css('.catalogue-id::text'))[0]

    def product_name(self, response, raw_skus):
        brand = self.product_brand(raw_skus)
        return clean(response.css('.product-title-text::text'))[0].replace(brand, "")

    def product_description(self, response):
        return clean(response.css('div[itemprop="description"] ::text'))

    def image_urls(self, response, raw_skus):
        urls = []
        img_urls = set(re.findall('src" : "(.+)\?', raw_skus))
        for c_code in self.colours_map(response, raw_skus).keys():
            urls += [re.sub('(\d+-\d+)', c_code, url) for url in img_urls]
        return urls

    def product_brand(self, raw_skus):
        return re.findall('brand" : "(.+)",', raw_skus)[0]


class TescoCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = TescoParseSpider()
    page_size = 20
    products_css = '.image-container'
    listing_css = '.fnfstamps--category'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

    def parse(self, response):
        yield from super(TescoCrawlSpider, self).parse(response)
        total_items = clean(response.css('.filter-productCount b::text'))
        if not total_items:
            return
        total_pages = int(total_items[0]) // self.page_size + 1
        cat_id = clean(response.css('.products-wrapper::attr(data-endecaid)'))[0]
        for pg_no in range(2, total_pages + 1):
            url = self.pagination_url_t.format(cat_id=cat_id, offset=(pg_no - 1) * self.page_size)
            response.meta['trail'] = self.add_trail(response)
            yield Request(url, meta=response.meta, callback=self.parse_pagination)

    def parse_pagination(self, response):
        products_urls_css = '.image-container .thumbnail::attr(href)'
        products_html = Selector(text=json.loads(response.text)['products'])
        for url in clean(products_html.css(products_urls_css)):
            response.meta['trail'] = self.add_trail(response)
            yield Request(response.urljoin(url), meta=response.meta, callback=self.parse_item)
