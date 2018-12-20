from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, Gender, clean


class Mixin:
    allowed_domains = ["rakuten.co.jp"]
    start_urls = ["https://www.rakuten.co.jp"]

    market = "JP"
    retailer = "rakuten-jp"
    default_brand = "rakuten"

    merch_map = [
        ("期間限定", "Limited Time"),
        ("送料無料", "Free Shipping")]

    colour_keys = [
        "COLOR", "色", "カラー", "色彩", "顔色", "ストリーマ",
        "ストリーマー", "呈色", "色のついた"]

    size_keys = [
        "SIZE", "サイズ", "寸法", "大小", "大小", "判",
        "値", "大きさ"]


class RakutenParser(Mixin, BaseParseSpider):
    name = Mixin.retailer + "-parse"

    description_css = "meta[name='description']::attr(content), .item_desc::text"
    price_css = ".price2::text"
    availability_css = ".inventory[rownum='{0}'][colnum='{1}'] .sku_cross"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["image_urls"] = self.image_urls(response)
        garment["merch_info"] = self.merch_info(garment)
        garment["gender"] = self.product_gender(garment)
        garment["category"] = self.product_category(response)
        garment["skus"] = self.skus(response)

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = "meta[property='apprakuten:item_id']::attr(content)"
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = "meta[property='og:title']::attr(content)"
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = "meta[property='apprakuten:shop_code']::attr(content)"
        return clean(response.css(css))

    def product_gender(self, garment):
        soup = " ".join(garment["description"] + [garment["name"]] + garment["merch_info"])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def merch_info(self, garment):
        soup = " ".join([desc for desc in garment["description"]]).lower()
        return [merch for key, merch in self.merch_map if key.lower() in soup]

    def image_urls(self, response):
        css = ".rakutenLimitedId_ImageMain1-3::attr(href)"
        return clean(response.css(css))

    def sku_dimensions(self, response):
        css = "td[valign='bottom'] .inventory_title::text"
        return clean(response.css(css))

    def get_attributes(self, response):
        colour_index, size_index = -1, -1

        for index, attr in enumerate(self.sku_dimensions(response)):
            if any([key for key in self.colour_keys if key.lower() in attr]):
                colour_index = index
            if any([key for key in self.size_keys if key.lower() in attr]):
                size_index = index

        return colour_index, size_index

    def table_skus_content(self, response):
        css_col = ".skuDisplayTable table tr td:nth-child(1) ::text"
        css_row = ".skuDisplayTable table tr:nth-child(1) ::text"
        colours = clean(response.css(css_row))
        sizes = clean(response.css(css_col))

        colour_index, size_index = self.get_attributes(response)

        if colour_index > size_index and colour_index is not -1:
            colours, sizes = sizes, colours
        if colour_index == -1:
            colours.clear() or colours.append(self.detect_colour_from_name(response))
        if size_index == -1:
            sizes.clear() or sizes.append(self.one_size)

        return colours, sizes

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)

        colours, sizes = self.table_skus_content(response)

        for row, colour in enumerate(colours):
            for col, size in enumerate(sizes):
                sku = common_sku.copy()
                sku["size"] = size

                if colour:
                    sku["colour"] = colour

                css = self.availability_css.format(row, col)
                if clean(response.css(css)) and colour:
                    sku["out_of_stock"] = True

                skus[f"{colour}_{size}"] = sku

        return skus


class RakutenCrawler(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + "-crawl"
    parse_spider = RakutenParser()

    listings_css = [".categoryMenu__l3Link", ".nextPage"]
    product_css = [".searchresultitems .dui-card"]

    deny_re = ["review", "/gold/"]

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css, deny=deny_re), callback="parse_item")]
