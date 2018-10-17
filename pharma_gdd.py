# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.spiders import CrawlSpider, Rule


class ProductItem(scrapy.Item):
    category = scrapy.Field()
    segment_1 = scrapy.Field()
    segment_2 = scrapy.Field()
    segment_3 = scrapy.Field()
    segment_4 = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    form = scrapy.Field()
    ean = scrapy.Field()
    image_urls = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    @staticmethod
    def fetch_images(product_gallery, loader_context):
        return [loader_context.get(
            'response').urljoin(i.replace('/thumbnails/70/', '/thumbnails/400/'))
                for i in product_gallery]

    @staticmethod
    def clean(value):
        value[0] = value[0].replace(u'\xa0', u' ')
        return value[0].strip()

    image_urls_in = fetch_images

    image_urls_out = Identity()
    brand_out = clean
    price_out = clean


class PharmaGddSpider(CrawlSpider):
    name = 'pharma_gdd'
    allowed_domains = ['www.pharma-gdd.com']

    rules = (
        Rule(LinkExtractor(restrict_css=['.menu a', '.border_nav a', '[rel="next"]']),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=['.product-title a']), callback='parse_product'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 1.25
    }

    start_urls = ['https://www.pharma-gdd.com/']

    def parse_product(self, response):
        product_loader = ProductLoader(item=ProductItem(), response=response)

        product_loader.add_css('name', '.row h1::text')
        product_loader.add_css('price', '.value-price::text')
        product_loader.add_css('brand', '.product-brand a::text')
        product_loader.add_css('image_urls', '.photo-thumbs img::attr(data-src)')

        product_loader.add_value('ean', response.xpath(
            '//script[contains(text(), "sku")]').re(r'sku":"(\d+)"'))
        
        category, segments = self.fetch_categories(response)
        product_loader.add_value('category', category)

        for key in segments.keys():
            product_loader.add_value(key, segments[key])

        return product_loader.load_item()

    @staticmethod
    def fetch_categories(response):
        segments = {}

        categories = response.css('.breadcrumb [itemprop="name"]::text').extract()
        count = 1

        for category in categories[2:]:
            if count == 5:
                break

            segments['segment_{}'.format(count)] = category
            count += 1

        return categories[1], segments
