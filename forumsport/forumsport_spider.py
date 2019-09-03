from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule
from w3lib.url import add_or_replace_parameters

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender, soupify


class Mixin:
    retailer = 'forumsport'


class MixinES(Mixin):
    retailer = Mixin.retailer + '-es'
    market = 'ES'
    lang = 'es'

    allowed_domains = ['forumsport.com']
    start_urls = ['https://www.forumsport.com/ropa-calzado/']
    one_sizes = ['unica']


class ParseSpider(BaseParseSpider):
    one_size = 'unica'

    description_css = '[itemprop="disambiguatingDescription"]::text'
    care_css = '.adv-feature-list strong::text'
    brand_css = '.model-brand-card meta[itemprop="brand"]::attr(content)'
    price_css = '.price-tag-big .previous-price,.price-tag-big .price::attr(content)'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return [garment] + self.colour_requests(response)

    def product_id(self, response):
        return clean(response.css('.ref span::text'))[0]

    def product_name(self, response):
        raw_product_name = clean(response.css('.model::text'))[0]
        return self.remove_brand_from_text(self.product_brand(response), raw_product_name)

    def product_category(self, response):
        trail = response.meta['trail']
        categories = [t for t, _ in trail] + [clean(response.css('title::text'))[0].split('|')[1]]
        return clean(categories)

    def product_gender(self, response):
        css = '.review.show-for-large-up::text, .product-name .description::text'
        return self.gender_lookup(soupify(clean(response.css(css)))) or Gender.ADULTS.value

    def colour_requests(self, response):
        css = 'a[style="enlaces_hermanos"]::attr(href)'
        return [response.follow(url=url) for url in clean(response.css(css))]

    def image_urls(self, response):
        return clean(response.css('.gallery-image img::attr(src)'))

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)
        raw_colour = clean(response.css('.gallery-image img::attr(title)'))[0]
        colour = self.detect_colour(raw_colour)

        if colour:
            common_sku['colour'] = colour

        oos_css = '.size-selected span:contains("disponible")'
        size_css = '.conver-sizes-items.active .size-item, script:contains("UNICA")'

        for size_s in response.css(size_css):
            sku = common_sku.copy()
            size = size_s.re_first(r'"(.*?)"')

            if size and size.lower() in self.one_sizes:
                sku['size'] = self.one_size
                sku['out_of_stock'] = not bool(response.css(oos_css))
            else:
                sku['size'] = clean(size_s.css('::text'))[0].lower()
                sku['out_of_stock'] = bool(size_s.css('.off'))

            skus[f'{self.product_id(response)}_{sku["size"]}'] = sku

        return skus


class CrawlSpider(BaseCrawlSpider):
    page_size = 24

    listings_css = ['.rowmenu li.sub-title~li']
    products_css = ['.product-preview']
    pagination_url = 'https://www.forumsport.com/listado.php'

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        meta = response.meta.copy()
        meta['trail'] = self.add_trail(response)

        css_t = 'input[name="{}"]::attr(value)'
        total_products = int(clean(response.css(css_t.format('total')))[0])
        params = {
            'seccion': int(clean(response.css(css_t.format('seccion')))[0]),
            'nombre_seccion': clean(response.css(css_t.format('nombre_seccion')))[0]
        }

        for page_num in range(2, total_products // self.page_size + 2):
            params['paginacion[pagina]'] = page_num
            yield Request(url=add_or_replace_parameters(self.pagination_url, params), meta=meta.copy())


class ForumSportESParseSpider(MixinES, ParseSpider):
    name = MixinES.retailer + '-parse'
    

class ForumSportESCrawlSpider(MixinES, CrawlSpider):
    name = MixinES.retailer + '-crawl'
    parse_spider = ForumSportESParseSpider()
