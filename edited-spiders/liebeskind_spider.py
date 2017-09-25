import json

from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst
from w3lib.url import add_or_replace_parameter, url_query_cleaner

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
        garment['meta'] = {'requests_queue': self.color_requests(response)}

        return self.next_request_or_garment(garment)

    def parse_colors(self, response):
        garment = response.meta['garment']

        garment['image_urls'] += self.image_urls(response)
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def color_requests(self, response):
        requests = []
        xpath = "//li[contains(@class,'ta_color jsColorVariant') and @data-loaded='false']//@data-product"
        color_ids = clean(response.xpath(xpath))

        for color_id in color_ids:
            url = add_or_replace_parameter(response.url, 'sku', color_id)
            # These urls are available on listings pages as well so use dont_filter
            requests += [Request(url, dont_filter=True, callback=self.parse_colors)]

        return requests

    def skus(self, response):
        skus = {}
        skus_json = self.skus_json(response)

        if skus_json:
            sizes = clean(response.xpath("//li[contains(@class,'size jsSizeVariant')]//text()")) or [self.one_size]
            previous_price, price, currency = self.product_pricing(response)

            for color in skus_json.keys():
                for size in sizes:
                    size_key = "1" if size == self.one_size else size

                    sku = {
                        'price': price,
                        'currency': currency,
                        'size': size,
                        'colour': color,
                    }

                    # Watches do not have valid data in sku json so we dont know their oos status
                    if size_key not in list(skus_json[color].keys()):
                        sku['out_of_stock'] = True

                    if previous_price:
                        sku['previous_prices'] = [previous_price]

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
        xpath_color = "//div[@class='select']//select[@class='jsColorInputSelect']//option"
        sku_colors = []
        for color in response.xpath(xpath_color):
            color_id = clean(color.xpath('@value'))
            if color_id:
                sku_colors.append((clean(color.xpath('text()'))[0], color_id[0]))
        return sku_colors


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
