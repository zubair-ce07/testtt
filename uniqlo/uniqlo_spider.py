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


class ParseSpider(BaseParseSpider):
    description_css = 'meta[property="og:description"]::attr(content), p.about::text'
    care_css_t = '.spec dt:contains("{}")+dd::text'
    care_css = f'{care_css_t.format("素材")},{care_css_t.format("取扱い")}'
    one_size = 'one size'

    def parse(self, response):
        raw_product = self.raw_product(response)
        garment = self.new_unique_garment(self.product_id(raw_product))

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(raw_product)
        merch_info = self.merch_info(raw_product)

        if merch_info:
            garment['merch_info'] = self.merch_info(raw_product)

        return garment

    def raw_product(self, response):
        css = 'script:contains("JSON_DATA")'
        return json.loads(response.css(css).re_first(r'=(.*?);<'))["GoodsInfo"]["goods"]

    def product_id(self, raw_product):
        return clean(raw_product['l1GoodsCd'])

    def product_name(self, response):
        return clean(response.css('#goodsNmArea::text'))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumbs a::text'))[:-1]

    def product_gender(self, response):
        return soupify(self.product_category(response)) or Gender.ADULTS.value

    def merch_info(self, raw_product):
        for raw_sku in raw_product['l2GoodsList'].values():
            if int(raw_sku['L2GoodsInfo']['termLimitSalesFlg']):
                return [raw_sku['L2GoodsInfo']['termLimitSalesEndMsg']]

    def image_urls(self, raw_product):
        product_id = self.product_id(raw_product)
        image_urls = []

        for raw_image in raw_product['goodsSubImageList'].split(';'):
            image_urls.append(f'{raw_product["httpsImgDomain"]}/goods/'
                              f'{product_id}/sub/{raw_image}.jpg')

        for colour in raw_product['colorInfoList']:
            image_urls.append(f'{raw_product["httpsImgDomain"]}/goods/'
                              f'{product_id}/item/{colour}_{product_id}.jpg')

        return image_urls

    def skus(self, raw_product):
        skus = {}

        colours_map = raw_product['colorInfoList']
        sizes_map = raw_product['sizeInfoList']
        lengths_map = raw_product['lengthInfoList']

        for sku_id, raw_sku in raw_product['l2GoodsList'].items():
            raw_sku = raw_sku['L2GoodsInfo']
            sku = self.product_pricing_common(None, money_strs=[raw_sku['salesPrice']])
            sku['colour'] = self.detect_colour(colours_map[raw_sku['colorCd']])
            sku['size'] = sizes_map[raw_sku['sizeCd']] or self.one_size
            sku['out_of_stock'] = not bool(int(raw_sku['sumStockCnt']))
            length = lengths_map[raw_sku['lengthCd']]

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


class UniqloJPCrawlSpider(MixinJP, CrawlSpider):
    name = MixinJP.retailer + '-crawl'
    parse_spider = UniqloJPParseSpider()
