from json import loads
from re import findall

from demjson import decode
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from scrapy import FormRequest

from asos.items import Product


class AsosSpider(CrawlSpider):
    name = 'asos'
    allowed_domains = ['asos.com']

    start_url = 'http://www.asos.com/ru/'
    stock_url = 'http://www.asos.com/api/product/catalogue/v2/stockprice'
    category_url = 'http://api.asos.com/fashion/navigation/v2/tree/navigation'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.99 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://www.asos.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    cookies = {}

    product_css = 'article'
    pagination_css = '[data-auto-id="loadMoreProducts"]'

    rules = (
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
        Rule(LinkExtractor(restrict_css=pagination_css, ), callback='parse'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 6,
    }

    def start_requests(self):
        yield Request(self.start_url, headers=self.headers, callback=self.parse_navigation_attr)

    def parse_navigation_attr(self, response):
        script_xpath = '//script[contains(.,"var RegionalStore")]'
        script_sel = response.xpath(script_xpath)
        raw_store = script_sel.re_first('\s*var\s*RegionalStore\s*=([^;]+)')
        raw_config = script_sel.re_first('\s*var\s*GlobalConfig\s*=([^;]+)')

        raw_store = loads(raw_store, strict=False)
        raw_config = decode(raw_config)

        params = {
            "country": raw_config.get('countryCode'),
            "keyStoreDataversion": raw_store.get('keyStoreDataversion'),
            "lang": raw_config.get('languageCode')
        }
        yield FormRequest(self.category_url, headers=self.headers, cookies=self.cookies,
                          formdata=params, callback=self.parse_category, method='GET')

    def parse_category(self, response):
        self.extract_cookie(response)

        category_links = self.extract_category_links(loads(response.text, strict=False), [])

        for link in category_links:
            yield Request(link, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse_product(self, response):
        raw_product = self.get_raw_product(response)

        product_item = Product()

        product_item['gender'] = self.get_gender(raw_product)
        product_item['image_urls'] = self.get_image_urls(raw_product)
        product_item['name'] = self.get_product_name(raw_product)
        product_item['skus'] = self.get_skus(raw_product)

        product_item['retailer_sku'] = self.get_retailer_sku(response)
        product_item['description'] = self.get_description(response)
        product_item['category'] = self.get_categories(response)
        product_item['url'] = self.get_product_url(response)
        product_item['brand'] = self.get_brand(response)
        product_item['care'] = self.get_care(response)

        return self.product_stock_request(product_item, raw_product)

    def product_stock_request(self, product_item, raw_product):
        raw_stock = raw_product.get('store', {})
        params = {
            "productIds": str(raw_product.get('id')),
            "currency": raw_stock.get('currency'),
            "keyStoreDataversion": raw_stock.get('keyStoreDataversion'),
            "store": raw_stock.get('code')
        }
        yield FormRequest(self.stock_url, headers=self.headers, cookies=self.cookies,
                          meta={'item': product_item}, formdata=params,
                          callback=self.parse_product_stock, method='GET')

    def parse_product_stock(self, response):
        raw_stock = loads(response.text, strict=False)[0].get("variants")
        product_item = response.meta.get('item')
        product_skus = product_item.get('skus').copy()
        prod_stock_map = {r_stock.get("variantId"): r_stock.get("isInStock") for r_stock in raw_stock}

        for sku in product_skus:
            if prod_stock_map.get(sku.get('sku_id', '')) == "false":
                sku['out_of_stock'] = True

            sku['sku_id'] = f'{sku.get("color")}_{sku.get("size")}'

        product_item['skus'] = product_skus

        return product_item

    def get_raw_product(self, response):
        xpath = '//script[contains(.,"Pages/FullProduct")]'
        raw_product = response.xpath(xpath).re_first("view\('([^']+)")
        return loads(raw_product, strict=False)

    def get_gender(self, raw_product):
        return raw_product.get('gender', 'Unisex')

    def get_image_urls(self, raw_product):
        raw_images = raw_product.get('images', [])
        product_images = [raw_image.get('url') for raw_image in raw_images]
        return [f'http:{url}?$XXL$' for url in product_images]

    def get_product_name(self, raw_product):
        return raw_product.get('name', '')

    def get_skus(self, raw_product):
        raw_skus = raw_product.get('variants', [])
        raw_price = raw_product.get('price', {})

        if not raw_skus:
            return []

        product_skus = []
        for raw_sku in raw_skus:
            sku = {'size': raw_sku.get('size'),
                   'color': raw_sku.get('colour'),
                   'price': raw_price.get('current'),
                   'currency': raw_price.get('currency')}

            prev_price = raw_price.get('previous')

            if prev_price:
                sku['previous_price'] = [prev_price]

            sku['sku_id'] = raw_sku.get('variantId')

            product_skus.append(sku)

        return product_skus

    def get_care(self, response):
        care_css = '.care-info span ::text'
        return response.css(care_css).extract()

    def get_description(self, response):
        desc_css = '.product-description li::text'
        return response.css(desc_css).extract()

    def get_retailer_sku(self, response):
        prod_sku_css = '.product-code span::text'
        return response.css(prod_sku_css).extract_first(default='')

    def get_brand(self, response):
        brand_css = '.brand-description strong::text'
        return response.css(brand_css).extract_first(default='')

    def get_product_url(self, response):
        return response.url

    def get_categories(self, response):
        category_css = '.bread-crumb a::text'
        return response.css(category_css).extract()

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
