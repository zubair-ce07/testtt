import json

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from w3lib.url import add_or_replace_parameter

from nike.items import NikeItem


class NikeParser:
    visited_products = set()
    gender_map = {
        'kids girls boys': 'unisex-kids',
        'women men': 'unisex-adults',
        'girls boys': 'unisex-adults',
        'women': 'women',
        'men': 'men',
        'girls': 'girls',
        'boys': 'boys',
    }

    def parse(self, response):
        if '/pd/' in response.url:
            return self.parse_secondry(response)

        product_id = self.retailer_sku(response)

        if self.is_visited_id(product_id):
            return

        raw_product = self.extract_raw_product(response)

        item = NikeItem()
        item['retailer_sku'] = product_id
        item['name'] = self.extract_name(raw_product)
        item['brand'] = self.extract_brand(response)
        item['gender'] = self.extract_gender(raw_product)
        item['category'] = self.extract_category(response)
        item['trail'] = self.extract_trail(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(raw_product)
        item['image_urls'] = self.extract_image_urls(raw_product)
        item['skus'] = self.extract_skus(raw_product)
        item['url'] = response.url

        return [item] + self.generate_colour_requests(response)

    def parse_secondry(self, response):
        raw_product = self.extract_raw_product_secondary(response)
        product_id = self.retailer_sku_secondary(raw_product)

        if self.is_visited_id(product_id):
            return

        item = NikeItem()
        item['retailer_sku'] = product_id
        item['name'] = self.extract_name_secondary(raw_product)
        item['gender'] = self.extract_gender(raw_product)
        item['brand'] = self.extract_brand(response)
        item['category'] = self.extract_category(response)
        item['trail'] = self.extract_trail(response)
        item['care'] = self.extract_care_secondary(raw_product)
        item['description'] = self.extract_description_secondary(raw_product)
        item['image_urls'] = self.extract_image_urls_secondary(raw_product)
        item['skus'] = self.extract_skus_secondary(raw_product)
        item['url'] = response.url

        return [item] + self.generate_colour_requests(response)

    def is_visited_id(self, product_id):
        if product_id in self.visited_products:
            return True

        self.visited_products.add(product_id)

    def extract_raw_product(self, response):
        css = '#app-root ~ script::text'
        raw_product = response.css(css).re_first('{.+}')
        raw_product = json.loads(raw_product)
        raw_product = raw_product['Threads']['products']

        raw_product['retailer_sku'] = self.retailer_sku(response)
        return raw_product

    def extract_raw_product_secondary(self, response):
        css = '#product-data::text'
        raw_product = response.css(css).extract_first()
        return json.loads(raw_product)

    def retailer_sku(self, response):
        css = '.description-preview__style-color.ncss-li::text'
        return response.css(css).extract_first().replace('Style: ', '')

    def retailer_sku_secondary(self, raw_product):
        return f"{raw_product['styleNumber']}{raw_product['colorNumber']}"

    def clean_pricing(self, prices):
        pricing = {}
        prices = [float(p) * 100 if isinstance(p, float) or p.replace('.', '', 1).isdigit()
                  else float(p[1:]) * 100 for p in prices]
        pricing['price'], *previous_prices = sorted(prices)

        if previous_prices and pricing['price'] < previous_prices[0]:
            pricing['previous_prices'] = previous_prices
        return pricing

    def extract_pricing(self, raw_prices):
        pricing = self.clean_pricing([raw_prices['currentPrice'], raw_prices['fullPrice']])
        pricing['currency'] = raw_prices['currency']
        return pricing

    def extract_pricing_secondary(self, raw_pricing):
        pricing = self.clean_pricing([raw_pricing['rawPrice'], raw_pricing['overriddenLocalPrice']])
        pricing['currency'] = raw_pricing['currencyCode']
        return pricing

    def extract_in_stock_skus(self, raw_skus):
        return [raw_sku['skuId'] for raw_sku in raw_skus['availableSkus']]

    def extract_skus(self, raw_product):
        skus = []
        common_sku = {}

        raw_colour = raw_product[raw_product['retailer_sku']]
        common_sku['colour'] = raw_colour['colorDescription']
        common_sku.update(self.extract_pricing(raw_colour))
        in_stock_skus = self.extract_in_stock_skus(raw_colour)

        for raw_sku in raw_colour['skus']:
            sku = common_sku.copy()
            sku['sku_id'] = raw_sku['id']
            size = raw_sku['localizedSize']
            sku['size'] = 'One Size' if size == 'ONE SIZE' else size

            if raw_sku['skuId'] not in in_stock_skus:
                sku['out_of_stock'] = True

            skus += [sku]

        return skus

    def extract_skus_secondary(self, raw_product):
        skus = []
        common_sku = self.extract_pricing_secondary(raw_product)
        common_sku['colour'] = raw_product['colorDescription']

        for raw_sku in raw_product['skuContainer']['productSkus']:
            sku = common_sku.copy()
            sku['sku_id'] = raw_sku['id']
            sku['size'] = raw_sku['sizeDescription']

            if raw_sku['inStock'] is not True:
                sku['out_of_stock'] = True

            skus += [sku]

        return skus

    def extract_image_urls(self, raw_product):
        raw_urls = raw_product[raw_product['retailer_sku']]
        raw_urls = raw_urls['nodes'][0]['nodes']
        return [url['properties'].get('squarishURL') or
                url['properties']['startImageURL'] for url in raw_urls]

    def extract_image_urls_secondary(self, raw_product):
        return raw_product['imagesHeroLarge']

    def extract_brand(self, response):
        css = '#app-root ~ script::text'
        brand = response.css(css).re('{"brand":"(.*?)",')
        if brand:
            return brand[0]

        css = "[type='application/ld+json']::text"
        raw_brand = response.css(css).extract_first().replace('\n', '')
        brand = json.loads(raw_brand)['brand']
        if brand:
            return brand
        return 'NIKE'

    def extract_name(self, raw_product):
        return raw_product[raw_product['retailer_sku']]['title']

    def extract_name_secondary(self, raw_product):
        return raw_product['displayName']

    def extract_gender(self, raw_product):
        raw_gender = raw_product.get(raw_product.get('retailer_sku'))

        soup = ' '.join(raw_gender['genders']).lower() if raw_gender else \
            raw_product['trackingData']['product']['gender']

        for gender_str, gender in self.gender_map.items():
            if gender_str.lower() in soup:
                return gender

        return 'unisex-adults'

    def extract_care(self, response):
        css = '.pi-pdpmainbody li ::text'
        return response.css(css).extract()

    def extract_care_secondary(self, raw_product):
        raw_care = raw_product['content']
        return Selector(text=raw_care).css('ul li::text').extract()

    def extract_description(self, raw_product):
        raw_description = raw_product[raw_product['retailer_sku']]
        return raw_description['descriptionPreview'].split('.')

    def extract_description_secondary(self, raw_product):
        raw_description = raw_product['content']
        return Selector(text=raw_description).css('p ::text').extract()

    def extract_trail(self, response):
        return response.meta['trail']

    def extract_category(self, response):
        return [t for t, _ in response.meta['trail'] if t]

    def generate_colour_requests(self, response):
        css = '.colorway-product-overlay:not(.colorway-product-overlay--selected) a::attr(href),' \
              '.color-chip-container li:not(.selected) a::attr(href)'
        urls = response.css(css).extract()

        meta = {'trail': self.extract_trail(response)}
        return [response.follow(url, callback=self.parse, meta=meta.copy()) for url in urls]


class NikeCrawler(CrawlSpider):
    name = 'nike_spider'
    allowed_domains = ['nike.com']
    start_urls = ['https://store.nike.com/gb/en_gb/']
    nike_parser = NikeParser()

    listing_url_t = 'https://store.nike.com/html-services/' \
                    'gridwallData?country=GB&lang_locale=en_GB&gridwallPath=n/1j5'
    page_size = 60

    def parse(self, response):
        yield from self.create_listings_requests(response)

    def parse_products(self, response):
        yield from self.create_product_requests(response)

    def create_listings_requests(self, response):
        total_products = self.extract_total_products(response)
        total_pages = (total_products // self.page_size) + 1
        meta = {'trail': [(self.extract_title(response), response.url)]}

        requests = []

        for page_number in range(total_pages):
            url = add_or_replace_parameter(self.listing_url_t, 'pn', page_number + 1)
            requests.append(response.follow(url, callback=self.parse_products, meta=meta.copy()))

        return requests

    def create_product_requests(self, response):
        raw_urls = json.loads(response.text)['sections'][0]['items']

        requests = []
        meta = {'trail': response.meta['trail'] + [('', response.url)]}

        for raw_url in raw_urls:
            url = raw_url['pdpUrl']
            requests.append(response.follow(url, callback=self.nike_parser.parse, meta=meta.copy()))

        return requests

    def extract_title(self, response):
        css = 'head title::text'
        return response.css(css).extract_first()

    def extract_total_products(self, response):
        css = '#pageTrackingDataElement::text'
        raw_number = json.loads(response.css(css).extract_first())
        return raw_number['response']['totalResults']
