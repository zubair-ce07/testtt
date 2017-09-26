import json

from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst
from scrapy.spiders import Rule
from w3lib.url import url_query_cleaner

from .base import BaseParseSpider, BaseCrawlSpider
from .base import clean


class Mixin:
    lang = 'de'
    market = 'DE'
    retailer = 'liebeskind-de'
    allowed_domains = ['de.liebeskind-berlin.com']
    start_urls = ['https://de.liebeskind-berlin.com/']


class LiebeskindParseSpider(Mixin, BaseParseSpider):
    take_first = TakeFirst()
    name = Mixin.retailer + '-parse'
    price_x = "//p[contains(@class,'product-price')]//text()"

    def parse(self, response):
        pid = self.product_id(response)
        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = self.skus(response)

        return self.next_request_or_garment(garment)

    def parse_colors(self, response):
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def skus(self, response):
        skus = {}
        skus_json = self.skus_json(response)

        sizes = clean(response.xpath("//li[contains(@class,'size jsSizeVariant')]//text()")) or [self.one_size]
        for color in skus_json:
            for size in sizes:
                size_key = "1" if size == self.one_size else size
                sku = self.product_pricing_common_new(response)
                sku['size'] = size
                sku['colour'] = color

                # Watches do not have valid data in sku json so we dont know their oos status
                if size_key not in skus_json[color]:
                    sku['out_of_stock'] = True
                skus[color + '_' + size] = sku

        return skus

    def product_brand(self, response):
        return 'Liebeskind'

    def image_urls(self, response):
        xpath = "//img[contains(@src,'LBKV2_Zoom')]/@src"
        return clean(response.xpath(xpath))

    def product_gender(self, response):
        if "herren" in ' '.join(self.product_category(response)).lower():
            return 'men'
        return 'women'

    def product_category(self, response):
        xpath = "//span[@data-pagecontextrank='1']/@data-pagecontext"

        cat_data = self.take_first(clean(response.xpath(xpath)))
        cat_data = json.loads(cat_data)

        return cat_data['category']['path'].split('/')

    def raw_description(self, response):
        xpath = "//div[@id='pdp-details-longdesc']//text()"
        return clean(response.xpath(xpath))

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria(rd)]

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria(rd)]

    def product_id(self, response):
        return self.take_first(clean(response.xpath("//a[@class='prodMiniAnchor']/@name")))

    def product_name(self, response):
        return self.take_first(clean(response.xpath("//header[@class='page-head']//text()")))

    def skus_json(self, response):
        raw_sku = {}
        xpath_skus_t = "//a[contains(@class,'jsColorVariant') and @data-colorid='{color_id}']/@data-sizes"

        for color_name, color_id in self.sku_colors(response):
            sku_data = json.loads(
                self.take_first(clean(response.xpath(xpath_skus_t.format(color_id=color_id)))) or '{}')
            raw_sku[color_name] = sku_data
        return raw_sku

    def sku_colors(self, response):
        xpath_color = "//select[contains(@class,'jsColorInputSelect')]//option"
        return [(clean(color.xpath('text()'))[0], clean(color.xpath('@value'))[0])
                for color in response.xpath(xpath_color)]


class LiebeskindCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = LiebeskindParseSpider()

    deny_r = ['_alle', 'lederpflege', 'Magazin']

    listings_x = [
        "//nav[contains(@class,'mainnav')]",
        "//a[contains(@class,'pagination__btn')]",
    ]

    products_x = [
        "//a[contains(@class,'jsProductDetailLink')]",
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_x,
                           deny=deny_r, process_value=lambda url: url_query_cleaner(url, 'isAjax', remove=True)),
             callback='parse'),

        Rule(LinkExtractor(restrict_xpaths=products_x),
             callback='parse_item')
    )
