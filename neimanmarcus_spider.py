import json
import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.selector import Selector
from w3lib.url import url_query_cleaner

from .base import BaseCrawlSpider, BaseParseSpider, clean, soupify, Gender


class Mixin:
    retailer = "neimanmarcus"
    default_brand = "Neiman Marcus"
    merch_info_map = [
        ('limited edition', 'Limited Edition')
    ]

    headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
    sku_payload = 'data={{"ProductSizeAndColor":{{"productIds":"{0}"}}}}'

    product_url = "https://www.neimanmarcus.com/en-cn/product.service"
    pagination_url = "https://www.neimanmarcus.com/category.service"
    region_url = 'https://www.neimanmarcus.com/dt/api/profileCountryData'
    image_url_t = "http://neimanmarcus.scene7.com/is/image/NeimanMarcus/{0}?&wid=1200&height=1500"


class MixinCN(Mixin):
    retailer = Mixin.retailer + "-cn"
    market = "CN"

    start_urls = ["https://www.neimanmarcus.com", ]
    allowed_domains = ["neimanmarcus.com"]

    region_payload = {"country": "CN", "currency": "CNY"}


class MixinJP(Mixin):
    retailer = Mixin.retailer + "-jp"
    market = "JP"

    start_urls = ["https://www.neimanmarcus.com", ]
    allowed_domains = ["neimanmarcus.com"]

    region_payload = {"country": "JP", "currency": "JPY"}


class MixinHK(Mixin):
    retailer = Mixin.retailer + "-hk"
    market = "HK"

    start_urls = ["https://www.neimanmarcus.com", ]
    allowed_domains = ["neimanmarcus.com"]

    region_payload = {"country": "HK", "currency": "HKD"}


class MixinTW(Mixin):
    retailer = Mixin.retailer + "-tw"
    market = "TW"

    start_urls = ["https://www.neimanmarcus.com", ]
    allowed_domains = ["neimanmarcus.com"]

    region_payload = {"country": "TW", "currency": "TWD"}


class ParseSpider(BaseParseSpider):
    raw_description_css = ".productCutline ::text, .cutlineDetails ::text"
    price_css = ".product-details-source .item-price::text, " \
                ".product-details-source .product-price::text"

    def parse(self, response):
        response.meta["response"] = response
        yield self.sku_requests(response)

    def parse_raw_skus(self, response):
        raw_skus = json.loads(response.text)["ProductSizeAndColor"]["productSizeAndColorJSON"]
        return json.loads(raw_skus)

    def parse_products(self, response):
        raw_skus = self.parse_raw_skus(response)
        primary_response = response.meta["response"]
        product_sels = primary_response.css(".hero-zoom-frame")

        for product_sel, raw_sku in zip(product_sels, raw_skus):
            product_id = self.product_id(product_sel)
            garment = self.new_unique_garment(product_id)

            if not garment:
                return

            self.boilerplate(garment, primary_response)

            garment['name'] = self.product_name(product_sel)
            garment['description'] = self.product_description(product_sel)
            garment['care'] = self.product_care(product_sel)
            garment["image_urls"] = self.image_urls(product_sel)
            garment['category'] = self.product_category(primary_response)
            garment["brand"] = self.product_brand(product_sel)
            garment["gender"] = self.product_gender(garment)
            garment["merch_info"] = self.merch_info(garment)
            garment["skus"] = self.skus(raw_sku, product_sel)

            yield garment

    def product_id(self, response):
        css = ".prod-img::attr(prod-id)"
        return clean(response.css(css))[0]

    def merch_info(self, garment):
        soup = soupify([garment['name']] + garment['description']).lower()
        return [merch for merch_str, merch in self.merch_info_map if merch_str in soup]

    def product_brand(self, response):
        css = ".prodDesignerName a::text, .prodDesignerName::text, .product-designer a::text"
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = ".product-name span+span::text"
        return clean(response.css(css))[0]

    def product_category(self, response):
        css = "script:contains('@graph')::text"
        regex = 'category":"(.+?)"'
        raw_category = response.css(css).re_first(regex)
        return raw_category.split("/") if raw_category else []

    def product_gender(self, garment):
        soup = soupify(garment["category"] + garment["description"] + [garment["name"]])
        return self.gender_lookup(soup, True) or Gender.ADULTS.value

    def image_urls(self, response):
        images = clean(response.css("#color-pickers .color-picker::attr(data-sku-img)"))
        return [self.image_url_t.format(image_id) for image in images
                for image_id in json.loads(image).values()] or \
                clean(response.css(".img-wrap img::attr(data-zoom-url)"))

    def sku_requests(self, response):
        raw_product_id = clean(response.css(".prod-img::attr(prod-id)"))

        product_id = soupify(raw_product_id, ",")
        payload = self.sku_payload.format(product_id)

        return Request(self.product_url, self.parse_products, dont_filter=True, body=payload,
                       method="POST", headers=self.headers, meta=response.meta.copy())

    def skus(self, raw_skus, product_sel):
        skus = {}
        common_sku = self.product_pricing_common(product_sel)

        for raw_sku in raw_skus["skus"]:
            sku = common_sku.copy()

            color = raw_sku.get("color")
            if color:
                sku["colour"] = color.split("?")[0]

            sku["size"] = raw_sku.get('size') or self.one_size

            if raw_sku["status"] != "In Stock":
                sku["out_of_stock"] = True

            sku_id = f"{sku['colour']}_{sku['size']}" if color else sku["size"]
            skus[sku_id] = sku

        return skus


class CrawlSpider(BaseCrawlSpider):
    listings_css = [
        ".silo-nav",
        ".designerlist",
    ]
    products_css = [
        ".product-list",
        ".category-items",
        ".products"
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=products_css), callback="parse_item")
    )

    def start_requests(self):
        headers = {"content-type": "application/json;charset=UTF-8"}
        yield Request(self.region_url, self.parse_region, method='POST', body=json.dumps(self.region_payload), headers=headers)

    def parse_region(self, response):
        return [Request(url, self.parse) for url in self.start_urls]

    def parse(self, response):
        yield from super().parse(response)
        yield from self.parse_pagination(response)

    def parse_pagination(self, response):
        total_pages = clean(response.css("#epagingBottom li::attr(pagenum)"))

        if not total_pages:
            return []

        meta = self.get_meta_with_trail(response)
        category = url_query_cleaner(response.url)
        category_id = re.findall("cat(.+)", category)[0]

        parameters = 'data={{{{"GenericSearchReq":{{{{"pageOffset":{{0}},"pageSize":"30","mobile":false,' \
                     '"definitionPath":"/nm/commerce/pagedef rwd/template/EndecaDrivenHome","categoryId":' \
                     '"cat{category}"}}}}}}}}&service=getCategoryGrid&sid=getCategoryGrid'.format(category=category_id)

        return [Request(self.pagination_url, self.product_requests, method="POST",
                        body=parameters.format(page), headers=self.headers, meta=meta) for page in total_pages]

    def product_requests(self, response):
        meta = self.get_meta_with_trail(response)

        raw_category = json.loads(response.text)
        raw_products = Selector(text=raw_category['GenericSearchResp']['productResults'])
        urls = clean(raw_products.css(".products .product .details a::attr(href)"))

        return [response.follow(url, self.parse_item, meta=meta) for url in urls]


class ParseSpiderCN(MixinCN, ParseSpider):
    name = MixinCN.retailer + "-parse"


class CrawlSpiderCN(MixinCN, CrawlSpider):
    name = MixinCN.retailer + "-crawl"
    parse_spider = ParseSpiderCN()


class ParseSpiderJP(MixinJP, ParseSpider):
    name = MixinJP.retailer + "-parse"


class CrawlSpiderJP(MixinJP, CrawlSpider):
    name = MixinJP.retailer + "-crawl"
    parse_spider = ParseSpiderJP()


class ParseSpiderHK(MixinHK, ParseSpider):
    name = MixinHK.retailer + "-parse"


class CrawlSpiderHK(MixinHK, CrawlSpider):
    name = MixinHK.retailer + "-crawl"
    parse_spider = ParseSpiderHK()


class ParseSpiderTW(MixinTW, ParseSpider):
    name = MixinTW.retailer + "-parse"


class CrawlSpiderTW(MixinTW, CrawlSpider):
    name = MixinTW.retailer + "-crawl"
    parse_spider = ParseSpiderTW()
