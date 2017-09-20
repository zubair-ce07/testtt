import datetime
import json
import re
from urllib.parse import quote_plus
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.http import HtmlResponse
from training.utils import clean_and_convert_price, currency_information


def modify_product_url(url):
    return url.replace("http://fsm2.attraqt.com", "http://de.boohoo.com")


class BoohooSpider(CrawlSpider):
    name = 'boohoo-de'
    language = 'de'
    genders = ['girls', 'boys']
    visited = set()

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

    care = ['Material', 'Cotton', 'Polyester', 'Elastane', 'Viskose']

    site_id = 'df08ca30-5d22-4ab2-978a-cf3dbbd6a9a5'
    product_store_url = 'http://fsm2.attraqt.com/zones-js.aspx?version=17.4.3' \
                        '&siteId={site_id}&referrer=&sitereferrer=&pageurl={url}&zone0=prod_list_prods' \
                        '&currency=EUR&config_categorytree={config_categorytree}' \
                        '&config_parentcategorytree={config_parentcategorytree}&config_currency=EUR'

    mega_menu_css = '.nav-primary'
    pagination_css = '.pagnNext'
    product_link_css = '.prod-search-results .js-quickBuyDetails'

    rules = (
        Rule(LinkExtractor(restrict_css=[mega_menu_css, pagination_css],
                           process_value=modify_product_url),
             callback='crawl_pages'),
        Rule(LinkExtractor(restrict_css=[product_link_css],
                           process_value=modify_product_url),
            callback='parse_product'),
    )

    start_urls = [
        'http://de.boohoo.com',
    ]

    def crawl_pages(self, response):
        categories = response.url.replace('http://de.boohoo.com/', '').split('/')
        category_tree = '%2F'.join(categories)
        parent_category_tree = '%2F'.join(categories[:-1])
        product_store_url = self.product_store_url.format(
            site_id=self.site_id,
            config_parentcategorytree=parent_category_tree,
            config_categorytree=category_tree,
            url=quote_plus(response.url)
        )
        return Request(url=product_store_url,
                       callback=self.modify_product_store_response)

    def modify_product_store_response(self, response):
        response = HtmlResponse(url=response.url,
                                status=response.status,
                                headers=response.headers,
                                body=str.encode(response.body.decode('unicode_escape')),
                                request=response.request)

        yield from self.parse(response)

    def parse_product(self, response):
        retailer_sku = self.product_retailer_sku(response)
        if retailer_sku in self.visited:
            return
        self.visited.add(retailer_sku)

        product = {
            'crawl_start_time': datetime.datetime.now(),
            'name': self.product_name(response),
            'brand': self.product_brand(response),
            'merch_info': self.merch_info(response),
            'retailer_sku': retailer_sku,
            'category': self.product_category(response),
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
        raw_product = self.product_raw(response)
        skus = {}
        for color in raw_product['attributes']['92']['options']:
            for size in raw_product['attributes']['1113']['options']:
                out_of_stock = False
                if not set(color['products']).intersection(size['products']):
                    out_of_stock = True

                price, currency = self.product_price_and_currency(response)
                sku_id = '{color}_{size}'.format(color=color['label'], size=size['label'])
                sku = {
                    'sku_id': sku_id,
                    'size': size['label'],
                    'currency': currency,
                    'price': price[0],
                    'previous_price': price[1:],
                    'color': color['label']
                }
                if out_of_stock:
                    sku['out_of_stock'] = out_of_stock
                skus[sku_id] = sku

        return list(skus.values())

    def product_name(self, response):
        name_css = '.product-shop .product-name h1::text'
        return response.css(name_css).extract_first()

    def product_category(self, response):
        return []

    def product_brand(self, response):
        return self.brands.get(response.url.split('/')[-2], 'boohoo')

    def product_image_urls(self, response):
        image_urls_css = '.gallery-image:not(#default-gallery-image) img::attr(src)'
        return response.css(image_urls_css).extract()

    def merch_info(self, response):
        return []

    def product_gender(self, response):
        gender_regex = '\(\"pdxtgender\"\,\"(.*?)\"\)|$'
        gender_css = '.main script::text'

        splited_url = response.url.split('/')
        if 'kids' in splited_url:
            for gender in self.genders:
                if gender in splited_url:
                    return gender

        gender = re.findall(gender_regex, response.css(gender_css).extract_first())[0]
        if gender == 'Weiblich':
            product_gender = 'women'
        if gender == 'Männlich':
            product_gender = 'men'
        return product_gender or 'unisex-adults'

    def product_price_and_currency(self, response):
        price_css = '.price-info .price::text'
        product_price = response.css(price_css).extract()
        if product_price:
            currency = currency_information(product_price[0])
            price = [clean_and_convert_price(price, currency[1]) for price in product_price]
            price.sort(key=int)
            return (price, currency[0])

    def product_raw_description(self, response):
        description_css = '.toggle-content .collateral-accordion ::text'
        return response.css(description_css).extract()

    def product_description(self, response):
        description = list()
        raw_description = self.product_raw_description(response)
        for information in raw_description:
            is_care = False
            for care in self.care:
                if care in information:
                    is_care = True
                    break
            if not is_care and information.strip():
                description.append(information.strip())
        return description

    def product_care(self, response):
        description = self.product_raw_description(response)
        care_description = list()
        for information in description:
            for care in self.care:
                if care in information:
                    care_description.append(information.strip())
        return care_description

    def product_retailer_sku(self, response):
        retailer_sku_css = '#prodSKU::text'
        return response.css(retailer_sku_css).extract_first()

    def product_raw(self, response):
        config_regex = 'new Product.Config\((.*?)\)|$'
        config_css = '#product-options-wrapper > script:nth-child(2)::text'
        config = response.css(config_css).extract_first()
        config = re.findall(config_regex, config)[0]
        return json.loads(config)
