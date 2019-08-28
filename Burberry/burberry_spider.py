import re
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

class BurberryLimitsParseSpider(BaseParseSpider):
    description_css = '.accordion-tab_content p::text'
    price_css = '.product-purchase_price::text'
    care_css = '.accordion-tab_sub-item li::text'

    def parse(self, response):
        product_id = self.retailer_sku(response)
        product_item = self.new_unique_garment(product_id)
        if not product_item:
            return

        product_item['name'] = self.product_name(response)
        product_item['brand'] = self.product_brand(response)
        product_item['description'] = self.product_description(response)
        product_item['care'] = self.product_care(response)
        product_item['url'] = response.url
        product_item['image_urls'] = self.image_urls(response)
        product_item['gender'] = self.gender(response)
        product_item['category'] = self.product_category(response)
        product_item['skus'] = self.skus(response)
        if not self.is_product_available(response):
            product_item['out_of_stock'] = True

        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)
        meta['product_item'] = product_item
        url = f"/service/products{response.css('html::attr(data-default-url)').get()}"
        header = {'x-csrf-token': response.css('.csrf-token::attr(value)').get()}
        yield response.follow(url, callback=self.parse_sizes, headers=header, meta=meta)

    def parse_sizes(self, response):
        product_item = response.meta['product_item']
        raw_sizes = [option for option in json.loads(response.text)['options'] if option['type'] == 'size']
        if raw_sizes:
            raw_sizes = raw_sizes[0]['items']
            sizes_unavailable = [size['label'] for size in raw_sizes if not size['isAvailable']]
            for (id, sku) in product_item['skus'].items():
                if sku['size'] in sizes_unavailable:
                    sku['out_of_stock'] = True

        return product_item

    def product_name(self, response):
        return response.css(".product-purchase_name::text").get()

    def retailer_sku(self, response):
        return re.findall('\d+', response.css(".accordion-tab_item-number::text").get())[0]

    def image_urls(self, response):
        raw_urls = response.css(".product-carousel_item noscript img::attr(src)").getall()
        return [f'http:{url.split("?$")[0]}' for url in raw_urls]

    def product_category(self, response):
        raw_categories = response.css('html::attr(data-atg-category)').get()
        return raw_categories.split(r"/")

    def colors(self, response):
        return clean(response.css('.product-purchase_selected::text'))

    def sizes(self, response):
        return response.css('.product-purchase_options label::text').getall()

    def gender(self, response):
        soup = ' '.join(self.product_category(response))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def is_product_available(self, response):
        return not response.css('.isOutOfStock').getall()

    def skus(self, response):
        pricing_common = self.product_pricing_common(response)
        product_sizes = self.sizes(response)
        color = self.colors(response)[0]
        skus = {}
        for size in product_sizes or [self.one_size]:
            sku = {
                "colour": color,
                "size": size
            }
            sku.update(pricing_common)
            skus[f"{color}_{size}"] = sku
        return skus

class BurberryCNParseSpider(BurberryLimitsParseSpider, MixinCN):
    name = MixinCN.retailer + '-parse'

class BurberryCrawlSpider(BaseCrawlSpider):
    listings_css = ['.nav-level2_main']
    deny = [r'-looks']
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse_category'),
    )

    def parse_category(self, response):
        products = clean(response.css(".products_container .product a.product_link::attr(href)"))
        for product in products:
            yield response.follow(product, self.parse_item)

class BurberryLimitsCNCrawlSpider(MixinCN, BurberryCrawlSpider):
    name = MixinCN.retailer + '-crawl'
    parse_spider = BurberryCNParseSpider()
