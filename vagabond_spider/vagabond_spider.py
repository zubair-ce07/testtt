from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, LinkExtractor, clean, soupify, Gender


class Mixin:
    retailer = 'vagabond'
    default_brand = 'Vagabond'
    allowed_domains = ['vagabond.com']


class MixinUK(Mixin):
    market = 'UK'
    retailer = Mixin.retailer + '-uk'
    start_urls = ['https://www.vagabond.com/']
    image_url_t = 'https://www.vagabond.com{}'


class VagabondParseSpider(BaseParseSpider):
    price_css = '.productPrice .price ::text'
    raw_description_css = '#productInformationArea .tab-content ::text'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["gender"] = self.product_gender(response)
        garment['image_urls'] = self.product_image_urls(response)
        garment['skus'] = self.skus(response)

        return garment

    def product_category(self, response):
        return [i[0] for i in response.meta['trail']]

    def product_name(self, response):
        return soupify(clean(response.css('.product_name ::text')))

    def product_id(self, response):
        return clean(response.css('#ProductCode ::attr(value)'))[0]

    def product_gender(self, response):
        soup = soupify([response.url] + self.product_category(response))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def product_image_urls(self, response):
        css = '.product-image-navigation.thumbs img ::attr(data-src)'
        return [self.image_url_t.format(rel_url) for rel_url in clean(response.css(css))]

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        sizes_s = response.css('#productInformationArea .sel__box__options ')
        colour = self.detect_colour(soupify(clean(response.css('#tab2 ::text'))))

        if colour:
            common_sku['colour'] = colour

        if sizes_s:

            for size_s in sizes_s:
                sku = common_sku.copy()
                sku['size'] = clean(size_s.css('::text')[0])

                if size_s.css('.disabled'):
                    sku['out_of_stock'] = True

                skus[f'{colour}_{sku["size"]}' if colour else sku["size"]] = sku

        else:
            common_sku['size'] = self.one_size
            skus[f'{colour}_{self.one_size}' if colour else self.one_size] = common_sku

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
