import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule
from w3lib.url import add_or_replace_parameters

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender, soupify


class Mixin:
    retailer = 'uniqlo'
    default_brand = 'ユニクロ'
    allowed_domains = ['uniqlo.com']


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    start_urls = ['https://www.uniqlo.com/jp/']

    lang = 'ja'
    listing_url = 'https://www.uniqlo.com/jp/store/feature/uq/alias/v2/ajaxAliasItem.jsp'
    product_url = 'https://www.uniqlo.com/jp/spa-proxy/catalog/product/details'


class ParseSpider(BaseParseSpider):
    description_css = 'meta[property="og:description"]::attr(content), p.about::text'
    care_css_t = '.spec dt:contains("{}")+dd::text'
    care_css = f'{care_css_t.format("素材")},{care_css_t.format("取扱い")}'

    def parse(self, response):
        garment = self.new_unique_garment(self.product_id(response))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['meta'] = {
            'requests_queue': self.product_request(response)
        }

        return self.next_request_or_garment(garment)

    def parse_product(self, response):
        garment = response.meta['garment']
        raw_product = self.raw_product(response)
        merch_info = self.merch_info(raw_product)

        if merch_info:
            garment['merch_info'] = merch_info

        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(raw_product)

        return self.next_request_or_garment(garment)

    def product_request(self, response):
        params = {'products': self.product_id(response)}
        return [
            Request(url=add_or_replace_parameters(self.product_url, params),
                    callback=self.parse_product)
        ]

    def product_id(self, response):
        css = 'script:contains("mpn")::text'
        return json.loads(response.css(css).re_first(r"{.*}"))['mpn']

    def product_name(self, response):
        return clean(response.css('#goodsNmArea::text'))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumbs a::text'))[:-1]

    def product_gender(self, response):
        soup = soupify(self.product_category(response))
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def raw_product(self, response):
        return json.loads(response.text)['products'][0]

    def merch_info(self, raw_product):
        return [raw_product['termsLimitMsg']] if raw_product['termsLimitFlag'] else None

    def image_urls(self, raw_product):
        image_urls = [ri['zoom']['path'] for ri in raw_product['alternateImages']]
        return image_urls + [ri['zoom']['path'] for _, ri in raw_product['images'].items()]

    def skus(self, raw_product):
        skus = {}
        colours_map = raw_product.get('colorsList')
        sizes_map = raw_product.get('sizesList')

        for sku_id, raw_sku in raw_product['skus'].items():
            money_strs = [  
                raw_product['basePrice'], raw_sku['salesPrice'],
            ]
            sku = self.product_pricing_common(None, money_strs=money_strs)
            sku['colour'] = self.detect_colour(colours_map.get('raw_sku["color"]', {}).get('name'))
            sku['size'] = sizes_map[raw_sku['size']]['name']
            sku['out_of_stock'] = not bool(int(raw_sku['sumStockCount']))

            if raw_product.get('allLengthsList'):
                length = raw_product['allLengthsList'][raw_sku['length']]['name']
                if length:
                    sku['length'] = length

            skus[sku_id] = sku

        return skus


class CrawlSpider(BaseCrawlSpider):
    product_css = ['.name']
    listing_css = ['.gnav_category_wrapper a']

    rules = (
        Rule(link_extractor=LinkExtractor(restrict_css=product_css), callback='parse_item'),
        Rule(link_extractor=LinkExtractor(restrict_css=listing_css), callback='parse_listing'),
    )

    def parse_listing(self, response):
        base_url = response.css('script:contains("base:")').re_first(r"'(.*?)'")
        page_codes = clean(response.css('.set-alias::attr(data-layer)'))
        params = {
            'dispLayerInfoFull': soupify([f'{base_url}{pc}' for pc in page_codes], delimiter=',')
        }

        return Request(url=add_or_replace_parameters(self.listing_url, params))


class UniqloJPParseSpider(MixinJP, ParseSpider):
    name = MixinJP.retailer + '-parse'
    start_urls = ['https://www.uniqlo.com/jp/store/goods/418414-32']


class UniqloJPCrawlSpider(MixinJP, CrawlSpider):
    name = MixinJP.retailer + '-crawl'
    parse_spider = UniqloJPParseSpider()
