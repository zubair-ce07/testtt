from json import loads
from w3lib.html import remove_tags
from w3lib.url import url_query_cleaner

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

from universal.items import Product


class UniversalSpider(CrawlSpider):
    name = 'universal'
    allowed_domains = ['universal.at']

    start_urls = ['https://www.universal.at/']

    stock_url = 'https://www.universal.at/INTERSHOP/rest/WFS/EmpirieCom-UniversalAT-Site/' \
                '-;loc=de_AT;cur=EUR/inventories/{}/master'

    gender_map = {
        'damen': 'Ladies',
        'herren': "Men's",
        'kinder': 'Kids',
    }
    care_words = ['reinigung', 'Maschinenwäsche', '%']
    deny_urls = ['/lifestyle/', '/baumarkt/', '.*\/technik\/?.*', '.*\/sale\/?.*']

    listing_css = '.nav-main,.ls-image-link,.branch,.paging-holder .pp'
    product_css = '.link-product'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_urls), callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_product'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }

    def parse_product(self, response):
        raw_product = self.extract_raw_product(response)

        product_item = Product()

        product_item['name'] = self.extract_product_name(raw_product)
        product_item['retailer_sku'] = self.extract_retailer_sku(raw_product)
        product_item['brand'] = self.extract_brand(raw_product)
        product_item['description'] = self.extract_description(raw_product)
        product_item['care'] = self.extract_care(raw_product)
        product_item['skus'] = self.extract_skus(raw_product)

        product_item['gender'] = self.extract_gender(response)
        product_item['image_urls'] = self.extract_image_urls(response)
        product_item['url'] = self.extract_product_url(response)
        product_item['category'] = self.extract_categories(response)

        return self.product_stock_request(product_item)

    def product_stock_request(self, product_item):
        meta = {'item': product_item}
        yield Request(self.stock_url.format(product_item['retailer_sku']), meta=meta,
                      callback=self.parse_stock)

    def extract_raw_product(self, response):
        return loads(response.css('[type="text/x-json-product"]::text').extract_first())

    def parse_stock(self, response):
        raw_stock = loads(response.text)["variants"]
        prod_stock_map = {value['sku']: value["deliveryStatus"] for value in raw_stock}

        product_item = response.meta['item']
        product_skus = product_item['skus'].copy()

        for sku in product_skus:
            if prod_stock_map[sku['sku_id']] == 'NOT_AVAILABLE':
                sku['out_of_stock'] = True

            sku['sku_id'] = f"{sku['color']}_{sku['size']}"

        product_item['skus'] = product_skus

        return product_item

    def extract_skus(self, raw_product):
        product_skus = []
        for raw_sku in raw_product["variations"].values():
            sku = {}
            color_specs = raw_sku["variationValues"]
            sku['size'] = color_specs.get("Var_Size", color_specs.get("Var_Dimension3", 'One_Size'))
            sku['color'] = color_specs.get("Var_Article", '')
            sku['price'] = raw_sku["currentPrice"]["value"]
            sku['currency'] = raw_sku["currentPrice"]["currency"]
            prev_price = raw_sku.get('oldPrice')

            if prev_price:
                sku['previous_price'] = [prev_price['value']]
            sku['sku_id'] = raw_sku['sku']

            product_skus.append(sku)

        return product_skus

    def extract_gender(self, response):
        prod_categories = self.extract_categories(response)
        for raw_gender in self.gender_map.keys():
            if raw_gender in ' '.join(prod_categories).lower():
                return self.gender_map[raw_gender]
        return 'Unisex-adults'

    def extract_image_urls(self, response):
        raw_images = response.css('.product-main-gallery-item img::attr(data-lazy)').extract()
        return [f'{url_query_cleaner(url)}?w=3210&h=1947' for url in raw_images]

    def extract_product_name(self, raw_product):
        return raw_product["name"]

    def extract_care(self, raw_product):
        raw_care = raw_product["commonMap"]['k2'] or {}
        prod_care = []
        for care in raw_care.get('ArticleDetails', []):
            if care['name'].lower() in ' '.join(self.care_words).lower():
                prod_care.append(care['name'])

        return prod_care

    def extract_description(self, raw_product):
        return [remove_tags(raw_product.get("longDescription", raw_product['tags']['T0']))]

    def extract_retailer_sku(self, raw_product):
        return raw_product['sku']

    def extract_brand(self, raw_product):
        return raw_product['variation'].get("manufacturerName", 'Universal')

    def extract_product_url(self, response):
        return response.url

    def extract_categories(self, response):
        category_css = '[type="application/ld+json"]:contains(BreadcrumbList)::text'
        raw_category = loads(response.css(category_css).extract_first())
        return [c['item']['name'] for c in raw_category['itemListElement']]
