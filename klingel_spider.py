import re

from scrapy import Request, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from w3lib.url import url_query_cleaner

from .base import BaseCrawlSpider, BaseParseSpider, clean, Gender


class Mixin:
    allowed_domains = ["klingel.de"]
    start_urls = ["www.klingel.de"]

    market = "DE"
    retailer = "klingel-de"
    default_brand = "klingel"

    category_req_url = "https://www.klingel.de/AjaxCategoryNavDataJSONView?" \
                       "catalogId=1000100000&langId=-3&storeId=100004"
    ajax_url_t = "AjaxProductDescription?storeId=100004&langId=-3&catalogId=1000100000&productId={}"


class KlingelParser(Mixin, BaseParseSpider):
    name = Mixin.retailer + "-parse"

    description_css = "span[itemprop='description']::text"
    care_css = ".materialDescription ::text"
    brand_css = ".brandName::text"
    price_css = "span[id*='offerPrice']::text"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)

        garment["image_urls"] = self.image_urls(response)
        garment["category"] = self.product_category(response)
        garment["gender"] = self.product_gender(garment)
        garment["skus"] = {}

        garment["meta"] = {"requests_queue": self.colour_requests(response)}

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        css = "#productPartNumber::attr(value)"
        return clean(response.css(css))[0]

    def product_name(self, response):
        css = ".productName ::text"
        return " ".join(clean(response.css(css)))

    def product_category(self, response):
        css = "a[id*='WC_BreadCrumb_Link'] ::text"
        return clean(response.css(css))

    def product_gender(self, garment):
        soup = " ".join(garment["description"] + [garment["name"]] + garment["category"])
        return self.gender_lookup(soup) or Gender.ADULTS.value

    def image_urls(self, response):
        css = ".productThumbNail::attr(src)"
        raw_img_urls = clean(response.css(css))
        return [url_query_cleaner(response.urljoin(url)) for url in raw_img_urls]

    def colour_id(self, response):
        css = "input[name='productId']::attr(value)"
        return clean(response.css(css))[0]

    def colour_requests(self, response):
        colours_css = ".color::attr(title)"
        colours = clean(response.css(colours_css))
        colour_id = self.colour_id(response)

        return [FormRequest(response.urljoin(self.ajax_url_t.format(colour_id)),
                            callback=self.parse_colour, formdata={"colorId": colour},
                            dont_filter=True) for colour in colours]

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['meta']["requests_queue"] += self.size_requests(response)
        return self.next_request_or_garment(garment)

    def size_requests(self, response):
        size_css = ".sizeLabel::attr(id), .singleSize::text"
        sizes = clean(response.css(size_css))

        selected_colour_css = "input[name='selectedColor']::attr(value)"
        selected_colour = clean(response.css(selected_colour_css))[0]

        return [FormRequest(response.url, callback=self.parse_size,
                            formdata={"colorId": selected_colour, "sizeId": size},
                            dont_filter=True) for size in sizes]

    def parse_size(self, response):
        garment = response.meta['garment']
        garment["skus"].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def skus(self, response):
        colour_css = "input[name='selectedColor']::attr(value)"
        size_css = "input[name='selectedSize']::attr(value)"
        unavailable_size_css = ".productSizes > .unavailable > .sizeLabel::attr(id)"
        unavailable_sizes = clean(response.css(unavailable_size_css))

        sku = self.product_pricing_common(response)

        sku["colour"] = clean(response.css(colour_css))[0]

        size = clean(response.css(size_css))
        sku["size"] = size[0] if size else self.one_size

        if sku["size"] in unavailable_sizes:
            sku["out_of_stock"] = True

        return {f"{sku['colour']}_{sku['size']}": sku}


class KlingelCrawler(Mixin, BaseCrawlSpider):
    name = Mixin.retailer + "-crawl"
    parse_spider = KlingelParser()

    product_css = [".productBoxContainer"]
    pagination_css = [".categoryPageNumberNext"]

    rules = [
        Rule(LinkExtractor(restrict_css=pagination_css), callback="parse"),
        Rule(LinkExtractor(restrict_css=product_css), callback="parse_item")]

    def start_requests(self):
        yield Request(self.category_req_url, callback=self.parse_category)

    def parse_category(self, response):
        script_re = "url : '(.*)'"
        category_urls = re.findall(script_re, response.text)

        return [response.follow(url, callback=self.parse) for url in category_urls]
