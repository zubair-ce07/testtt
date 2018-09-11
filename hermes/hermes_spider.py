import json
import re
from urllib.parse import urljoin

from scrapy import Request, Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import (BaseCrawlSpider, BaseParseSpider, Gender, clean,
                   reset_cookies)


class Mixin:
    retailer = 'hermes'
    allowed_domains = ['hermes.com']
    start_urls = ['https://www.hermes.com']


class MixinAT(Mixin):
    retailer = Mixin.retailer + '-at'
    market = 'AT'
    start_urls = ['https://www.hermes.com/at/de/']

    paging_url_t = 'https://www.hermes.com/apps/cde/personalize/grid/{}'
    stock_url = 'https://www.hermes.com/apps/ecom/stock'


class HermesParseSpider(BaseParseSpider, Mixin):
    care_css = '.field-name-field-care-instructions-text ::text'
    raw_product_r = re.compile('Drupal.settings,(.*)\);')

    def parse(self, response):
        raw_product = self.raw_product(response)['hermes_products']['data']['products']

        product_id = self.product_id(raw_product)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return
        
        self.boilerplate(garment, response)

        garment['name'] = self.product_name(raw_product)
        garment['description'] = self.product_description(response, raw_product=raw_product)
        garment['care'] = self.product_care(response, raw_product=raw_product)
        garment['category'] = self.product_category(response)
        garment['brand'] = self.product_brand(response)

        if self.is_homeware(response):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(response)
            
        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(raw_product)

        garment['meta'] = {'requests_queue': self.stock_request(garment)}

        return self.next_request_or_garment(garment)
    
    def parse_stock(self, response):
        garment = response.meta.get('garment')
        stock = json.loads(response.text)

        garment['skus'] = self.update_skus_status(stock, garment['skus'])

        return self.next_request_or_garment(garment)

    def update_skus_status(self, stock, skus):
        for sku_id, sku in skus.items():
            if stock.get(sku_id, {}).get('in_stock') == False:
                sku['out_of_stock'] = True

        return skus

    def stock_request(self, garment):
        skus = '","'.join(garment['skus'].keys())

        formdata = f'{{"skus":["{skus}"],"locale":"at_de","container_id":null}}'
        headers = {'content-type': 'application/json'}
        cookies = {"ECOM_SESS": "315ec9f785993778ab5f5ee8fb81e18f"}

        return [Request(self.stock_url, self.parse_stock, body=formdata,
                        method='POST', cookies=cookies, headers=headers)]

    def product_id(self, raw_product):
        return raw_product[0]['nid']

    def product_name(self, raw_product):
        return raw_product[0]['display_name']

    def raw_description(self, response, **kwargs):
        raw_product = kwargs.get('raw_product')

        raw_description = raw_product[0]['description'] + raw_product[0]['measurements']
        raw_description += clean(Selector(text=raw_product[0].get('detail', '')).css(' ::text'))

        return sum([rd.split(',') for rd in raw_description], [])
    
    def product_category(self, response):
        raw_product = self.raw_product(response)['personalize_taxonomy_context']
        category = raw_product['vocabularies']['product_category']

        return category.split(',')
    
    def product_brand(self, response):
        css = '[type="application/ld+json"]::text'
        raw_brand = json.loads(clean(response.css(css)[0]))['brand']
        
        return raw_brand['name']
    
    def is_homeware(self, response):
        return 'home' in ' '.join(self.product_category(response)).lower()
    
    def product_gender(self, response):
        soup = self.product_category(response) + [t for _, t in response.meta.get('trail', [])]
        return self.gender_lookup(' '.join(soup)) or Gender.ADULTS.value
    
    def image_urls(self, raw_product):
        image_urls = [f"http:{img['uri']}-1535-1535.jpg" for p in raw_product for img in p['images']]
        return sorted(set(image_urls), key=image_urls.index)

    def skus(self, raw_products):
        skus = {}
        for raw_sku in raw_products:
            money_strs = [raw_sku['price']]
            sku = self.product_pricing_common(None, money_strs=money_strs)

            raw_colour = raw_sku['attributes'].get('field_color_hermes')
            if raw_colour:
                sku['colour'] = raw_colour['name']
            
            size = raw_sku['attributes'].get('field_ref_size', {}).get('attr_display')
            sku['size'] = size or self.one_size

            skus[raw_sku['sku']] = sku

        return skus

    def raw_product(self, response):
        xpath = '//script[contains(., "basePath")]'
        return json.loads(response.xpath(xpath).re_first(self.raw_product_r))


class HermesCrawlSpider(BaseCrawlSpider, Mixin):
    custom_settings = {'DOWNLOAD_DELAY': 0.5}
    raw_listing_r = re.compile('Drupal.settings,(.*)\);')

    listing_css = ['#tray-nav-shop']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css),
             callback='parse_listing'),
    )

    def parse_listing(self, response):
        xpath = '//script[contains(., "basePath")]'
        raw_listing = response.xpath(xpath).re_first(self.raw_listing_r)
        raw_listing = json.loads(raw_listing)

        meta = {'trail': self.add_trail(response)}
        headers = {"Content-Type": "application/json", 'Cookie': 'has_js=1'}
        form_data = json.dumps({
            "offset": 0,
            "limit": 36,
            "locale": raw_listing['hermes_locale'],
            "url_locale": raw_listing['hermes_url_locale'],
            "parents": raw_listing['hermes_category']['parents'],
            "sort": "relevance"
        })
        url = self.paging_url_t.format(raw_listing['hermes_category']['data'])

        yield Request(url, self.parse_paging, body=form_data, meta=meta,
                      method='POST', headers=headers)

    def parse_paging(self, response):
        page = json.loads(response.text)

        meta = {'trail': response.meta.get('trail')}
        headers = response.request.headers
        form_data = json.loads(response.request.body.decode())

        total_products = page['total']
        for page_offset in range(36, total_products, 36):
            form_data['offset'] = page_offset

            yield Request(response.url, self.parse_products, body=json.dumps(form_data),
                          method='POST', headers=headers, meta=meta, dont_filter=True)

        yield from self.parse_products(response)

    def parse_products(self, response):
        raw_products = json.loads(response.text)['products']

        meta = {'trail': response.meta.get('trail')}
        headers = response.request.headers

        for product in raw_products['items']:
            url = f'{self.start_urls[0]}{product["url"][1:]}/'

            yield reset_cookies(Request(url, self.parse_item, meta=meta, headers=headers))


class HermesATParseSpider(HermesParseSpider, MixinAT):
    name = MixinAT.retailer + '-parse'


class HermesATCrawlSpider(HermesCrawlSpider, MixinAT):
    name = MixinAT.retailer + '-crawl'
    parse_spider = HermesATParseSpider()
