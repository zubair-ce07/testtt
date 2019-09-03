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


class MixinCN(Mixin):
    retailer = Mixin.retailer + "-cn"
    market = "CN"

    start_urls = [
        "https://www.neimanmarcus.com",
        ]

    allowed_domains = ["neimanmarcus.com"]

    product_req_t = 'data={{"ProductSizeAndColor":{{"productIds":"{0}"}}}}&sid=getSizeAndColorData&bid=ProductSizeAndColor'
    product_url = "https://www.neimanmarcus.com/en-cn/product.service"
    content_type = "application/x-www-form-urlencoded; charset=UTF-8"
    body = {"country": "CN", "currency": "CNY"}


class MixinJP(Mixin):
    retailer = Mixin.retailer + "-jp"
    market = "JP"

    start_urls = [
        "https://www.neimanmarcus.com",
        ]

    allowed_domains = ["neimanmarcus.com"]

    product_req_t = 'data={{"ProductSizeAndColor":{{"productIds":"{0}"}}}}&sid=getSizeAndColorData&bid=ProductSizeAndColor'
    product_url = "https://www.neimanmarcus.com/en-cn/product.service"
    content_type = "application/x-www-form-urlencoded; charset=UTF-8"
    body = {"country": "JP", "currency": "JPY"}


class MixinHK(Mixin):
    retailer = Mixin.retailer + "-hk"
    market = "HK"

    start_urls = [
        "https://www.neimanmarcus.com",
        ]

    allowed_domains = ["neimanmarcus.com"]

    product_req_t = 'data={{"ProductSizeAndColor":{{"productIds":"{0}"}}}}&sid=getSizeAndColorData&bid=ProductSizeAndColor'
    product_url = "https://www.neimanmarcus.com/en-cn/product.service"
    content_type = "application/x-www-form-urlencoded; charset=UTF-8"
    body = {"country": "HK", "currency": "HKD"}


class MixinTW(Mixin):
    retailer = Mixin.retailer + "-tw"
    market = "TW"

    start_urls = [
        "https://www.neimanmarcus.com",
        ]

    allowed_domains = ["neimanmarcus.com"]

    product_req_t = 'data={{"ProductSizeAndColor":{{"productIds":"{0}"}}}}&sid=getSizeAndColorData&bid=ProductSizeAndColor'
    product_url = "https://www.neimanmarcus.com/en-cn/product.service"
    content_type = "application/x-www-form-urlencoded; charset=UTF-8"
    body = {"country": "TW", "currency": "TWD"}


class ParseSpider(BaseParseSpider):
    raw_description_css = ".productCutline ::text, .cutlineDetails ::text"
    price_css = ".product-details-source .item-price::text, .product-details-source .product-price::text"

    def parse_individual_products(self, response):
        raw_skus = json.loads(response.text)["ProductSizeAndColor"]["productSizeAndColorJSON"]
        response_html = response.meta["response"]

        for selectors, raw_json in zip(response_html.css(".hero-zoom-frame"), json.loads(raw_skus)):
            product_id = self.product_id(selectors)
            garment = self.new_unique_garment(product_id)

            if not garment:
                return

            self.boilerplate_normal(garment, response_html)

            garment["image_urls"] = self.image_urls(selectors)
            garment["skus"] = {}
            garment['category'] = self.product_category(response)
            garment["gender"] = self.product_gender(garment)
            garment["skus"] = self.skus(raw_json, response_html)
            yield garment

    def parse(self, response):
        response.meta["response"] = response
        yield self.sku_requests(response)

    def product_id(self, response):
        css = ".prod-img::attr(prod-id)"
        return clean(response.css(css))[0]

    def product_brand(self, response):
        css = ".prodDesignerName a::text, .prodDesignerName::text"
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = ".product-name span::text"
        return clean(response.css(css))[0]

    def product_category(self, response):
        return ["Clothes"]

    def product_gender(self, garment):
        soup = soupify(garment["name"], garment["trail"])
        return self.gender_lookup(soup, True) or Gender.ADULTS.value

    def image_urls(self, response):
        return clean(response.css(".img-wrap img::attr(data-zoom-url)"))

    def sku_requests(self, response):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        product_id = clean(response.css(".prod-img::attr(prod-id)"))
        refined_product_id = ','.join(product_id) if len(product_id) > 1 else product_id[0]
        payload_data = self.product_req_t.format(refined_product_id)
        meta = {'response': response.meta["response"]}

        return Request(self.product_url, self.parse_individual_products, dont_filter=True, body=payload_data, method="POST", headers=headers, meta=meta)

    def skus(self, raw_json, response_html):
        skus = {}
        common_sku = self.product_pricing_common(response_html)
        sku = common_sku.copy()

        for item in raw_json["skus"]:
            sku["colour"] = item.get("color", "One color?").split("?")[0]
            sku["size"] = item.get("size", "Single size")

            if item["status"] == "Out of Stock":
                sku["out_of_stock"] = True

            sku_id = f"{sku['colour']}_{sku['size']}" if sku["colour"] else sku["size"]
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
        url = 'https://www.neimanmarcus.com/dt/api/profileCountryData?instart_disable_injection=true'

        yield Request(url, self.parse_region, method='POST', body=json.dumps(self.body), headers=headers)

    def parse_region(self, response):
        yield Request(self.start_urls[0], self.parse)

    def parse(self, response):
        yield from super(CrawlSpider, self).parse(response)

        requests = self.parse_pagination(response)
        if requests:
            yield from requests

    def parse_pagination(self, response):
        pages = clean(response.css("#epagingBottom li::attr(pagenum)"))
        if pages:
            url = "https://www.neimanmarcus.com/category.service"
            parameters = 'data={{"GenericSearchReq":{{"pageOffset":{0},"pageSize":"30","mobile":false,"definitionPath":"/nm/commerce/pagedef_' \
                         'rwd/template/EndecaDrivenHome","categoryId":"cat{1}"}}}}&service=getCategoryGrid&sid=getCategoryGrid'
            headers = {"content-type": "application/x-www-form-urlencoded"}

            category = url_query_cleaner(response.url)
            category_id = re.findall("cat(.+)", category)[0]
            meta = {'trail': self.add_trail(response)}

            return [Request(url, self.parse_page, method="POST", body=parameters.format(page, category_id), headers=headers, meta=meta.copy()) for page in pages]

    def parse_page(self, response):
        raw_product_links = json.loads(response.text)["GenericSearchResp"]["productResults"]
        url_html = Selector(text=raw_product_links)
        urls = clean(url_html.css(".products .product .details a::attr(href)"))
        meta = {'trail': self.add_trail(response)}

        return [response.follow(url, self.parse_item,  meta=meta.copy()) for url in urls]


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
