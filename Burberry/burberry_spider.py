import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from skuscraper.parsers.genders import Gender
from .base import BaseParseSpider, BaseCrawlSpider, clean

class Mixin:
    retailer = 'burberry'
    default_brand = "Burberry"

class MixinCN(Mixin):
    allowed_domains = ["cn.burberry.com"]
    retailer = Mixin.retailer + "-cn"
    market = "CN"
    start_urls = ['https://cn.burberry.com/']

class BurberryParseSpider(BaseParseSpider):
    description_css = '.accordion-tab_content p::text'
    price_css = '.product-purchase_price::text'
    care_css = '.accordion-tab_sub-item li::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)

        garment['skus'] = {}
        garment['meta'] = {}
        garment['meta']['requests_queue'] = [self.raw_data_request(response)]
        if not self.is_product_available(response):
            garment['out_of_stock'] = True

        garment['meta']['requests_queue'] += self.color_requests(response, self.request_header(response))
        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)
        garment['meta']['requests_queue'] += [self.raw_data_request(response)]
        garment['meta']['pricing_common'] = self.product_pricing_common(response)
        return self.next_request_or_garment(garment)

    def parse_raw_data(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        if not garment['category']:
            garment['category'] = self.raw_category(json.loads(response.text))
        return self.next_request_or_garment(garment)

    def product_name(self, response):
        return clean(response.css(".product-purchase_name::text"))[0]

    def product_id(self, response):
        return re.findall('\d+', clean(response.css(".accordion-tab_item-number::text"))[0])[0]

    def image_urls(self, response):
        raw_urls = clean(response.css(".product-carousel_item noscript img::attr(src)"))
        return [f'http:{url.split("?$")[0]}' for url in raw_urls]

    def product_category(self, response):
        raw_categories = clean(response.css('html::attr(data-atg-category)'))
        if not raw_categories:
            return []
        return raw_categories[0].split(r"/")

    def raw_category(self, raw_data):
        category = raw_data['dataDictionaryProductInfo']['categoryMerch']
        return category.split('|')

    def product_gender(self, response):
        soup = ' '.join(self.product_category(response))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def is_product_available(self, response):
        return not clean(response.css('.isOutOfStock'))

    def raw_data_request(self, response):
        url = f"/service/products{clean(response.css('html::attr(data-default-url)'))[0]}"
        return response.follow(url, callback=self.parse_raw_data, headers=self.request_header(response))

    def color_requests(self, response, headers):
        urls = clean(response.css('.product-purchase_selector-colour a::attr(href)'))
        return [response.follow(url, self.parse_color, headers=headers)
         for url in urls if not self.product_id(response) in url]

    def request_header(self, response):
        return {'x-csrf-token': clean(response.css('.csrf-token::attr(value)'))[0]}

    def skus(self, response):
        raw_data = json.loads(response.text)
        raw_sizes = [option for option in raw_data['options'] if option['type'] == 'size']
        raw_colors = [option for option in raw_data['options'] if option['type'] == 'colour'][0]
        selected_colour = [colour['label'] for colour in raw_colors['items'] if colour['value'] == raw_colors['currentValue']][0]

        common_sku = {
            "colour": selected_colour,
            "price": raw_data['price'],
            "currency": raw_data['currency']
        }
        skus = {}
        if raw_sizes:
            raw_sizes = raw_sizes[0]['items']
            for size in raw_sizes:
                sku = {"size": size['label']}
                sku.update(common_sku)
                if not size['isAvailable']:
                    sku['out_of_stock'] = True
                skus[f"{selected_colour}_{size['label']}"] = sku
        else:
            common_sku.update({"size": self.one_size})
            skus[f"{selected_colour}_{self.one_size}"] = common_sku
        return skus

class BurberryCNParseSpider(BurberryParseSpider, MixinCN):
    name = MixinCN.retailer + '-parse'

class BurberryCrawlSpider(BaseCrawlSpider):
    listings_css = ['.nav-level2_main']
    deny = [r'-looks']
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse_category'),
    )

    def parse_category(self, response):
        header = {'x-csrf-token': clean(response.css('.csrf-token::attr(value)'))[0]}
        pagging_urls = clean(response.css('li.shelf::attr(data-all-products)'))
        for url in pagging_urls:
            yield response.follow(url, callback=self.parse_products, headers=header)

    def parse_products(self, response):
        raw_products = json.loads(response.text)
        for product in raw_products:
            yield response.follow(product['link'], self.parse_item)

class BurberryCNCrawlSpider(MixinCN, BurberryCrawlSpider):
    name = MixinCN.retailer + '-crawl'
    parse_spider = BurberryCNParseSpider()
