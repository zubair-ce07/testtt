from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    allowed_domains = ["rakuten.co.jp"]
    start_urls = ["https://www.rakuten.co.jp"]

    lang = "ja"
    market = "JP"
    retailer = "rakuten-jp"

    MERCH_MAP = [
        ("期間限定", "Limited Time"),
        ("送料無料", "Free Shipping")]

    COLOUR_KEYS = ["色", "カラー", "色彩", "顔色", "ストリーマ", "ストリーマー", "呈色", "色のついた"]

    one_colour = ["ワンカラー"]


class RakutenParser(Mixin, BaseParseSpider):
    name = Mixin.retailer + "-parser"

    description_css = "meta[name='description']::attr(content), .item_desc::text"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["url"] = response.url
        garment["image_urls"] = self.image_urls(response)
        garment["merch_info"] = self.merch_info(garment)
        garment["gender"] = self.product_gender(garment)
        garment["category"] = self.product_category(response)
        garment["skus"] = self.skus(response)

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = "meta[property='apprakuten:item_id']::attr(content)"
        return response.css(css).extract_first()

    def product_name(self, response):
        css = "meta[property='og:title']::attr(content)"
        return response.css(css).extract_first()

    def product_category(self, response):
        css = "meta[property='apprakuten:shop_code']::attr(content)"
        return response.css(css).extract()

    def product_gender(self, garment):
        soup = " ".join(garment["description"] + [garment["name"]] + garment["merch_info"])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def merch_info(self, garment):
        soup = " ".join([desc.lower() for desc in garment["description"]])
        return [merch for key, merch in self.MERCH_MAP if key.lower() in soup]

    def image_urls(self, response):
        css = ".rakutenLimitedId_ImageMain1-3::attr(href)"
        return response.css(css).extract()

    def product_price(self, response):
        css = "meta[property='apprakuten:price']::attr(content)"
        return response.css(css).extract_first()

    def currency_type(self, response):
        css = "meta[property='apprakuten:currency']::attr(content)"
        return response.css(css).extract_first()

    def sku_dimensions(self, response):
        css = "td[valign='bottom'] .inventory_title::text"
        return clean(response.css(css).extract())

    def skus(self, response):
        skus = {}
        row_attr, col_attr = [], []
        money_str = [self.product_price(response), self.currency_type(response)]

        css_row = ".skuDisplayTable table tr:nth-child(1) ::text"
        css_col = ".skuDisplayTable table tr td:nth-child(1) ::text"

        skus_dimension = self.sku_dimensions(response)
        if not skus_dimension:
            sku = self.product_pricing_common(None, money_strs=money_str)
            skus[self.product_id(response)] = sku
            return skus

        row_soup = skus_dimension[0].split()
        row_check = [key for key in self.COLOUR_KEYS if key in row_soup]

        colours = clean(response.css(css_row).extract()) if row_check else row_attr.extend(
            clean(response.css(css_row).extract()))

        col_soup = skus_dimension[-1].split()
        col_check = [key for key in self.COLOUR_KEYS if key in col_soup]

        colours = clean(response.css(css_col).extract()) if col_check else col_attr.extend(
            clean(response.css(css_col).extract()))

        if not colours:
            colours = self.one_colour
            sizes = [f"{row}/{col}" for row in row_attr for col in col_attr]
        else:
            sizes = row_attr if row_attr else col_attr

        for colour in colours:
            for size in sizes:
                sku = self.product_pricing_common(None, money_strs=money_str)
                sku["colour"] = colour
                sku["size"] = size
                skus[f"{colour}_{size}"] = sku

        return skus


class RakutenCrawler(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + "-crawler"
    parse_spider = RakutenParser()

    listings_css = [".categoryMenu__l1Container", ".dui-pagination"]
    product_css = [".aditem"]

    deny_re = ["review"]

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css, deny=deny_re), callback="parse_item")]
