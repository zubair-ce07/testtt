from json import loads
from re import findall
from w3lib.url import url_query_cleaner
from six.moves.urllib.parse import urlencode

from demjson import decode
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from asos.items import Product


class AsosSpider(CrawlSpider):
    name = 'asos'
    allowed_domains = ['asos.com']
    start_urls = ['http://www.asos.com/ru/']

    stock_url_t = 'http://www.asos.com/api/product/catalogue/v2/stockprice?{}'
    listing_url_t = 'http://api.asos.com/fashion/navigation/v2/tree/navigation?{}'

    product_css = 'article'
    pagination_css = '[data-auto-id="loadMoreProducts"]'

    rules = (
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
        Rule(LinkExtractor(restrict_css=pagination_css, ), callback='parse'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/68.0.3440.106 Safari/537.36'
    }

    def parse_start_url(self, response):
        script_sel = response.xpath('//script[contains(.,"var RegionalStore")]')

        raw_store = loads(script_sel.re_first('\s*var\s*RegionalStore\s*=([^;]+)'))
        raw_config = decode(script_sel.re_first('\s*var\s*GlobalConfig\s*=([^;]+)'))

        params = {
            "country": raw_config.get('countryCode'),
            "keyStoreDataversion": raw_store.get('keyStoreDataversion'),
            "lang": raw_config.get('languageCode')
        }
        yield Request(self.listing_url_t.format(urlencode(params)), callback=self.parse_menu)

    def parse_menu(self, response):
        for url in self.extract_listing_urls(loads(response.text), []):
            yield Request(url, cookies=self.extract_cookie(response), callback=self.parse)

    def parse_product(self, response):
        raw_product = self.extract_raw_product(response)

        product_item = Product()

        product_item['gender'] = self.extract_gender(raw_product)
        product_item['skus'] = self.extract_skus(raw_product)

        product_item['name'] = self.extract_product_name(response)
        product_item['image_urls'] = self.extract_image_urls(response)
        product_item['retailer_sku'] = self.extract_retailer_sku(response)
        product_item['description'] = self.extract_description(response)
        product_item['category'] = self.extract_categories(response)
        product_item['url'] = self.extract_product_url(response)
        product_item['brand'] = self.extract_brand(response)
        product_item['care'] = self.extract_care(response)

        return self.stock_request(product_item, raw_product)

    def parse_stock(self, response):
        raw_stock = loads(response.text)[0].get("variants")
        product_item = response.meta['item']
        product_skus = product_item['skus'].copy()
        product_item['skus'] = self.update_skus_status(product_skus, raw_stock)
        return product_item

    def stock_request(self, product_item, raw_product):
        raw_stock = raw_product['store']

        params = {}
        params["productIds"] = str(raw_product.get('id')),
        params["currency"] = raw_stock.get('currency'),
        params["keyStoreDataversion"] = raw_stock.get('keyStoreDataversion'),
        params["store"] = raw_stock.get('code')

        yield Request(self.stock_url_t.format(urlencode(params)), meta={'item': product_item},
                      callback=self.parse_stock)

    def update_skus_status(self, skus, raw_stock):
        prod_stock_map = {r_stock.get("variantId"): r_stock.get("isInStock") for r_stock in raw_stock}

        for sku in skus:

            if prod_stock_map[sku['sku_id']] == "false":
                sku['out_of_stock'] = True

            sku['sku_id'] = f'{sku["color"]}_{sku["size"]}'

        return skus

    def extract_raw_product(self, response):
        xpath = '//script[contains(.,"Pages/FullProduct")]'
        return loads(response.xpath(xpath).re_first("view\('([^']+)"))

    def extract_gender(self, raw_product):
        return raw_product.get('gender') or 'Unisex'

    def extract_skus(self, raw_product):
        raw_price = raw_product['price']
        common = dict()
        common['price'] = raw_price['current']
        common['currency']= raw_price['currency']
        prev_price = raw_price.get('previous')

        if prev_price:
            common['previous_price'] = [prev_price]

        product_skus = []
        for raw_sku in raw_product['variants']:
            sku = common.copy()
            sku['color'] = raw_sku['colour']
            sku['size'] = raw_sku.get('size') or 'One Size'
            sku['sku_id'] = raw_sku['variantId']
            product_skus.append(sku)

        return product_skus

    def extract_image_urls(self, response):
        raw_images = response.css('.product-gallery img::attr(src)').extract()
        product_images = [url_query_cleaner(raw_image) for raw_image in raw_images]

        return [f'http:{url}?$XXL$' for url in product_images]

    def extract_product_name(self, response):
        return response.css('.product-hero h1::text').extract_first()

    def extract_care(self, response):
        return response.css('.care-info span ::text').extract()

    def extract_description(self, response):
        return response.css('.product-description li::text').extract()

    def extract_retailer_sku(self, response):
        return response.css('.product-code span::text').extract_first()

    def extract_brand(self, response):
        return response.css('.brand-description strong::text').extract_first()

    def extract_product_url(self, response):
        return response.url

    def extract_categories(self, response):
        return response.css('.bread-crumb a::text').extract()

    def extract_listing_urls(self, raw_navs, category_links):
        for raw_nav in raw_navs:
            link = raw_nav.get('link')
            if link:
                if link.get('linkType') == 'category':
                    category_links.append(link.get('webUrl'))
            sub_nav = raw_nav.get('children')
            if sub_nav:
                self.extract_listing_urls(sub_nav, category_links)
        return category_links

    def extract_cookie(self, response):
        raw_cookie = response.request.headers.get(b'Cookie')
        if raw_cookie:
            return {'geocountry': findall('geocountry=([^;]+)', raw_cookie.decode('utf-8'))[0]}
