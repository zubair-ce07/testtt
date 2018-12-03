from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.selector import Selector

from .base import BaseParseSpider, BaseCrawlSpider, clean, soupify, Gender


class Mixin:
    retailer = 'philipmorris-uk'
    market = 'UK'
    download_delay = 0.1

    allowed_domains = ['philipmorrisdirect.co.uk']
    start_urls = ['https://www.philipmorrisdirect.co.uk/']


class PhilipMorrisParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    brand_css = '.brand-logo::attr(alt)'
    description_css = '.prodDesc p::text'
    care_css = '.spec li::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        if self.out_of_stock(response):
            return self.out_of_stock_item(response, response, product_id)

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response, garment)
        if self.is_homeware(response, garment):
            garment['industry'] = 'homeware'
        else:
            garment['gender'] = self.product_gender(garment)

        return garment

    def product_id(self, response):
        return clean(response.css('.refs::text'))[0].split(' ')[-1]

    def product_name(self, response):
        return clean(response.css('.detail h1::text'))[0]

    def product_category(self, response):
        return clean(response.css('#breadcrumb a::text'))[1:-1]

    def image_urls(self, response):
        return clean(response.css('#prod-gallery img::attr(src)'))

    def product_gender(self, garment):
        soup = soupify(garment['category'] + garment['description'])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def out_of_stock(self, response):
        return response.css('.delStatTmpUnavail, .unavailableItem')

    def is_homeware(self, response, garment):
        homeware_keys = ['Bathrooms', 'Housewares', 'Tabletop', 'Linen', 'Homewares']
        return any(key in garment['category'] for key in homeware_keys)

    def extract_size(self, size_str, garment):
        size_str = clean(size_str.lower().replace(garment['name'].lower(), ''))
        colour = self.colour_detector.detect_colour(size_str, False)
        size_str = size_str.lower().replace(colour, '')
        if size_str:
            return size_str.strip().replace(' ', '_')

    def skus(self, response, garment):
        skus = {}

        sku_css = '[itemtype="https://schema.org/Product"]'

        for sku in clean(response.css(sku_css)):
            sel = Selector(text=sku)

            money_css = '[itemprop=price]::attr(content), [itemprop=priceCurrency]::attr(content)'
            money_str = clean(sel.css(money_css))
            sku = self.product_pricing_common(response, money_strs=money_str)

            soup = soupify(clean(sel.css('[itemprop=name]::attr(content)')))
            size = self.extract_size(soup, garment)
            sku['size'] = size if size else self.one_size

            colour = self.colour_detector.detect_colour(soup, False)
            if colour:
                sku['colour'] = colour

            sku_id = '_'.join(sc for sc in [sku.get('colour', ''), sku['size']] if sc)
            skus[sku_id] = sku

        return skus


class PhilipMorrisCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = PhilipMorrisParseSpider()

    listings_css = ['.nav', '.deptWrapper']
    products_css = ['.deptProdWrapper']

    deny_re = ['shooting', 'toys', 'hardware']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )
