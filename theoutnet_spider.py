import re
import json

from w3lib.url import add_or_replace_parameter

from .base import BaseParseSpider, BaseCrawlSpider, clean
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.http import Request


class Mixin:
    retailer = 'theoutnet'
    gender = 'women'
    outlet = True
    lang = 'en'

    allowed_domains = ['www.theoutnet.com', 'cache.theoutnet.com']

    start_url_t = 'https://www.theoutnet.com/{}/Shop/{}'

    cats = ['Just-In', 'Clothing', 'Bags', 'Shoes', 'Accessories']


def make_start_urls(region):
    return [
        [Mixin.start_url_t.format(region, cat), {'category': [cat]}] for cat in Mixin.cats
    ]


class MixinUK(Mixin):
    retailer = Mixin.retailer + '-uk'
    market = 'UK'
    start_urls_with_meta = make_start_urls('en-uk')


class MixinRU(Mixin):
    retailer = Mixin.retailer + '-ru'
    market = 'RU'
    start_urls_with_meta = make_start_urls('en-ru')


class MixinAU(Mixin):
    retailer = Mixin.retailer + '-au'
    market = 'AU'
    start_urls_with_meta = make_start_urls('en-au')


class MixinCN(Mixin):
    retailer = Mixin.retailer + '-cn'
    market = 'CN'
    allowed_domains = ['store.theoutnet.cn', 'cache.theoutnet.com']
    start_urls_with_meta = make_start_urls('en-cn')


class MixinEU(Mixin):
    retailer = Mixin.retailer + '-eu'
    market = 'EU'
    start_urls_with_meta = make_start_urls('en-de')


class MixinHK(Mixin):
    retailer = Mixin.retailer + '-hk'
    market = 'HK'
    start_urls_with_meta = make_start_urls('en-hk')


class MixinJP(Mixin):
    retailer = Mixin.retailer + '-jp'
    market = 'JP'
    lang = 'ja'
    start_urls_with_meta = make_start_urls('ja-jp')
    sentence_delimiter = '/'


class MixinAE(Mixin):
    retailer = Mixin.retailer + '-ae'
    market = 'AE'
    start_urls_with_meta = make_start_urls('en-ae')


class MixinUS(Mixin):
    retailer = Mixin.retailer + '-us'
    market = 'US'
    start_urls_with_meta = make_start_urls('en-us')


class TheOutnetParseSpider(BaseParseSpider):
    price_css = 'div.price .price ::text'
    raw_description_css = '.item-info .selected ul ::text,.compositionInfo .text ::text'

    image_urls_re = re.compile('_(.*?)_')

    def parse(self, response):
        garment_id = self.product_id(response)
        garment = self.new_unique_garment(garment_id)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['brand'] = self.product_brand(response)
        garment['name'] = self.product_name(response)
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)
        garment['merch_info'] = self.merch_info(response)
        garment['skus'] = self.skus(response)
        garment['image_urls'] = self.image_urls(response)

        if response.css('.item-content__soldout-label'):
            garment['out_of_stock'] = True

        garment['meta'] = {'requests_queue': self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta.get('garment')
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return response.css('script:contains("yTos.navigation")').re_first('"RootPartNumber":"(\d+)"')

    def product_name(self, response):
        return clean(response.css('.item-content__model-name ::text'))[0]

    def product_brand(self, response):
        return clean(response.css('.item-content__title a ::text'))[0]

    def product_colour(self, response):
        colour = clean(response.css('.colors > p::text'))[0]
        return colour.split(':')[-1].strip()

    def image_urls(self, response):
        css = '.slider--with-thumbs-nav img::attr(src)'
        return [self.image_urls_re.sub('_14_', i) for i in clean(response.css(css))]

    def colour_requests(self, response):
        requests = []

        for url in clean(response.css('.colorInfo a::attr(href)')):
            requests += [Request(url, dont_filter=True, callback=self.parse_colour)]

        return requests

    def merch_info(self, response):
        soup = clean(response.css('.item-content__badge ::text'))
        if not soup:
            return []
        if 'exclusive' in soup[0].lower() or 'extra' in soup[0].lower():
            return soup
        return []

    def sku_merch_info(self, raw_sku):
        merch = []

        if raw_sku['IsPreorderForSelectedColor']:
            merch.append('Pre Order')

        if raw_sku['IsLimitedForSelectedColor']:
            merch.append('Limited Availability')

        if raw_sku['IsLastAvailableForSelectedColor']:
            merch.append('Last Available')

        return merch

    def raw_skus(self, response):
        raw_skus = []

        for raw_sku_s in response.css('.HTMLListSizeSelector li'):
            raw_skus += [json.loads(clean(raw_sku_s.css('::attr(data-ytos-size-model)'))[0])]

        return raw_skus

    def skus(self, response):
        skus = {}
        common = self.product_pricing_common(response)
        color = clean(response.css('.selectedColorInfo::text'))[0]
        sku_id_t = '{}_{}'

        for raw_sku_data in self.raw_skus(response):
            sku = common.copy()

            sku['colour'] = color
            sku['size'] = self.one_size if '--' in raw_sku_data['Label'] else raw_sku_data['Label']

            if raw_sku_data['IsSoldoutForSelectedColor']:
                sku['out_of_stock'] = True

            sku_merch_info = self.sku_merch_info(raw_sku_data)
            if sku_merch_info:
                sku['merch_info'] = sku_merch_info

            skus[sku_id_t.format(color, sku['size'])] = sku

        return skus


class TheOutnetCrawlSpider(BaseCrawlSpider):
    pagination_css = '.nextPage'
    products_css = '.itemLink'

    rules = (Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),)

    total_pages_re = re.compile('totalPages":"(\d*?)"')

    def parse_start_url(self, response):
        xpath = '//script[contains(.,"totalPages")]'
        total_pages = response.xpath(xpath).re_first(self.total_pages_re)

        for page in range(1, int(total_pages) + 1):
            yield Request(url=add_or_replace_parameter(response.url, 'page', str(page)), callback=self.parse)


class TheOutnetUKParseSpider(TheOutnetParseSpider, MixinUK):
    name = MixinUK.retailer + '-parse'


class TheOutnetUKCrawlSpider(TheOutnetCrawlSpider, MixinUK):
    name = MixinUK.retailer + '-crawl'
    parse_spider = TheOutnetUKParseSpider()


class TheOutnetRUParseSpider(TheOutnetParseSpider, MixinRU):
    name = MixinRU.retailer + '-parse'


class TheOutnetRUCrawlSpider(TheOutnetCrawlSpider, MixinRU):
    name = MixinRU.retailer + '-crawl'
    parse_spider = TheOutnetRUParseSpider()


class TheOutnetAUParseSpider(TheOutnetParseSpider, MixinAU):
    name = MixinAU.retailer + '-parse'


class TheOutnetAUCrawlSpider(TheOutnetCrawlSpider, MixinAU):
    name = MixinAU.retailer + '-crawl'
    parse_spider = TheOutnetAUParseSpider()


class TheOutnetCNParseSpider(TheOutnetParseSpider, MixinCN):
    name = MixinCN.retailer + '-parse'


class TheOutnetCNCrawlSpider(TheOutnetCrawlSpider, MixinCN):
    name = MixinCN.retailer + '-crawl'
    parse_spider = TheOutnetCNParseSpider()


class TheOutnetEUParseSpider(TheOutnetParseSpider, MixinEU):
    name = MixinEU.retailer + '-parse'


class TheOutnetEUCrawlSpider(TheOutnetCrawlSpider, MixinEU):
    name = MixinEU.retailer + '-crawl'
    parse_spider = TheOutnetEUParseSpider()


class TheOutnetHKParseSpider(TheOutnetParseSpider, MixinHK):
    name = MixinHK.retailer + '-parse'


class TheOutnetHKCrawlSpider(TheOutnetCrawlSpider, MixinHK):
    name = MixinHK.retailer + '-crawl'
    parse_spider = TheOutnetHKParseSpider()


class TheOutnetJPParseSpider(TheOutnetParseSpider, MixinJP):
    name = MixinJP.retailer + '-parse'


class TheOutnetJPCrawlSpider(TheOutnetCrawlSpider, MixinJP):
    name = MixinJP.retailer + '-crawl'
    parse_spider = TheOutnetJPParseSpider()


class TheOutnetAEParseSpider(TheOutnetParseSpider, MixinAE):
    name = MixinAE.retailer + '-parse'


class TheOutnetAECrawlSpider(TheOutnetCrawlSpider, MixinAE):
    name = MixinAE.retailer + '-crawl'
    parse_spider = TheOutnetAEParseSpider()


class TheOutnetUSParseSpider(TheOutnetParseSpider, MixinUS):
    name = MixinUS.retailer + '-parse'


class TheOutnetUSCrawlSpider(TheOutnetCrawlSpider, MixinUS):
    name = MixinUS.retailer + '-crawl'
    parse_spider = TheOutnetUSParseSpider()

