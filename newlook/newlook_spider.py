import json
import re

from scrapy.http import Request
from w3lib.url import (add_or_replace_parameter, url_query_cleaner,
                       url_query_parameter)

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    retailer = 'newlook'
    allowed_domains = ['www.newlook.com']
    start_urls = ['http://www.newlook.com']

    DOWNLOAD_DELAY = 0.5


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls = ['http://www.newlook.com/uk/']

    nav_url_t = 'http://www.newlook.com/uk/json/meganav/tier-one/{}'
    product_url_t = 'http://www.newlook.com/uk{}'
    skus_url_t = 'http://www.newlook.com/uk/json/multiProduct/productDetails.json?id={}'


class NewlookParseSpider(BaseParseSpider, Mixin):
    brand_css = '[itemprop="brand"] meta::attr(content)'
    description_css = '[itemprop="description"] ::text'
    care_css = '.product-details__care ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(garment['category'])
        garment['image_urls'] = self.image_urls(response)
        garment['merch_info'] = self.merch_info(response)

        if self.is_homeware(garment['category']):
            garment['gender'] = None
            garment['industry'] = 'homeware'

        garment['meta'] = {'requests_queue': self.skus_request(product_id)}

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        pid = url_query_parameter(response.url, 'id')

        raw_product = json.loads(response.text)['data'][pid]

        garment = response.meta['garment']
        garment['skus'] = self.skus(raw_product, pid)

        return self.next_request_or_garment(garment)

    def skus_request(self, product_id):
        return [Request(self.skus_url_t.format(product_id), self.parse_skus)]

    def product_id(self, response):
        return clean(response.css('[itemprop="sku"]::attr(content)'))[0]

    def raw_name(self, response):
        return clean(response.css('.product-description__name::text'))[0]

    def product_gender(self, category):
        soup = ' '.join(category).lower()
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_name(self, response):
        raw_name = self.raw_name(response)
        brand = self.product_brand(response)

        return re.sub(brand, '', raw_name)

    def product_category(self, response):
        category_css = '.breadcrumb [property="name"]::text'
        return clean(response.css(category_css))[1:-1]

    def merch_info(self, response):
        css = '.product-description__highlight ::text'
        return clean(response.css(css))

    def image_urls(self, response):
        images_css = '.product-gallery::attr(data-ng-init)'
        images_script = response.css(images_css).extract_first()
        image_urls = re.findall("'(.+?)'", images_script)

        return ['https:' + url + '?qlt=80&w=720' for url in image_urls]

    def is_homeware(self, category):
        soup = ' '.join(category).lower()
        return 'homeware' in soup

    def product_pricing_common(self, raw_product):
        raw_price = raw_product['price']
        previous_price = raw_product.get('previousPrice', {}).get('value')
        
        money_strs = [raw_price['value'], previous_price, raw_price['currencyIso']]

        return super().product_pricing_common(None, money_strs=money_strs)

    def skus(self, raw_product, pid):
        sku_common = self.product_pricing_common(raw_product)
        sku_common['colour'] = raw_product['colourOptions'][pid]['displayName']

        skus = {}
        for raw_sku in raw_product['sizeOptions']:
            sku = sku_common.copy()
            sku['size'] = raw_sku['value']

            if 'hasStock' in raw_sku:
                sku['out_of_stock'] = True

            skus[raw_sku['sku']] = sku

        return skus


class NewlookCrawlSpider(BaseCrawlSpider, Mixin):
    listing_urls_r = re.compile('"url":"(.+?)"')

    def parse_start_url(self, response):
        meta = {'trail': self.add_trail(response)}

        nav_css = '.main-navigation__primary-menu-link::attr(data-uid)'
        nav_ids = clean(response.css(nav_css))

        for nav_id in nav_ids:
            url = self.nav_url_t.format(nav_id)

            yield Request(url, self.parse_menu, meta=meta.copy())
    
    def parse_menu(self, response):
        meta = {'trail': self.add_trail(response)}

        listing_urls = self.listing_urls_r.findall(response.text)
        for url in listing_urls:
            if '/c/' not in url:
                continue
            
            url = response.urljoin(url)
            url = f'{url_query_cleaner(url)}/data-48.json'

            yield Request(url, self.parse_listing, meta=meta.copy())
    
    def parse_listing(self, response):
        meta = {'trail': self.add_trail(response)}

        raw_category = json.loads(response.text)
        if not raw_category['success']:
            return

        for product in raw_category['data']['results']:
            for color in product['colourOptions'].values():
                url = self.product_url_t.format(color['url'])

                yield Request(url, self.parse_item, meta=meta.copy())

        if not url_query_parameter(response.url, 'page'):
            yield from self.pagination_requests(response, raw_category)

    def pagination_requests(self, response, category):
        meta = {'trail': self.add_trail(response)}

        pages = category['data']['pagination']['numberOfPages']
        for page in range(1, pages):
            url = add_or_replace_parameter(response.url, 'page', page)

            yield Request(url, self.parse_listing, meta=meta.copy())


class NewlookUKParseSpider(NewlookParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class NewlookUKCrawlSpider(NewlookCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = NewlookUKParseSpider()
