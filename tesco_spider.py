import re
import json
from scrapy import Selector
from scrapy.spiders import Rule
from scrapy.http import Request
from w3lib.url import add_or_replace_parameter
from scrapy.linkextractors import LinkExtractor
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'tesco-uk'
    market = 'UK'
    currency = '£'
    allowed_domains = ['tesco.com']
    start_urls = ['https://www.tesco.com/direct/clothing/']
    gender_map = [
        ('women', 'women'),
        ('men', 'men'),
        ('boy', 'boys'),
        ('girl', 'girls'),
        ('kid', 'unisex-kids')
    ]


class TescoParseSpider(BaseParseSpider, Mixin):

    name = Mixin.retailer + '-parse'

    def parse(self, response):

        product_json, product_sku_json = self.raw_product(response)
        if product_json['prices'].get('error'):
            return
        product_id = self.product_id(product_json)

        current_product_sku_id = self.product_sku_id(product_sku_json)
        remaining_product_sku_ids = self.remaining_product_sku_ids(product_json, current_product_sku_id)

        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)

        requests = []
        garment['skus'] = {}
        garment['image_urls'] = []
        if self.homeware(garment):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(garment)

        garment['skus'], garment['image_urls'] = self.default_sku(response, product_json, product_sku_json)

        for sku_id in remaining_product_sku_ids:
            product_sku_url = add_or_replace_parameter(response.url, 'skuId', sku_id)
            requests.append(Request(product_sku_url, self.parse_skus, dont_filter=True))

        garment['meta'] = {'requests_queue': requests}

        return self.next_request_or_garment(garment)

    def parse_skus(self, response):
        garment = response.meta['garment']
        product_json, product_sku_json = self.raw_product(response)
        if not product_sku_json.get('prices'):
            return self.next_request_or_garment(garment)

        price_string, pprice_string = self.sku_prices(product_json, product_sku_json)
        prices = self.product_pricing_common_new(response, [price_string, pprice_string])
        sku_id = product_sku_json['id']
        garment['skus'][sku_id] = {
            "merch_info": "Earn " + str(product_sku_json['prices']["clubcardPoints"]) + " Clubcard points"
        }
        garment['skus'][sku_id].update(prices)
        if product_sku_json['attributes'].get('colour'):
            garment['skus'][sku_id].update({'colour': product_sku_json['attributes']['colour']})
            garment['skus'][sku_id].update({'size': product_sku_json['attributes']['size']})

        for media in product_sku_json['mediaAssets']['skuMedia']:
            if media["mediaType"] == "Large":
                garment['image_urls'].append(media['src'].replace("?$[preset]$", "/"))

        return self.next_request_or_garment(garment)

    def product_id(self, product_json):
        return product_json.get('id')

    def product_sku_id(self, product_sku_json):
        return product_sku_json.get('id')

    def remaining_product_sku_ids(self, product_json, current_product_sku_id):
        current_product_sku_ids = []
        for link in product_json['links']:
            if link['type'] == "sku" and link['rel'] == "childSku":
                current_product_sku_ids.append(link['id'])

        return list(set(current_product_sku_ids) - set([current_product_sku_id]))

    def product_name(self, response):
        return clean(response.css('[itemprop="name"]::text'))[0]

    def product_description(self, response):
        return clean(response.css('[itemprop="description"]::text, [itemprop="description"] p::text'))

    def product_category(self, response):
        return clean(response.css('#breadcrumb-v2 [itemprop="title"]::text'))[1:]

    def product_care(self, response):
        return clean(response.css('.product-spec-label::text, .product-spec-value::text'))

    def product_gender(self, garment):
        soup = garment['category']
        soup = ' '.join(soup).lower()
        for gender_string, gender in self.gender_map:
            if gender_string in soup:
                return gender

        return 'unisex-adults'

    def homeware(self, garment):
        return garment.get('industry') or 'Homeware' in garment['category']

    def raw_product(self, response):
        raw_product = response.css('script').extract()
        raw_product = ''.join(raw_product)
        raw_product = re.findall('product =\n({.*}),\nsku =\n({.*}),\nassetData', raw_product, flags=re.DOTALL)[0]
        return json.loads(raw_product[0]) , json.loads(raw_product[1])

    def default_sku(self, response, product_json, product_sku_json):
        if not product_sku_json.get('prices'):
            return
        price_string, pprice_string = self.sku_prices(product_json, product_sku_json)
        prices = self.product_pricing_common_new(response, [price_string, pprice_string])
        return self.read_default_sku(product_sku_json, prices)

    def read_default_sku(self, product_sku_json, prices):
        sku = {}
        image_urls = []
        sku_id = product_sku_json['id']
        sku[sku_id] = {
            "merch_info": "Earn " + str(product_sku_json['prices']["clubcardPoints"]) + " Clubcard points"
        }
        sku[sku_id].update(prices)
        if product_sku_json['attributes'].get('colour'):
            sku[sku_id].update({'colour': product_sku_json['attributes']['colour']})
        if product_sku_json['attributes'].get('size'):
            sku[sku_id].update({'size': product_sku_json['attributes']['size']})

        for media in product_sku_json['mediaAssets']['skuMedia']:
            if media["mediaType"] == "Large":
                image_urls.append(media['src'])

        return sku, image_urls

    def sku_prices(self, product_json, product_sku_json):
        prices = product_sku_json['prices']
        product_prices = product_json['prices']

        price_string = self.currency + prices.get('price', prices.get('fromPrice'))
        pprice_string = self.currency + prices.get('was', product_prices.get('price', product_prices.get('toPrice')))
        return price_string, pprice_string


class TescoCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer + '-crawl'
    parse_spider = TescoParseSpider()

    PRODUCT_CATEGORY_CSS = '.product'
    STANDARD_PRODUCT_RANGE = 20

    pagination_url = "https://www.tesco.com/direct/blocks/catalog/productlisting/infiniteBrowse.jsp?catId={0}&offset={1}"

    rules = (
        Rule(LinkExtractor(restrict_css=PRODUCT_CATEGORY_CSS), callback='parse_products'),
    )

    def parse_products(self, response):
        data_count = response.css('#listing::attr(data-maxcount)').extract_first()
        if not data_count:
            return
        requests = []
        product_count = int(data_count)
        for offset in range(0, product_count, self.STANDARD_PRODUCT_RANGE):
            category_id = response.css('.products-wrapper::attr(data-endecaid)').extract_first()
            pagination_url = self.pagination_url.format(category_id, offset)
            requests.append(Request(pagination_url, self.parse_pagination_products, dont_filter=True))
        return requests

    def parse_pagination_products(self, response):
        requests = []
        for product_url in self.product_urls(response):
            requests.append(Request(response.urljoin(product_url), self.parse_spider.parse, dont_filter=True))
        return requests

    def product_urls(self, response):
        product_card_css = '.image-container .thumbnail::attr(href)'
        product_urls = clean(response.css(product_card_css))
        if product_urls:
            return product_urls
        products_html = response.text.replace('\n', '').replace('\\', '')
        products_html = Selector(text=products_html)
        product_urls = clean(products_html.css(product_card_css))
        if product_urls:
            return product_urls
        return []
