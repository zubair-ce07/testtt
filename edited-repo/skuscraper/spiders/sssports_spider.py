import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    market = 'US'
    retailer = 'sssports-us'
    allowed_domains = ['sssports.com']
    start_urls = ['http://www.sssports.com']


class SssportsParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    raw_description_css = '[itemprop="description"] ::text'
    price_css = '.price-box ::text'

    size_re = 'ize\",\"options\":(.+?),\"position'
    colour_re = 'Colour\",\"options\":(.+?),\"position'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.image_urls(response)

        if response.css('.error'):
            garment['out_of_stock'] = True
        else:
            garment['skus'] = self.skus(response)
        return garment

    def product_id(self, response):
        return clean(response.css('[data-product-id]::attr(data-product-id)'))[0]

    def product_name(self, response):
        return clean(response.css('div[itemprop="name"] h2::text'))[0]

    def product_brand(self, response):
        return clean(response.css('[itemprop="brand"] ::text'))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumbs li ::text'))[1:-1]

    def product_gender(self, garment):
        soup = ' '.join(garment['category'] + [garment['name']] + garment['description'])
        return self.gender_lookup(soup) or 'unisex-adults'

    def image_urls(self, response):
        raw_images = clean(response.css('.sss-thumb-image-link img::attr(src)'))
        return [image.replace('/dpr_auto,f_auto,q_70,w_215/d_coming-soon.jpg', '') for image in raw_images]

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        raw_sku = response.xpath('//script[contains(., "jsonConfig")]/text()')
        if raw_sku:
            raw_colour = json.loads(raw_sku.re(self.colour_re)[0])
            common_sku['colour'] = raw_colour[0]['label']
            raw_sizes = raw_sku.re(self.size_re)
            raw_sizes = json.loads(raw_sizes[0]) if raw_sizes else raw_sizes

            for raw_size in raw_sizes:
                sku = common_sku.copy()
                sku['size'] = raw_size['label']
                if not raw_size['products']:
                    sku['out_of_stock'] = True
                skus[f'{sku["colour"]}_{sku["size"]}'] = sku

        if not skus:
            common_sku['size'] = self.one_size
            sku_id = f'{common_sku["colour"]}_{self.one_size}' if raw_sku else self.one_size
            skus[sku_id] = common_sku
        return skus


class sssportsCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = SssportsParseSpider()
    listings_css = ['.item-footer', '.pages-item-next']
    products_css = ['.product-item-photo']
    deny_re = [
        '/mens/equipment/fitness-equipment',
        '/brands',
        '/sports',
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
