import re
import json

from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = 'tesco-uk'
    allowed_domains = ['tesco.com']
    lang = 'en'
    market = 'UK'
    s_availability_url_t = "https://www.tesco.com/direct/rest/inventory/product/{c_code}?format=standard"
    s_price_url_t = "https://www.tesco.com/direct/rest/price/product/{c_code}?format=standard"
    s_text_url_t = "https://www.tesco.com/direct/rest/content/catalog/product/{c_code}?format=standard"
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

        self.boilerplate_normal(garment, response)
        garment['skus'] = {}
        garment['image_urls'] = self.image_urls(response)
        garment['meta'] = {'requests_queue': self.skus_requests(response)}
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def colours_map(self, response):
        c_map = {}
        script_text = response.xpath('//script[contains(text(), "window.Data.PDP")]').extract_first()
        for c_sku_json in json.loads(re.findall('links" : (?s)(.+)},\nsku ', script_text)[0]):
            if c_sku_json.get("rel") in ["colourAssociation", "self"]:
                if c_sku_json.get('options'):
                    c_map[c_sku_json["id"]] = c_sku_json['options']['primary']
                else:
                    c_map[c_sku_json["id"]] = self.detect_colour_from_name(response)
        return c_map

    def skus_requests(self, response):
        requests = []
        for c_code, c_name in self.colours_map(response).items():
            response.meta['colour'] = c_name
            requests.append(Request(self.s_text_url_t.format(c_code=c_code), meta=response.meta,
                                    callback=self.parse_colour))
            requests.append(Request(self.s_availability_url_t.format(c_code=c_code), meta=response.meta,
                                    callback=self.parse_colour))
            requests.append(Request(self.s_price_url_t.format(c_code=c_code), meta=response.meta,
                                    callback=self.parse_colour))
        return requests

    def skus(self, response):
        skus = response.meta['garment']['skus']
        common = {'currency': 'GBP'}
        common['colour'] = response.meta['colour']
        res_json = json.loads(response.text)
        skus_json = res_json['links'] if res_json.get('links') else res_json['products'][0]['skus']

        for sku_json in skus_json:
            if not sku_json.get('id'):
                continue
            if sku_json.get('rel') and not sku_json.get('rel') == "childSku":
                continue
            sku = skus.get("{}_{}".format(common['colour'], sku_json['id']), common.copy())

            if sku_json.get('rel'):
                sku['size'] = sku_json['options']['secondary'] if sku_json.get('options') else sku_json['id']
            if sku_json.get('price'):
                sku['price'] = int(sku_json.get('price').replace(".", ""))
                if sku_json.get('was'):
                    sku['previous_prices'] = [int(sku_json.get('was').replace(".", ""))]
            # for out-of-stock products
            if not sku.get('price') and res_json.get('prices'):
                sku['price'] = int(res_json.get('prices').get('price').replace(".", ""))
                if res_json.get('prices').get('was'):
                    sku['previous_prices'] = [int(res_json.get('prices').get('was').replace(".", ""))]

            if sku_json.get('available') is False:
                sku['out_of_stock'] = True
            skus["{}_{}".format(sku['colour'], sku_json['id'])] = sku
        return skus

    def product_care(self, response):
        return []

    def product_category(self, response):
        return clean(response.css('div#breadcrumb-v2 li:not(.first) span::text'))

    def product_id(self, response):
        if response.css('.product-description-block .style-ref::text'):
            return clean(response.css('.product-description-block .style-ref::text'))[0].split('Ref: ')[1][:-2]
        return clean(response.css('.catalogue-id::text'))[0]

    def product_name(self, response):
        brand = self.product_brand(response)
        return clean(response.css('.product-title-text::text'))[0].replace(brand, "")

    def product_description(self, response):
        return clean(response.css('div[itemprop="description"] ::text'))

    def image_urls(self, response):
        urls = []
        img_urls = list(set(response.xpath('//script[contains(text(), "window.Data.PDP")]').re('src" : "(.+)\?')))
        for c_code in list(self.colours_map(response).keys()):
            urls += [re.sub('(\d+-\d+)', c_code, url) for url in img_urls]
        return urls

    def product_brand(self, response):
        return response.xpath('//script[contains(text(), "window.Data.PDP")]').re('brand" : "(.+)",')[0]


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
        cat_id = response.css('.products-wrapper').re('data-endecaid="(.+?)"')[0]
        for pg_no in range(2, total_pages + 1):
            url = self.pagination_url_t.format(cat_id=cat_id, offset=(pg_no - 1) * self.page_size)
            response.meta['trail'] = self.add_trail(response)
            yield Request(url, meta=response.meta, callback=self.parse_pagination)

    def parse_pagination(self, response):
        urls = re.findall('nail\\\\" href=\\\\"(.+?)\\\\"', response.text)
        for url in urls:
            response.meta['trail'] = self.add_trail(response)
            yield Request(response.urljoin(url), meta=response.meta, callback=self.parse_item)
