from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from .base import BaseParseSpider, BaseCrawlSpider, clean


class MixinUK:
    retailer = 'liujo-uk'
    market = 'UK'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/gb']
    gender = 'Women'


class MixinIT:
    retailer = 'liujo-it'
    market = 'IT'
    lang = 'italian'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/it']
    gender = 'Women'


class MixinDE:
    retailer = 'liujo-de'
    market = 'DE'
    lang = 'german'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/de']
    gender = 'Women'


class MixinFR:
    retailer = 'liujo-fr'
    market = 'FR'
    lang = 'french'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/fr']
    gender = 'Women'


class MixinES:
    retailer = 'liujo-es'
    market = 'ES'
    lang = 'spanish'
    allowed_domains = ['liujo.com']
    start_urls = ['http://www.liujo.com/es']
    gender = 'Women'


class LiujoParseSpider(BaseParseSpider):
    price_css = '.price-box'

    def parse(self, response):

        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id[0])
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        # garment['description'], garment['care'] = self.retrieve_care(garment['description'])
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response, sku_id[0])
        garment['gender'] = "Women"

        if self.gender_check(garment['trail']):
            garment['gender'] = 'unisex-kids'

        return garment

    def gender_check(self, trail):
        soup = " ".join([t for _, t in trail or []]).lower()
        return any(child in soup for child in ['kids', 'enfant', 'bambina', 'bebe'])
        # return 'kids' in soup

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
        description = clean(response.css('meta[name=description]::attr(content)'))
        return description + [rd for rd in self.raw_description(response) if not self.care_criteria(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria(rd)]

    def raw_description(self, response):
        description_tab = clean(response.css('meta[name=description]::attr(content)'))
        details_tab = clean(response.css('.details-content ::text'))
        return description_tab+details_tab

    def image_urls(self, response):
        return clean(response.css('.small-preview a::attr(href)'))

    def skus(self, response, sku_id):
        skus = {}
        script_json = self.magento_product_data(response)
        common_sku = self.product_pricing_common_new(response)
        common_sku['size'] = self.one_size

        #  for when there is no size or color e.g. pendants
        if script_json is None:
            skus[sku_id] = common_sku.copy()
            return skus

        script_json = self.magento_product_map(script_json)
        for keys, value in script_json.items():
            sku = common_sku.copy()
            for val in value:
                if val['name'] in ['Color', 'Colore', 'Couleur']:
                    if val['label'] not in ["", 'Color', 'Colore', 'Couleur']:
                        sku['colour'] = val['label']
                if val['name'] in ['Size', "Gr\u00f6\u00dfe", 'Taglia', 'Taille']:
                    sku['size'] = val['label']
            skus[keys] = sku
        return skus

    def product_category(self, response):
        return clean(response.css('.collection-attribute::attr(content)'))


class LiujoCrawlSpider(BaseCrawlSpider):

    category_css = "#site-menu a[target=_self]"
    page_css = "liujo-paginator a"
    product_css = ".product-name a"
    rules = (Rule(LinkExtractor(restrict_css=[category_css, page_css]), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item'))


class LiujoUKParseSpider(LiujoParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class LiujoUKCrawlSpider(LiujoCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = LiujoUKParseSpider()


class LiujoITParseSpider(LiujoParseSpider, MixinIT):
    name = MixinIT.retailer + '-parse'


class LiujoITCrawlSpider(LiujoCrawlSpider, MixinIT):
    name = MixinIT.retailer + '-crawl'
    parse_spider = LiujoITParseSpider()


class LiujoDEParseSpider(LiujoParseSpider, MixinDE):
    name = MixinDE.retailer + '-parse'


class LiujoDECrawlSpider(LiujoCrawlSpider, MixinDE):
    name = MixinDE.retailer + '-crawl'
    parse_spider = LiujoDEParseSpider()


class LiujoFRParseSpider(LiujoParseSpider, MixinFR):
    name = MixinFR.retailer + '-parse'


class LiujoFRCrawlSpider(LiujoCrawlSpider, MixinFR):
    name = MixinFR.retailer + '-crawl'
    parse_spider = LiujoFRParseSpider()


class LiujoESParseSpider(LiujoParseSpider, MixinES):
    name = MixinES.retailer + '-parse'


class LiujoESCrawlSpider(LiujoCrawlSpider, MixinES):
    name = MixinES.retailer + '-crawl'
    parse_spider = LiujoESParseSpider()
