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

    start_url = 'http://www.asos.com/ru/'
    stock_url = 'http://www.asos.com/api/product/catalogue/v2/stockprice?{}'
    category_url = 'http://api.asos.com/fashion/navigation/v2/tree/navigation?{}'

    cookies = {}

    product_css = 'article'
    pagination_css = '[data-auto-id="loadMoreProducts"]'

    rules = (
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
        Rule(LinkExtractor(restrict_css=pagination_css, ), callback='parse'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 6,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/68.0.3440.106 Safari/537.36'
    }

    def start_requests(self):
        yield Request(self.start_url, callback=self.parse_navigation_attr)

    def parse_navigation_attr(self, response):
        script_xpath = '//script[contains(.,"var RegionalStore")]'
        script_sel = response.xpath(script_xpath)
        raw_store = script_sel.re_first('\s*var\s*RegionalStore\s*=([^;]+)')
        raw_config = script_sel.re_first('\s*var\s*GlobalConfig\s*=([^;]+)')

        raw_store = loads(raw_store)
        raw_config = decode(raw_config)

        params = {
            "country": raw_config.get('countryCode'),
            "keyStoreDataversion": raw_store.get('keyStoreDataversion'),
            "lang": raw_config.get('languageCode')
        }
        yield Request(self.category_url.format(urlencode(params)), callback=self.parse_category)

    def parse_category(self, response):
        self.extract_cookie(response)
        category_links = self.extract_category_links(loads(response.text), [])

        for link in category_links:
            yield Request(link, cookies=self.cookies, callback=self.parse)

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

        return self.product_stock_request(product_item, raw_product)

    def product_stock_request(self, product_item, raw_product):
        raw_stock = raw_product.get('store', {})
        params = {
            "productIds": str(raw_product.get('id')),
            "currency": raw_stock.get('currency'),
            "keyStoreDataversion": raw_stock.get('keyStoreDataversion'),
            "store": raw_stock.get('code')
        }
        yield Request(self.stock_url.format(urlencode(params)), cookies=self.cookies,
                      meta={'item': product_item}, callback=self.parse_product_stock)

    def parse_product_stock(self, response):
        raw_stock = loads(response.text)[0].get("variants")
        product_item = response.meta.get('item')
        product_skus = product_item.get('skus').copy()
        prod_stock_map = {r_stock.get("variantId"): r_stock.get("isInStock") for r_stock in raw_stock}

        for sku in product_skus:
            if prod_stock_map.get(sku.get('sku_id', '')) == "false":
                sku['out_of_stock'] = True

            sku['sku_id'] = f'{sku.get("color")}_{sku.get("size")}'

        product_item['skus'] = product_skus

        return product_item

    def extract_raw_product(self, response):
        xpath = '//script[contains(.,"Pages/FullProduct")]'
        raw_product = response.xpath(xpath).re_first("view\('([^']+)")
        return loads(raw_product)

    def extract_gender(self, raw_product):
        prod_gender = raw_product.get('gender')

        if not prod_gender:
            prod_gender = 'Unisex'

        return prod_gender

    def extract_skus(self, raw_product):
        raw_skus = raw_product['variants']
        raw_price = raw_product['price']

        product_skus = []
        for raw_sku in raw_skus:
            sku = {'color': raw_sku['colour'],
                   'price': raw_price['current'],
                   'currency': raw_price['currency']
                   }
            prod_size = raw_sku.get('size')

            if not prod_size:
                prod_size = 'One Size'

            sku['size'] = prod_size
            prev_price = raw_price.get('previous')

            if prev_price:
                sku['previous_price'] = [prev_price]

            sku['sku_id'] = raw_sku.get('variantId')
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

    def extract_category_links(self, raw_navs, category_links):
        for raw_nav in raw_navs:
            link = raw_nav.get('link')
            if link:
                if link.get('linkType') == 'category':
                    category_links.append(link.get('webUrl'))
            sub_nav = raw_nav.get('children')
            if sub_nav:
                self.extract_category_links(sub_nav, category_links)
        return category_links

    def extract_cookie(self, response):
        raw_cookie = response.request.headers.get(b'Cookie')
        if raw_cookie:
            self.cookies['geocountry'] = findall('geocountry=([^;]+)', raw_cookie.decode('utf-8'))[0]
