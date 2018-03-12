import json

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'colcci-br'
    market = 'BR'
    allowed_domains = ['colcci.com.br']
    start_urls_with_meta = [
        ('https://www.colcci.com.br/fitness/', {'gender': 'women'}),
        ('https://www.colcci.com.br/feminino-novo/', {'gender': 'women'}),
        ('https://www.colcci.com.br/acessorios/', {'gender': 'women'}),
        ('https://www.colcci.com.br/masculino-novo/', {'gender': 'men'}),
        ('https://www.colcci.com.br/fitnesssale/', {'gender': 'men'}),
    ]


class ParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)
        return garment

    def product_id(self, response):
        css = '[name="add_to_cart"]::attr(value)'
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = "h1[itemprop='name']::text"
        return clean(response.css(css))[0]

    def product_brand(self, response):
        return 'Colcci'

    def product_category(self, response):
        css = "#breadcrumb a::text"
        return clean(response.css(css))[1:]

    def product_description(self, response):
        return []

    def product_care(self, response):
        return clean(response.css('#whatItIs ::text'))

    def raw_skus(self, response):
        css = 'script:contains("LS.variants")::text'
        raw_js = response.css(css).re('variants\s*=\s*(\[.*]);')
        return json.loads(raw_js[0])

    def skus(self, response):
        skus = {}
        raw_skus = self.raw_skus(response)
        for raw_sku in raw_skus:
            money_strs = [raw_sku.get('price_short'), raw_sku.get('compare_at_price_short')]
            sku = self.product_pricing_common_new(None, money_strs=money_strs)

            sku['colour'] = raw_sku['option0']
            size = raw_sku['option1']
            sku['size'] = self.one_size if size == 'U' else size

            if not raw_sku['available']:
                sku['out_of_stock'] = True
            skus[raw_sku['id']] = sku
        return skus

    def image_urls(self, response):
        css1 = ".jTscrollerContainer a::attr(href)"
        css2 = ".imagecolContent a::attr(href)"
        return response.css(css1).extract() or response.css(css2).extract()


def clean_url(url):
    return url.replace('http://', 'https://')


class CrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = ParseSpider()

    pagination_css = [
        ".pagination"
    ]

    products_css = ".product-table"

    rules = (
        Rule(LinkExtractor(restrict_css=pagination_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css, process_value=clean_url), callback='parse_item'),
    )
