import re
import json
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import Rule
from w3lib.url import url_query_cleaner, add_or_replace_parameter, url_query_parameter
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean
from ..parsers.currencyparser import CurrencyParser


class Mixin:
    retailer = 'whitestuff'
    market = 'UK'
    lang = 'en'
    allowed_domains = ['whitestuff.com']
    start_urls = ['https://www.whitestuff.com']
    gender_map = [
        ('women', 'women'),
        ('womens', 'women'),
        ('men', 'men'),
        ('mens', 'men'),
        ('boy', 'boys'),
        ('boys', 'boys'),
        ('girl', 'girls'),
        ('girls', 'girls'),
        ('kid', 'unisex-kids'),
        ('kids', 'unisex-kids')
    ]


class WhiteStuffParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['skus'] = {}
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(garment)
        request_url = clean(response.css('.product-form script::attr(src)'))[0]
        request = self.skus_request(request_url)
        garment['meta'] = {'requests_queue': request}
        return self.next_request_or_garment(garment)

    def skus_request(self, request_url):
        return [Request(request_url, self.parse_skus, dont_filter=True)]

    def parse_skus(self, response):
        garment = response.meta['garment']
        response_json = re.findall('({.*})', response.text, flags=re.DOTALL)
        response_json = self.clean_json(response_json[0])
        response_json = re.sub(r"(?<!\\)\\'", "'", response_json)
        response_json = json.loads(response_json)
        if not response_json['inStock']:
            garment['out_of_stock'] = True
            return self.next_request_or_garment(garment)

        skus = response_json['productVariations']
        for sku_key in skus:
            sku = skus[sku_key]
            currency, price = CurrencyParser.currency_and_price(sku['salePrice']) if sku['salePrice']!="N/A" else ["",""]
            _, previous_prices = CurrencyParser.currency_and_price(sku['listPrice']) if sku['listPrice']!="N/A" else ["",""]
            sku_id = sku['productSKU']
            garment['skus'][sku_id] = {
                'colour': sku['colour'],
                'size': sku['size'],
                'currency': currency,
                'price': price,
                "previous_prices":previous_prices,
                'out_of_stock': sku["inStock"]
            }

        return self.next_request_or_garment(garment)

    def clean_json(self, json):
        return json.replace('//this is temporary until the feature is supported in the backoffice','')

    def product_id(self, response):
        product_id = clean(response.css('[itemprop="sku"]::text'))
        return product_id[0] if product_id else ""

    def product_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]

    def product_description(self, response):
        description = response.css('.product-info__desc::text')
        return clean(description) if description else ""

    def product_category(self, response):
        return clean(response.css('.breadcrumb-list__item-link::text'))[1:]

    def product_care(self, response):
        return clean(response.css('.ish-ca-type::text, .ish-ca-value::text'))

    def product_gender(self, garment):
        soup = garment['category']
        soup = ' '.join(soup).lower()
        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'

    def image_urls(self, response):
        css = '.product-image__main img::attr(src)'
        return [url_query_cleaner(u) for u in clean(response.css(css))]


class WhiteStuffCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = WhiteStuffParseSpider()
    base_url = "https://www.whitestuff.com"
    listing_css = ['#js-header-navbar']
    deny_paths = ['(https://www.whitestuff.com)/((global/explore)|(explore))/.*']
    products_url = "https://fsm.attraqt.com/zones-js.aspx?siteId={0}&pageurl={1}&zone0=banner&zone1=category&culture={2}&currency={3}&language={4}&config_categorytree={5}&config_category={6}&config_region={7}"
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_paths), callback='parse_products'),
    )

    def parse_products(self, response):
        config = re.findall('JSON.parse\(\'(\{.*\}})', response.text, flags=re.DOTALL)
        if not config:
            return
        config_json = json.loads(config[0])
        site_id = config_json['endpoit']['site']
        page_url = response.url
        culture = config_json['localization']['culture']
        currency = config_json['localization']['currency']
        language = config_json['localization']['language']
        config_region = config_json['config']['region']
        config_category_tree = re.findall('categorytree = \"([A-Za-z0-9_\./\\-]*)\"', response.text,
                                          flags=re.DOTALL)[0]
        if config_category_tree:
            config_category = config_category_tree.split('/')[1]
            request_to_product_url = self.products_url.format(site_id, page_url, culture, currency,
                                                                   language, config_category_tree,
                                                                   config_category, config_region)
            yield Request(url=request_to_product_url, callback=self.parse_products_list, dont_filter=True)

    def parse_products_list(self, response):
        product_list_json = re.findall('LM.buildZone\(({.*?})\)', response.text, flags=re.DOTALL)
        product_list_json = product_list_json[1]
        product_list_json = json.loads(product_list_json)
        products_html = product_list_json['html']
        products_selector = Selector(text=products_html)
        product_urls = products_selector.css('.product-tile__title a::attr(href)').extract()
        for product_url in product_urls:
            url = self.base_url + product_url
            yield Request(url, callback=self.parse_spider.parse, dont_filter=True)
        page_next_off = clean(products_selector.css('.pagnNext-off'))
        if not page_next_off:
            page_url = url_query_parameter(response.url, 'pageurl')
            current_page = url_query_parameter(page_url, 'esp_pg', '1')
            page_url = add_or_replace_parameter(page_url, 'esp_pg', str(int(current_page)+1))
            pagination_url = add_or_replace_parameter(response.url, 'pageurl', page_url)
            yield Request(url=pagination_url, callback=self.parse_products_list, dont_filter=True)
