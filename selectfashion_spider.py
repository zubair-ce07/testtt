from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'selectfashion-uk'
    market = 'UK'

    start_urls = ['https://www.selectfashion.co.uk/']
    allowed_domains = ['selectfashion.co.uk']

    gender = Gender.WOMEN.value
    default_brand = "Select Fashion"


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
        garment['merch_info'] = self.merch_info(response)
        garment['skus'] = self.skus(response)
        return garment

    def image_urls(self, response):
        image_urls = []
        images_css = '.imageThumb img::attr(src)'
        for image_url in clean(response.css(images_css)):
            image_url = image_url.replace('resizeandpad:200:300', '')
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
        common_sku = self.product_pricing_common(response)

        css = '.details-description p::text'
        soup = clean(response.css(css)) + self.raw_description(response)
        colour = self.detect_colour(soupify(soup))
        if colour:
            common_sku['colour'] = colour

        for size_sel in response.css('.s-size a'):
            sku = common_sku.copy()

            size = clean(size_sel.css('::text'))[0]
            sku['size'] = self.one_size if size == 'One' else size

            if size_sel.css('.notavailable'):
                sku['out_of_stock'] = True

            sku_id = f"{colour}_{sku['size']}" if colour else sku['size']
            skus[sku_id] = sku

        return skus


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
