import datetime
import json
from urllib.parse import quote_plus

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from training.utils import pricing, is_care


def clean_url(url):
    return url.replace("http://fsm2.attraqt.com", "http://de.boohoo.com")


class BoohooSpider(CrawlSpider):
    name = 'boohoo-de'
    language = 'de'
    gender_map = [('girls', 'girls'),
                  ('boys', 'boys'),
                  ('Männlich', 'men'),
                  ('Weiblich', 'women'),
                  ]
    visited_products = set()

    brands = {
        'boohoo-night-herren': 'boohooMAN Night',
        'herren-boohoo-basics': 'boohooMAN Basics',
        'boohoo-blue-herren': 'boohooMAN Blue',
        'boohoo-night': 'boohoo Night',
        'boohoo-blue': 'boohoo Blue',
        'boohoo-basics': 'boohoo basics',
        'boohoo-fit': 'boohoo Fit',
        'boohoo-boutique': 'boohoo boutique',
        'boohoo-cosmetics': 'cosmetics',
        'premium-collection': 'boohoo Premium'
    }

    care = ['material', 'cotton', 'polyester', 'elastane', 'viskose']

    site_id = 'df08ca30-5d22-4ab2-978a-cf3dbbd6a9a5'
    listing_url_t = 'http://fsm2.attraqt.com/zones-js.aspx?version=17.4.3' \
                  '&siteId={site_id}&referrer=&sitereferrer=&pageurl={url}&zone0=prod_list_prods' \
                  '&currency=EUR&config_categorytree={config_categorytree}' \
                  '&config_parentcategorytree={config_parentcategorytree}&config_currency=EUR'

    listing_css = ['.nav-primary', '.pagnNext']
    product_css = ['.prod-search-results .js-quickBuyDetails']

    start_urls = [
        'http://de.boohoo.com',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, process_value=clean_url), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=product_css, process_value=clean_url), callback='parse_product'),
    )

    def parse_pagination(self, response):
        categories = response.url.replace('http://de.boohoo.com/', '').split('/')
        category_tree = '%2F'.join(categories)
        parent_category_tree = '%2F'.join(categories[:-1])
        listing_url = self.listing_url_t.format(
            site_id=self.site_id,
            config_parentcategorytree=parent_category_tree,
            config_categorytree=category_tree,
            url=quote_plus(response.url)
        )
        return Request(url=listing_url,
                       callback=self.parse_listing)

    def parse_listing(self, response):
        response = HtmlResponse(url=response.url,
                                status=response.status,
                                headers=response.headers,
                                body=str.encode(response.body.decode('unicode_escape')),
                                request=response.request)

        yield from self.parse(response)

    def parse_product(self, response):
        retailer_sku = self.product_retailer_sku(response)
        if retailer_sku in self.visited_products:
            return
        self.visited_products.add(retailer_sku)

        product = {
            'crawl_start_time': datetime.datetime.now(),
            'name': self.product_name(response),
            'brand': self.product_brand(response),
            'merch_info': [],
            'retailer_sku': retailer_sku,
            'category': [],
            'image_urls': self.product_image_urls(response),
            'description': self.product_description(response),
            'skus': self.product_skus(response),
            'care': self.product_care(response),
            'gender': self.product_gender(response),
            'spider_name': self.name,
            'lang': self.language,
            'url': response.url,
            'url_original': response.url
        }

        return product

    def product_skus(self, response):
        raw_product = self.raw_product(response)
        skus = {}

        product_sizes = {product_id: size['label']
                        for size in raw_product['attributes']['1113']['options']
                        for product_id in size['products']}

        for size_id in product_sizes:
            for color in raw_product['attributes']['92']['options']:
                out_of_stock = False
                if size_id not in color['products']:
                    out_of_stock = True
                sku_id = '{color}_{size}'.format(color=color['label'], size=product_sizes[size_id])
                sku = self.pricing(response)
                sku.update(
                    {
                        'sku_id': sku_id,
                        'size': product_sizes[size_id],
                        'color': color['label']
                    }
                )
                if out_of_stock:
                    sku['out_of_stock'] = out_of_stock
                skus[sku_id] = sku

        return skus

    def product_name(self, response):
        name_css = '.product-shop .product-name h1::text'
        return response.css(name_css).extract_first()

    def product_brand(self, response):
        splitted_url = response.url.split('/')
        for brand in self.brands:
            if brand in splitted_url:
                return self.brands[brand]
        return 'boohoo'

    def product_image_urls(self, response):
        image_urls_css = '.gallery-image:not(#default-gallery-image) img::attr(src)'
        return response.css(image_urls_css).extract()

    def product_gender(self, response):
        gender_regex = '\(\"pdxtgender\"\,\"(.*?)\"\)|$'
        gender_css = '.main script::text'

        raw_gender = response.url.split('/') + response.css(gender_css).re(gender_regex)
        for gender_str, gender in self.gender_map:
            if gender_str in raw_gender:
                return gender
        return 'unisex-adults'

    def product_raw_description(self, response):
        description_css = '.toggle-content .collateral-accordion ::text'
        return response.css(description_css).extract()

    def product_description(self, response):
        raw_description = self.product_raw_description(response)
        return [rd.strip() for rd in raw_description
                if not is_care(self.care, rd) and rd.strip()]

    def pricing(self, response):
        css = '.price-info .price::text'
        return pricing(response, css)

    def product_care(self, response):
        raw_description = self.product_raw_description(response)
        return [rd.strip() for rd in raw_description
                if is_care(self.care, rd) and rd.strip()]

    def product_retailer_sku(self, response):
        retailer_sku_css = '#prodSKU::text'
        return response.css(retailer_sku_css).extract_first()

    def raw_product(self, response):
        config_regex = 'new Product.Config\((.*?)\)|$'
        config_css = '#product-options-wrapper > script::text'
        return json.loads(response.css(config_css).re(config_regex)[0])
