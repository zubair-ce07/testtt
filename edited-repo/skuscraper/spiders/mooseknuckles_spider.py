import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    market = 'US'
    retailer = 'mooseknuckles-us'
    allowed_domains = ['mooseknucklescanada.com']
    start_urls = ['https://www.mooseknucklescanada.com/us']


class MooseKnucklesParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    care_css = '.tab-content li::text'
    description_css = '.tab-content .std::text'
    price_css = '.price-info .price ::text'

    gender_map = (
        ('women', 'women'),
        ('womens', 'women'),
        ('men', 'men'),
        ('mens', 'men'),
        ('ladies', 'women'),
    )

    def parse(self, response):
        pid = self.magento_product_id(response)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(response)
        garment['skus'] = self.skus(response)
        return garment

    def product_name(self, response):
        return clean(response.css('.product-name h1::text'))[0]

    def product_brand(self, response):
        return 'Moose Knuckles'

    def product_gender(self, response):
        soup = " ".join(clean(response.css('.short-description .std::text')) + [response.url]).lower()
        for gender_str, gender in self.gender_map:
            if gender_str in soup:
                return gender
        return 'unisex-adults'

    def image_urls(self, response):
        images_script = clean(response.css('.product-img-box script::text'))[0].split('=')[-1]
        img_json = json.loads(images_script)
        if isinstance(img_json, dict):
            img_json = sum(img_json.values(), [])
        images = [i.get('fullimage') for i in img_json]
        return images if images else clean(response.css('.product-image-gallery .not-swiper img::attr(src)'))

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        script = self.magento_product_data(response)
        script_json = self.magento_product_map(script)
        skus = {}
        for key, item in script_json.items():
            for dimension in item:
                sku = common_sku.copy()
                if not clean(response.css('.availability .value::text'))[0] == 'In stock':
                    sku['out_of_stock'] = True
                if dimension['name'] == 'Colour':
                    sku['colour'] = dimension['label']
                elif dimension['name'] == 'Size':
                    sku['size'] = dimension['label']
                skus[key] = sku
        return skus


class MooseKnucklesCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = MooseKnucklesParseSpider()
    listings_css = ['.mega-menu-container .level1', ]
    products_css = ['.product-image', ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, ), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
