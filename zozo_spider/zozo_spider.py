from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from .base import BaseCrawlSpider, BaseParseSpider, clean


class MixinJP:
    retailer = "zozotown-jp"
    start_urls = ["http://zozo.jp/"]
    allowed_domains = ["zozo.jp"]
    market = "JP"
    one_sizes = ["FREE ", "ONE SIZE ", 'ﾌﾘｰ ']
    MERCH_INFO = ["この商品は予約商品です"]


class ZozotownParseSpider(BaseParseSpider):
    price_css = '.priceWrapper p ::text'

    def parse(self, response):
        pid = self.product_id(response)
        if not pid:
            return

        garment = self.new_unique_garment(pid)
        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["gender"] = self.product_gender(response)
        garment["skus"] = self.skus(response)

        if not garment["skus"]:
            garment.update(self.product_pricing_common_new(response))
            garment["out_of_stock"] = True
        garment["image_urls"] = self.image_urls(response)
        garment["merch_info"] = self.merch_info(response)

        return garment

    def product_id(self, response):
        css = '//script[contains(text(),"goodsName")]/text()'
        return response.xpath(css).re_first("gdid\s+:.([^']*)'")

    def product_name(self, response):
        return clean(response.css('.infoBlock h1 ::text'))[0]

    def product_brand(self, response):
        return clean(response.css('#nameList a ::text'))[-1]

    def product_gender(self, response):
        soup = clean(response.css('#itemDetailInfo a ::text'))[0]
        gender = self.gender_lookup(soup)

        return gender if gender else "unisex-adults"

    def product_category(self, response):
        return clean(response.css('.lineNavi li a ::text'))

    def raw_description(self, response):
        desc_sel = response.css('#tabItemInfo .innerBox')[0]
        raw_description = clean(desc_sel.css('.contbox ::text'))
        raw_care = clean(response.css('#itemDetailInfo dd ::text'))

        return raw_description+raw_care

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria_simplified(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria_simplified(rd)]

    def image_urls(self, response):
        raw_images = clean(response.css('#photoThimb img ::attr(src)'))
        return [raw_image.replace('35', '500') for raw_image in raw_images]

    def merch_info(self, response):
        merhc_info = clean(response.css('.reserveBox p ::text'))
        return [m for m in self.MERCH_INFO if m in merhc_info]

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common_new(response)
        color_size_sel = response.css('dl[class="clearfix"]')

        for sel in color_size_sel:
            color = clean(sel.css('span[class="txt"] ::text'))[0]
            common_sku["colour"] = color
            sizes = clean(sel.css('.stock span ::text'))
            sku = common_sku.copy()
            for raw_size, stock in zip(sizes[0::2], sizes[1::2]):

                if stock == "在庫なし":
                    sku["out_of_stock"] = True
                    continue

                size = raw_size.split('/')[0]
                my_size = self.one_size if size in self.one_sizes else size
                sku.update({"size": my_size})
                skus[f"{color}/{my_size}"] = sku

        return skus


class ZozotownCrawlSpider(BaseCrawlSpider):

    listing_css = [
        "#categoryList .clearfix",
        ".next"
    ]

    product_css = ".thumb"
    denied_r = ['interior',
                'tableware-kitchenware/',
                'music-books/',
                'category/others/gift-wrap-kit/',
                'category/maternity-baby/baby-car-item/',
                ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=denied_r), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")
    )


class ZozotownParseSpiderJP(MixinJP, ZozotownParseSpider):
    name = MixinJP.retailer + "-parse"


class ZozotownCrawlSpiderJP(MixinJP, ZozotownCrawlSpider):
    name = MixinJP.retailer + "-crawl"
    parse_spider = ZozotownParseSpiderJP()
