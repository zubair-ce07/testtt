from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'liujo-uk'
    market = 'UK'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/gb']
    gender = 'Women'


class LiujoParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_css = '.price-box'

    def parse(self, response):

        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id[0])
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['description'], garment['care'] = self.retrieve_care(garment['description'])
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response, sku_id[0])
        garment['gender'] = Mixin.gender
        if not self.gender_check(garment['trail']):
            garment['gender'] = 'unisex-kids'

        return garment

    def gender_check(self, trail):
        kids_url = ["http://www.liujo.com/gb/kids.html",
                    "http://www.liujo.com/gb/kids/junior.html",
                    "http://www.liujo.com/gb/kids/newborn.html",
                    "http://www.liujo.com/gb/kids/baby.html",
                    "http://www.liujo.com/gb/kids/teen.html"]
        for url in trail:
            if len(list(set(kids_url).intersection(url))) != 0:
                return False
        return True

    # empty function because care fields are mixed with details and are extracted after we retrieve details using function retrieve_care
    def product_care(self, response):
        return []

    def retrieve_care(self, details):
        care = []
        for detail in details:
            if self.care_criteria(detail):
                care.append(detail)
        details = list(set(details) ^ set(care))
        return details, care

    def product_id(self, response):
        return clean(response.css('.product-ids::text'))

    def product_name(self, response):
        return clean(response.css('.product-name>h1::text'))

    def product_description(self, response):
        description_tab = clean(response.css('meta[name=description]::attr(content)'))
        details_tab = clean(response.css('.details-content ::text'))
        return description_tab+details_tab

    def image_urls(self, response):
        return clean(response.css('.small-preview a::attr(href)'))

    def skus(self, response, sku_id):
        skus = {}
        script_json = self.magento_product_data(response)
        price = self.product_pricing_common_new(response)
        currency = price['currency']
        price = price['price']

        #  for when there is no size or color e.g. pendants
        if script_json is None:
            skus[sku_id] = {"size": self.one_size, "price": price, "currency": currency}
            return skus

        script_json = self.magento_product_map(script_json)
        for keys, value in script_json.items():
            dic_key = sku_id + "_" + keys
            for val in value:
                if val['name'] == 'Color':
                    if not dic_key in skus.keys():
                        skus[dic_key] = {"size": self.one_size, "price": price, "currency": currency}
                if val['name'] == 'Size':
                    size = val['label']
                    skus[dic_key] = {"size": size, "price": price, "currency": currency}

        return skus

    def product_category(self, response):
        return clean(response.css('.collection-attribute::attr(content)'))


class LiujoCrawlSpider(BaseCrawlSpider, Mixin):

    name = Mixin.retailer + '-crawl'
    category_css = "#site-menu a[target=_self]"
    page_css = "liujo-paginator a"
    product_css = ".product-name a"
    parse_spider = LiujoParseSpider()
    rules = (Rule(LinkExtractor(restrict_css=[category_css, page_css]), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'))
