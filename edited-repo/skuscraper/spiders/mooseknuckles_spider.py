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
    raw_description_css = '.tab-content .std::text, .tab-content li::text'
    care_css = '.tab-content li::text'
    price_css = '.price-info .price ::text'

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
        soup = ' '.join(clean(response.css('.short-description .std::text')) + [response.url])
        return self.gender_lookup(soup) or 'unisex-adults'

    def image_urls(self, response):
        raw_images = clean(response.css('.product-img-box script::text'))[0].split('=')[-1]
        raw_images = json.loads(raw_images)
        if isinstance(raw_images, dict):
            raw_images = sum(raw_images.values(), [])
        images = [i.get('fullimage') for i in raw_images]
        return images or clean(response.css('.product-image-gallery .not-swiper img::attr(src)'))

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        script = self.magento_product_data(response)
        script_json = self.magento_product_map(script)
        skus = {}
        for key, item in script_json.items():
            sku = common_sku.copy()
            if not clean(response.css('.availability .value::text'))[0] == 'In stock':
                sku['out_of_stock'] = True
            sku['colour'] = item[0]['label']
            sku['size'] = item[1]['label']
            skus[key] = sku
        return skus


class MooseKnucklesCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = MooseKnucklesParseSpider()
    listings_css = ['.mega-menu-container .level1', ]
    products_css = ['.product-image', ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
