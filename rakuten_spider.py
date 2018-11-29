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

    one_colour = "One Colour"


class RakutenParser(Mixin, BaseParseSpider):
    name = Mixin.retailer + "-parser"

    description_css = "meta[name='description']::attr(content), .item_desc::text"
    price_css = ".price2::text"
    availability_css = ".inventory[rownum='{0}'][colnum='{1}'] .sku_cross"

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
        css = ".spux-settings-spu::attr(data-item-id)"
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

    def colours_and_sizes(self, response, soup, css, colours=[], sizes=[]):
        check_colour = [key for key in self.colour_keys if key.lower() in soup]
        check_size = [key for key in self.size_keys if key.lower() in soup]

        colours = clean(response.css(css)) if check_colour else colours
        sizes = clean(response.css(css)) if check_size else sizes

        return colours, sizes

    def skus(self, response):
        skus = {}
        common_sku = self.product_pricing_common(response)

        css_row = ".skuDisplayTable table tr td:nth-child(1) ::text"
        css_col = ".skuDisplayTable table tr:nth-child(1) ::text"
        skus_dimension = self.sku_dimensions(response)

        if not skus_dimension:
            sku = common_sku.copy()
            sku["size"] = self.one_size
            skus[self.product_id(response)] = sku
            return skus

        col_soup = skus_dimension[0].lower()
        colours, sizes = self.colours_and_sizes(response, col_soup, css_col)

        if len(skus_dimension) > 1:
            row_soup = skus_dimension[-1].lower()
            colours, sizes = self.colours_and_sizes(response, row_soup, css_row, colours, sizes)

        if not sizes:
            sizes.append(self.one_size)
        if not colours:
            colours.append(self.detect_colour_from_name(response) or self.one_colour)

        for row, colour in enumerate(colours):
            for col, size in enumerate(sizes):
                sku = common_sku.copy()
                sku["size"] = size
                sku["colour"] = colour

                css = self.availability_css.format(row, col)
                if clean(response.css(css)) and colour != self.one_colour:
                    sku["out_of_stock"] = True

                skus[f"{colour}_{size}"] = sku

        return skus


class RakutenCrawler(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + "-crawler"
    parse_spider = RakutenParser()

    listings_css = [".categoryMenu__l1Container", ".dui-pagination"]
    product_css = [".searchresultitems .dui-card"]

    deny_re = ["review", "/gold/"]

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css, deny=deny_re), callback="parse_item")]
