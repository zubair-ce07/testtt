import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, Rule
from w3lib.url import add_or_replace_parameters

from .base import BaseCrawlSpider, BaseParseSpider, clean, soupify


class Mixin:
    retailer = 'uniqlo'


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    allowed_domains = ['uniqlo.com']
    start_urls = ['https://www.uniqlo.com/jp/']

    lang = 'ja'
    default_brand = 'ユニクロ'
    listing_url = 'https://www.uniqlo.com/jp/store/feature/uq/alias/v2/ajaxAliasItem.jsp'


class ParseSpider(BaseParseSpider):
    description_css = 'meta[property="og:description"]::attr(content), p.about::text'
    care_css = '.spec dd::text'

    def parse(self, response):
        raw_product = self.raw_product(response)
        garment = self.new_unique_garment(self.product_id(raw_product))

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['image_urls'] = self.image_urls(raw_product)
        garment['skus'] = self.skus(raw_product)

        return garment

    def raw_product(self, response):
        return json.loads(response.css('script:contains("JSON_DATA")').re_first(r'=(.*?);<'))

    def product_id(self, raw_product):
        return clean(raw_product['GoodsInfo']['goods']['l1GoodsCd'])

    def product_name(self, response):
        return clean(response.css('#goodsNmArea::text'))[0]

    def product_category(self, response):
        return clean(response.css('.breadcrumbs a::text'))[:-1]

    def image_urls(self, raw_product):
        product_id = self.product_id(raw_product)
        raw_images = raw_product["GoodsInfo"]["goods"]
        image_urls = []

        for raw_image in raw_images['goodsSubImageList'].split(';'):
            image_urls.append(f'{raw_images["httpsImgDomain"]}/goods/'
                              f'{product_id}/sub/{raw_image}.jpg')

        for colour in raw_images['colorInfoList']:
            image_urls.append(f'{raw_images["httpsImgDomain"]}/goods/'
                              f'{product_id}/item/{colour}_{product_id}.jpg')

        return image_urls

    def skus(self, raw_product):
        skus = {}

        raw_skus = raw_product['GoodsInfo']['goods']
        colours_map = raw_skus['colorInfoList']
        sizes_map = raw_skus['sizeInfoList']
        lengths_map = raw_skus['lengthInfoList']
        raw_skus = raw_skus['l2GoodsList']

        for sku_id, raw_sku in raw_skus.items():
            raw_sku = raw_sku['L2GoodsInfo']
            sku = self.product_pricing_common(None, money_strs=[raw_sku['salesPrice']])
            sku['colour'] = self.detect_colour(colours_map[raw_sku['colorCd']])
            sku['size'] = sizes_map[raw_sku['sizeCd']]
            sku['out_of_stock'] = not bool(int(raw_sku['realStockCnt']))
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

