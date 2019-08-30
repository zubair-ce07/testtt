import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from skuscraper.parsers.genders import Gender
from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify

class Mixin:
    retailer = 'burberry'
    default_brand = "Burberry"

class MixinCN(Mixin):
    allowed_domains = ["cn.burberry.com"]
    retailer = Mixin.retailer + "-cn"
    market = "CN"
    start_urls = ['https://cn.burberry.com/']

class BurberryParseSpider(BaseParseSpider):
    product_url_t = 'https://cn.burberry.com/service/products%s'
    description_css = '.accordion-tab_content p::text'
    care_css = '.accordion-tab_sub-item li::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['category'] = self.product_category(response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = []

        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.color_requests(response)}
        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta['garment']
        raw_product = json.loads(response.text)
        garment['image_urls'] += self.image_urls(raw_product)
        garment['skus'].update(self.skus(raw_product))
        return self.next_request_or_garment(garment)

    def product_name(self, response):
        return clean(response.css(".product-purchase_name::text"))[0]

    def product_id(self, response):
        return clean(response.css('.accordion-tab_item-number::text').re_first('\d+'))

    def image_urls(self, raw_product):
        raw_urls = [img['img']['src'] for img in raw_product['carousel'] if img.get('img', None)]
        return [f'http:{url}' for url in raw_urls]

    def product_category(self, response):
        raw_categories = clean(response.css('html::attr(data-atg-category)'))
        return raw_categories[0].split("/") if raw_categories else []

    def product_gender(self, response):
        soup = soupify(self.product_category(response))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def color_requests(self, response):
        urls = clean(response.css('.product-purchase_selector-colour a::attr(href)'))
        headers = {'x-csrf-token': clean(response.css('.csrf-token::attr(value)'))[0]}
        return [response.follow(self.product_url_t % (url), self.parse_color,
        headers=headers) for url in urls]

    def skus(self, raw_data):
        common_sku = self.product_pricing_common(None, [raw_data['price'],
        raw_data['currency'], raw_data['dataDictionaryProductInfo']['priceDiscount']])

        raw_varients = raw_data['findInStore']
        raw_sizes = raw_varients.get('size', {'items': [{'label': self.one_size}]})['items']
        selected_colour = raw_varients['colour']['value']
        common_sku["colour"] = selected_colour

        skus = {}
        for size in raw_sizes:
            sku = {"size": size['label']}
            sku.update(common_sku)
            if not ((size.get('isAvailable', None) or raw_data['isOutOfStock'])):
                sku['out_of_stock'] = True
            skus[f"{selected_colour}_{size['label']}"] = sku

        return skus

class BurberryCNParseSpider(BurberryParseSpider, MixinCN):
    name = MixinCN.retailer + '-parse'

class BurberryCrawlSpider(BaseCrawlSpider):
    listings_css = ['.nav-level2_main']
    deny = [r'-looks']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse_pagination'),
    )

    def parse_pagination(self, response):
        header = {'x-csrf-token': clean(response.css('.csrf-token::attr(value)'))[0]}
        pagging_urls = clean(response.css('li.shelf::attr(data-all-products)'))
        for url in pagging_urls:
            yield response.follow(url, callback=self.parse_category,
            headers=header, meta=self.get_meta_with_trail(response))

    def parse_category(self, response):
        for product in json.loads(response.text):
            yield response.follow(product['link'], self.parse_item, meta=self.get_meta_with_trail(response))

class BurberryCNCrawlSpider(MixinCN, BurberryCrawlSpider):
    name = MixinCN.retailer + '-crawl'
    parse_spider = BurberryCNParseSpider()
