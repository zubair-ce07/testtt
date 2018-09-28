from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'selectfashion-uk'
    market = 'UK'

    start_urls = ['https://www.selectfashion.co.uk/']
    allowed_domains = ['selectfashion.co.uk']
    gender = 'women'


class SelectFashionParser(Mixin, BaseParseSpider):
    name = Mixin.retailer + '-parse'

    raw_description_css = '#item-description ::text'
    price_css = ".product-price"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.gender_lookup(self.gender)
        garment['merch_info'] = self.merch_info(response)
        garment['skus'] = self.skus(response)
        return self.next_request_or_garment(garment)

    def image_urls(self, response):
        image_urls = []
        images = clean(response.css('.imageThumb img::attr(src)'))
        for image_url in images:
            image_url.replace('resizeandpad:200:300', '')
            image_urls.append(response.urljoin(image_url))
        return image_urls

    def merch_info(self, response):
        return clean(response.xpath('//p[@class="web-exclusive-banner"]/text()'))

    @staticmethod
    def product_id(response):
        return clean(response.css('#product_id ::attr(value)'))[0]

    @staticmethod
    def product_name(response):
        return clean(response.css('.product-title ::text'))[0]

    @staticmethod
    def product_category(response):
        return clean(response.css('.breadcrumb a::text'))

    def skus(self, response):
        skus = {}

        sku = self.product_pricing_common(response)
        sku['colour'] = colour = self.colour_detect(response)

        for size_sel in response.css('.s-size a'):
            sku_size = sku.copy()

            size = clean(size_sel.css('::text'))[0]
            sku_size['size'] = self.one_size if size == 'One' else size

            out_of_stock = clean(size_sel.css('::attr(class)'))[0]
            sku_size['out_of_stock'] = False if out_of_stock == "available" else True

            sku_id = f"{colour}_{sku_size['size']}"
            skus.update({sku_id: sku_size})

        return skus

    def colour_detect(self, response):
        detail_description = clean(response.css('.details-description p::text'))[0]
        colour = detail_description.split('_')[1]
        colour = self.detect_colour(colour)

        if colour is '':
            colour = clean(response.css(self.raw_description_css))[0]
            colour = self.detect_colour(colour)

        return colour


class SelectFashionCrawler(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = SelectFashionParser()

    listing_css = [
        '.dropdown-menu-link',
        '.paging_next a'

    ]
    product_css = ['.ac_gtm_product_click']

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css), callback='parse'
             ),
        Rule(
            LinkExtractor(restrict_css=product_css), callback='parse_item'
        )
    )
