import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from skuscraper.parsers.genders import Gender
from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify

class Mixin:
    retailer = 'smilodox'
    default_brand = "Smilodox"


class MixinUS(Mixin):
    allowed_domains = ["smilodox.com"]
    retailer = Mixin.retailer + "-us"
    market = 'US'
    retailer_currency = 'USD'
    start_urls = ['https://www.smilodox.com/en/?Currency=USD']
    deny = [r'/de/']


class SmilodoxParseSpider(BaseParseSpider):
    description_css = '.product_description h4 + p::text'
    price_css = '.price_single'
    care_css = '.product_description p+ p::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)

        garment['meta'] = {'requests_queue': self.skus_requests(response), 'varients': []}
        if not garment['meta']['requests_queue']:
            garment['skus'] = self.one_sku(response)

        return self.next_request_or_garment(garment)

    def parse_raw_skus(self, response):
        garment = response.meta['garment']
        raw_skus = re.findall('variations = (.+?);}if', response.text, re.MULTILINE | re.DOTALL)
        if raw_skus:
            raw_skus = json.loads(raw_skus[0])
            garment['skus'] = self.raw_skus(raw_skus)
            garment['meta']['requests_queue'] += self.varient_requests(response)

        return self.next_request_or_garment(garment)

    def parse_varient_map(self, response):
        garment = response.meta['garment']
        varient_map = re.findall('] = (.+?);}', response.text, re.MULTILINE | re.DOTALL)[0]
        garment['meta']['varients'] += self.product_varients(json.loads(varient_map))
        if not garment['meta']['requests_queue']:
            self.skus(garment)

        return self.next_request_or_garment(garment)

    def skus_requests(self, response):
        url = clean(response.css('.div_plenty_attribute_selection script::attr(src)'))
        return [response.follow(url[0], callback=self.parse_raw_skus)] if url else []

    def varient_requests(self, response):
        urls = re.findall('scripts.push\("(.+?)"\);', response.text, re.MULTILINE | re.DOTALL)
        return [response.follow(url, self.parse_varient_map, dont_filter=True)
                for url in urls if 'attribute_id' in url]

    def product_name(self, response):
        return clean(response.css(".product-content .h3::text"))[0]

    def product_id(self, response):
        return clean(response.css('#single .hidden-xs span::text'))[0]

    def image_urls(self, response):
        return clean(response.css(".product-img-box .single-thumbs li::attr(data-img-link)"))

    def product_category(self, response):
        return clean(response.css('.breadcrumb a::text'))

    def product_price(self, response):
        return clean(response.css('.price_single .Price::text'))[0]

    def product_currency(self, response):
        return clean(response.css('.price_single::text'))[0]

    def product_gender(self, response):
        soup = soupify(self.product_category(response))
        soup += soupify(list(part[1] for part in self.add_trail(response)))
        return self.gender_lookup(soup.lower()) or Gender.ADULTS.value

    def previous_prices(self, response):
        return clean(response.css('.uvp.hidden-xs::text'))

    def raw_skus(self, raw_skus):
        skus = {}
        for sku_id, raw_sku in raw_skus.items():
            money_strs = [raw_sku['variationPrice'], raw_sku['recommendedRetailPrice'],
            self.retailer_currency]
            sku = self.product_pricing_common(None, money_strs)
            sku['varient_ids'] = raw_sku['valueIds']
            skus.update({sku_id: sku})
        return skus

    def skus(self, garment):
        varient_map = garment['meta']['varients']
        skus = {}
        for _, sku in garment['skus'].items():
            sku_varients = []
            for varient_id in sku['varient_ids']:
                varient = next((item for item in varient_map if item['id'] == str(varient_id)))
                sku[varient['v_name']] = varient['name']
                sku_varients.append(varient['name'])
            del sku['varient_ids']
            if 'size' not in sku:
                sku_varients.append(self.one_size)
                sku['size'] = self.one_size
            skus.update({soupify(sku_varients, '_'): sku})

        garment['skus'] = skus

    def one_sku(self, respons):
        sku = self.product_pricing_common(respons)
        sku['previous_prices'] = self.previous_prices(respons)
        sku['size'] = self.one_size
        return {self.one_size: sku}

    def product_varients(self, raw_map):
        k_list = ['id', 'name']
        varient_map = []
        for _, value in raw_map['values'].items():
            varient = dict((k, v) for k, v in value.items() if k in k_list)
            varient['v_name'] = raw_map['name'].lower()
            varient_map.append(varient)

        return varient_map


class SmilodoxUSParseSpider(MixinUS, SmilodoxParseSpider):
    name = MixinUS.retailer + '-parse'


class SmilodoxCrawlSpider(BaseCrawlSpider):
    listings_css = ['.header-flex.header-flex--menu']
    deny = []

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny), callback='parse_category'),
    )

    def parse_category(self, response):
        products = clean(response.css('.article_order_form article::attr(data-href)'))
        for product in products:
            yield response.follow(product, self.parse_item,
            meta=self.get_meta_with_trail(response))

        next_page = clean(response.css('.paginator1 a[rel="next"]::attr(href)'))
        if next_page:
            yield response.follow(next_page[0], self.parse_category)


class SmilodoxUSCrawlSpider(MixinUS, SmilodoxCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = SmilodoxUSParseSpider()