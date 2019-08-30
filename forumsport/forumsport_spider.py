import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule
from w3lib.url import add_or_replace_parameters

from .base import BaseCrawlSpider, BaseParseSpider, clean, extract_text,\
    Gender, soupify


class Mixin:
    retailer = 'forumsport'
    market = 'ES'


class MixinES(Mixin):
    retailer = Mixin.retailer + '-es'
    lang = 'es'
    allowed_domains = ['forumsport.com']
    start_urls = ['https://www.forumsport.com/ropa-calzado/']


class MixinIT(Mixin):
    retailer = Mixin.retailer + '-it'
    lang = 'it'
    allowed_domains = ['eu.forumsport.com/it-it/']
    start_urls = ['https://eu.forumsport.com/it-it/']


class MixinFR(Mixin):
    retailer = Mixin.retailer + '-fr'
    lang = 'fr'
    allowed_domains = ['eu.forumsport.com/fr-fr/']
    start_urls = ['https://eu.forumsport.com/fr-fr/']


class MixinDE(Mixin):
    retailer = Mixin.retailer + '-de'
    lang = 'de'
    allowed_domains = ['eu.forumsport.com/de-de/']
    start_urls = ['https://eu.forumsport.com/de-de/']


class MixinPT(Mixin):
    retailer = Mixin.retailer + '-pt'
    lang = 'pt'
    allowed_domains = ['eu.forumsport.com/pt-pt/']
    start_urls = ['https://eu.forumsport.com/pt-pt/']


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    lang = 'en'
    allowed_domains = ['eu.forumsport.com']
    start_urls = ['https://eu.forumsport.com/en-uk/menu']


class ParseSpider(BaseParseSpider):
    care_css = '.adv-feature-list h4::text, #description .features li::text'
    description_css = '.short-description-container p::text'
    brand_css = '.model-features-card::attr(data-brand)'
    price_css = '.previous-price, .usizy-external::attr(data-price)'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {
            'requests_queue': self.colour_requests(response)
        }

        return self.next_request_or_garment(garment)

    def parse_colour_requests(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

    def product_id(self, response):
        return clean(response.css('.ref span::text'))[0]

    def product_name(self, response):
        raw_product_name = clean(response.css('.model::text'))[0]
        return self.remove_brand_from_text(self.product_brand(response), raw_product_name)

    def product_category(self, response):
        raw_categories = clean(response.css('script:contains("BreadcrumbList")::text'))

        if not raw_categories:
            return []

        raw_categories = json.loads(raw_categories[0])['itemListElement']
        return clean([c['item']['name'] for c in raw_categories[1:-1]])

    def product_gender(self, response):
        css = '.review.show-for-large-up::text, .product-name .description::text'
        return self.gender_lookup(soupify(clean(response.css(css)))) or Gender.ADULTS.value

    def colour_requests(self, response):
        css = '.color-section a::attr(href)'
        urls = extract_text(response.css(css), post_process=response.urljoin)

        # TODO: Extract images
        return [Request(url=url, callback=self.parse_colour_requests) for url in urls]

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = clean(response.css('.color-section .active'))[0]


class CrawlSpider(BaseCrawlSpider):
    listings_css = ['.no-children']
    products_css = ['.product-preview']

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        css_t = '.product-search-page::attr({})'
        url = response.urljoin(clean(response.css(css_t.format('data-scrolling-url')))[0])
        total_pages = int(clean(response.css(css_t.format('data-total-pages')))[0])

        for page_num in range(1, total_pages):
            new_url = f'{url}/{page_num}-{page_num}'
            new_url = add_or_replace_parameters(new_url, {'page': page_num})
            yield Request(url=new_url, meta=meta)


class ForumSportESParseSpider(MixinES, ParseSpider):
    name = MixinES.retailer + '-parse'
    description_css = '[itemprop="disambiguatingDescription"]::text'
    care_css = '.adv-feature-list strong::text'
    brand_css = '.model-brand-card meta[itemprop="brand"]::attr(content)'
    price_css = '.previous-price, .price::attr(content)'

    def skus(self, response):
        common_sku = self.product_pricing_common(response)
        common_sku['colour'] = clean(response.css('.color-section .active'))[0]
        skus = {}


class ForumSportUKParseSpider(MixinUK, ParseSpider):
    name = MixinUK.retailer + '-parse'


class ForumSportFRParseSpider(MixinFR, ParseSpider):
    name = MixinFR.retailer + '-parse'
    listing_css = ['.rowmenu li.sub-title~li']


class ForumSportESCrawlSpider(MixinES, CrawlSpider):
    name = MixinES.retailer + '-crawl'
    parse_spider = ForumSportESParseSpider()


class ForumSportUKCrawlSpider(MixinUK, CrawlSpider):
    name = MixinUK.retailer + '-crawl'
    parse_spider = ForumSportUKParseSpider()


class ForumSportFRCrawlSpider(MixinFR, CrawlSpider):
    name = MixinFR.retailer + '-crawl'
    parse_spider = ForumSportUKParseSpider()
