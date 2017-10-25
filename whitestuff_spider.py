import re
import json
from scrapy import Selector
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean
from w3lib.url import url_query_cleaner, url_query_parameter, add_or_replace_parameter, urljoin


class Mixin:
    retailer = 'whitestuff'
    market = 'UK'
    allowed_domains = ['whitestuff.com']
    start_urls = ['https://www.whitestuff.com']
    gender_map = [
        ('women', 'women'),
        ('men', 'men'),
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('kid', 'unisex-kids')
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

        if self.homeware(garment):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(garment)
        request_url = clean(response.css('.product-form script::attr(src)'))[0]
        request = self.skus_request(request_url)
        garment['meta'] = {'requests_queue': request}
        return self.next_request_or_garment(garment)

    def skus_request(self, request_url):
        return [Request(request_url, self.parse_skus, dont_filter=True)]

    def parse_skus(self, response):
        skus = self.extract_skus(response)
        garment = response.meta['garment']
        if skus:
            garment['skus'] = skus
        else:
            garment['out_of_stock'] = True
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('[itemprop="sku"]::text'))[0]

    def product_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]

    def product_description(self, response):
        description = clean(response.css('.product-info__desc::text'))
        return description if description else []

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

    def extract_skus(self, response):
        skus = {}
        response_json = re.findall('({.*})', response.text, flags=re.DOTALL)
        response_json = self.clean_json(response_json[0])
        response_json = re.sub(r"(?<!\\)\\'", "'", response_json)
        response_json = json.loads(response_json)
        if response_json['productPrice'] == "N/A" or not response_json['inStock']:
            return
        raw_skus = response_json['productVariations']
        for sku_key in raw_skus:
            sku = raw_skus[sku_key]
            if sku['salePrice'] == "N/A" or sku['listPrice'] == "N/A":
                continue
            sku_id = sku['productSKU']
            skus[sku_id] = {'colour': sku['colour'], 'size': sku['size'], 'out_of_stock': sku["inStock"]}
            price = self.product_pricing_common_new(response, [sku.get('salePrice'), sku.get('listPrice')])
            skus[sku_id].update(price)
        return skus

    def clean_json(self, json):
        return json.replace('//this is temporary until the feature is supported in the backoffice','')

    def homeware(self, garment):
        return 'Homeware' in garment['category']


class WhiteStuffCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = WhiteStuffParseSpider()
    listing_css = ['#js-header-navbar']
    deny_paths = ['explore/.*', 'kitchen/.*']
    products_url = "https://fsm.attraqt.com/zones-js.aspx?siteId={0}&pageurl={1}&zone0=banner&zone1=category&culture={2}&currency={3}&language={4}&config_categorytree={5}&config_category={6}&config_region={7}"

    rules = (
            Rule(LinkExtractor(restrict_css=listing_css, deny=deny_paths), callback='parse_products'),
    )

    def parse_products(self, response):
        config = re.findall('JSON.parse\(\'(\{.*\}})', response.text, flags=re.DOTALL)
        config_category_tree = re.findall('categorytree = \"([A-Za-z0-9_\./\\-]*)\"', response.text,
                                          flags=re.DOTALL)
        if not config or not config_category_tree:
            return
        config = config[0]
        page_url = response.url
        config_category_tree = config_category_tree[0]
        site_id, culture, currency, language, config_region = self.products_url_values(config)
        config_category = config_category_tree.split('/')[1]
        request_to_product_url = self.products_url.format(site_id, page_url, culture, currency, language,
                                                          config_category_tree, config_category, config_region)
        return Request(url=request_to_product_url, callback=self.parse_products_list, dont_filter=True)

    def parse_products_list(self, response):
        products_html = self.raw_products_response(response)
        product_urls = products_html.css('.product-tile__title a::attr(href)').extract()

        for product_url in product_urls:
            url = urljoin(self.start_urls[0],product_url)
            yield Request(url, callback=self.parse_spider.parse, dont_filter=True)

        page_next_off = clean(products_html.css('.pagnNext-off'))
        if page_next_off:
            return

        page_url = url_query_parameter(response.url, 'pageurl')
        current_page = url_query_parameter(page_url, 'esp_pg', '1')
        page_url = add_or_replace_parameter(page_url, 'esp_pg', str(int(current_page) + 1))
        pagination_url = add_or_replace_parameter(response.url, 'pageurl', page_url)
        return Request(url=pagination_url, callback=self.parse_products_list, dont_filter=True)

    def raw_products_response(self, response):
        product_list_json = re.findall('LM.buildZone\(({.*?})\)', response.text, flags=re.DOTALL)
        products_html = json.loads(product_list_json[1])['html']
        return Selector(text=products_html)

    def products_url_values(self, config):
        config_json = json.loads(config)
        site_id = config_json['endpoit']['site']
        culture = config_json['localization']['culture']
        currency = config_json['localization']['currency']
        language = config_json['localization']['language']
        config_region = config_json['config']['region']
        return site_id, culture, currency, language, config_region
