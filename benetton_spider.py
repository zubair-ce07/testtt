from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst
from scrapy.spiders import Rule
from w3lib.url import add_or_replace_parameter
from w3lib.url import url_query_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'benetton'
    allowed_domains = ['benetton.com']
    start_urls_t = 'http://{pfx}.benetton.com/'


class MixinIT(Mixin):
    retailer = Mixin.retailer + '-it'
    market = 'IT'
    lang = 'it'
    id_re = 'Codice Prodotto: (\w+)'
    color_re = 'Colore: (.*)'
    start_urls = [Mixin.start_urls_t.format(pfx='it')]
    gender_map = [
        ('donna', 'women'),
        ('uomo', 'men'),
        ('bambino', 'boys'),
        ('bambina', 'girls'),
    ]


class MixinES(Mixin):
    retailer = Mixin.retailer + '-es'
    market = 'ES'
    lang = 'es'
    id_re = 'Código producto: (\w+)'
    color_re = 'Color: (.*)'
    start_urls = [Mixin.start_urls_t.format(pfx='es')]
    gender_map = (
        ('nino', 'boys'),
        ('nina', 'girls'),
        ('mujer', 'women'),
        ('hombre', 'men')
    )


class MixinRU(Mixin):
    retailer = Mixin.retailer + '-ru'
    market = 'RU'
    lang = 'ru'
    id_re = 'Product code: (\w+)'
    color_re = 'Цвет: (.*)'
    start_urls = [Mixin.start_urls_t.format(pfx='ru')]
    gender_map = (
        ('ДЛЯ МАЛЬЧИКОВ', 'boys'),
        ('ДЛЯ ДЕВОЧЕК', 'girls'),
        ('ДЛЯ ЖЕНЩИН', 'women'),
        ('ДЛЯ МУЖЧИН', 'men')
    )


class BenettonParseSpider(BaseParseSpider, Mixin):
    take_first = TakeFirst()
    name = Mixin.retailer + '-parse'
    price_x = '//span[@class="price"]/text()'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate(garment, response)

        garment['brand'] = "United Colors of Benetton"
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)
        garment['category'] = self.product_category(response)
        garment['gender'] = self.product_gender(garment)
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)

        garment['meta'] = {'requests_queue': self.colour_requests(response)}
        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        urls = response.css('div.related_colors a::attr(href)').extract()
        return [Request(url, callback=self.parse_colour, dont_filter=True) for url in urls if response.url != url]

    def product_id(self, response):
        return response.css('span.product-sku::text').re(self.id_re)[0]

    def product_name(self, response):
        xpath = '//div[@class="product"]//text()'
        return self.take_first(clean(response.xpath(xpath)))

    def product_description(self, response):
        xpath = '//p[@class="description"]//text() | //span[@class="composition"]//text()'
        return clean(response.xpath(xpath))

    def product_care(self, response):
        return clean(response.xpath('//div[@id="product-care"]//text()'))

    def product_category(self, response):
        return response.css('span[itemprop=title]::text').extract()[1:]

    def image_urls(self, response):
        return response.css('div.slider-item img::attr(data-lazy)').extract()

    def parse_colour(self, response):
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def post_process(self, money_string):
        money_string = [m.replace(' ', '') for m in money_string]
        return money_string

    def product_pricing(self, response):
        return self.extract_prices(response, self.price_x, post_process=self.post_process)

    def skus(self, response):
        skus = {}
        previous_price, price, currency = self.product_pricing(response)
        color = response.css('p.attribute_color::text').re(self.color_re)[0]
        sizes = response.xpath('//div[contains(@class,"simple_swatch")]/span/text()').extract()

        for size in sizes:
            sku = {
                'price': price,
                'currency': currency,
                'size': size,
                'colour': color
            }

            if previous_price:
                sku['previous_prices'] = [previous_price]

            skus[color + '_' + size] = sku

        return skus

    def product_gender(self, garment):
        soup = ' '.join(garment['category']).lower()

        for gender_string, gender in self.gender_map:
            if gender_string.lower() in soup:
                return gender

        return 'unisex-adults'


class BenettonCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = BenettonParseSpider()

    listing_css = 'ul#nav'
    deny_r = [
        'identita'
    ]
    rules = [
        Rule(LinkExtractor(restrict_css=listing_css, deny=deny_r), callback='parse_category')
    ]

    def parse_category(self, response):
        product_urls = response.css('a.abs-link-item::attr(href)').extract()
        for url in product_urls:
            yield Request(url=url, callback=self.parse_spider.parse)

        return self.get_pagination_request(response)

    def get_pagination_request(self, response):
        products_count_sel = response.css('.toolbar script::text')
        if products_count_sel:
            total_products = int(products_count_sel.re('.*totalProducts[=\s]*(\d+)')[0])
            current_products = int(products_count_sel.re('.*currentProducts[=\s]*(\d+)')[0])

            if current_products != total_products:
                next_page_url = self.get_next_page_url(response)
                return Request(url=next_page_url, callback=self.parse_category)

    def get_next_page_url(self, response):
        current_page = int(url_query_parameter(response.url, 'p', '1'))
        return add_or_replace_parameter(response.url, 'p', current_page+1)


class BenettonITParseSpider(BenettonParseSpider, MixinIT):
    name = MixinIT.retailer + '-parse'


class BenettonITCrawlSpider(BenettonCrawlSpider, MixinIT):
    name = MixinIT.retailer + '-crawl'
    parse_spider = BenettonITParseSpider()


class BenettonESParseSpider(BenettonParseSpider, MixinES):
    name = MixinES.retailer + '-parse'


class PepeJeansESCrawlSpider(BenettonCrawlSpider, MixinES):
    name = MixinES.retailer + '-crawl'
    parse_spider = BenettonESParseSpider()


class BenettonRUParseSpider(BenettonParseSpider, MixinRU):
    name = MixinRU.retailer + '-parse'


class BenettonRUCrawlSpider(BenettonCrawlSpider, MixinRU):
    name = MixinRU.retailer + '-crawl'
    parse_spider = BenettonRUParseSpider()
