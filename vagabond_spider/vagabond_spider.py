from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean, Gender


class Mixin:

    retailer = 'vagabond'
    default_brand = 'Vagabond'
    allowed_domains = ['vagabond.com']

    gender = Gender.WOMEN.value


class MixinUK(Mixin):

    market = 'UK'
    retailer = Mixin.retailer + '-uk'
    start_urls = ['https://www.vagabond.com/']


class VagabondParseSpider(BaseParseSpider):

    price_css = '.productPrice .price ::text'
    raw_description_css = '#productInformationArea .tab-content ::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)

        return garment

    def product_id(self, response):
        css = 'script:contains(\'ecommerce\')::text'
        return response.css(css).re_first('\'id\':\s*\'(.*)\',')

    def product_category(self, response):
        return [i[1] for i in response.meta['trail']][-1].split('/')[4:-1]

    def product_name(self, response):
        return clean(' '.join(response.css('.product_name ::text').extract()))

    def image_urls(self, response):
        base_url = 'https://www.vagabond.com{}'
        css = '.product-image-navigation.thumbs img ::attr(data-src)'
        return [base_url.format(rel_url) for rel_url in response.css(css).extract()]

    def skus(self, response):
        skus = {}
        colour_css = '#tab2 > div > span:nth-child(2) ::text'

        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = self.detect_colour(response.css(colour_css).extract_first())

        for size_s in response.css('#productInformationArea .sel__box__options '):
            sku = common_sku.copy()
            sku['size'] = clean(size_s.css('::text').extract_first().split(' ')[0])

            if size_s.css('.disabled'):
                sku['out_of_stock'] = True

            skus[f'{common_sku["colour"]}_{sku["size"]}'] = sku

        else:
            common_sku['size'] = self.one_size
            skus[f'{common_sku["colour"]}_{self.one_size}'] = common_sku

        return skus


class VagabondCrawlSpider(BaseCrawlSpider):

    listings_css = ['.header__main--nav .main li']
    products_css = ['#ProductList a']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), process_request='process_request', callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), process_request='process_request', callback='parse_item'),
    )

    def process_request(self, request):
        request.cookies['country'] = 'en-GB'
        return request


class VagabondUKParseSpider(MixinUK, VagabondParseSpider):
    name = MixinUK.retailer + '-parse'


class VagabondUKCrawlSpider(MixinUK, VagabondCrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = VagabondUKParseSpider()
