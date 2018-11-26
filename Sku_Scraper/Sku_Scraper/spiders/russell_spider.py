import json
import re

import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from w3lib.url import add_or_replace_parameter, urljoin, urlparse

from ..items import Product


class RussellParseSpider(scrapy.Spider):
    name = "russell_parse_spider"
    seen_ids = set()
    gender_map = {
            "women": "women",
            "girl": "girls",
            "boy": "boys",
            "her": "women",
            "men": "men",
            "his": "men",
        }

    def parse(self, response):
        product_id = self.extract_pid(response)

        if self.is_seen_item(product_id):
            return

        product_loader = ItemLoader(item=Product(), response=response)
        product_loader.add_value("pid", product_id)

        gender = self.detect_gender(response)
        product_loader.add_value("gender", gender)

        category = self.extract_category(response)
        product_loader.add_value("category", category)

        url = self.extract_url(response)
        product_loader.add_value("url", url)

        name = self.extract_name(response)
        product_loader.add_value("name", name)

        description = self.extract_description(response)
        product_loader.add_value("description", description)

        image_urls = self.extract_image_urls(response)
        product_loader.add_value("image_urls", image_urls)

        skus = self.extract_skus(response)
        product_loader.add_value("skus", skus)

        yield product_loader.load_item()
        
    def is_seen_item(self, product_id):
        if product_id in self.seen_ids:
            return True

        self.seen_ids.add(product_id)

    def extract_pid(self, response):
        css = "[itemprop='productID']::text"
        return response.css(css).extract_first()

    def detect_gender(self, response):
        soup = self.extract_category(response) + \
               self.extract_description(response) + \
               [self.extract_url(response)]
        soup = " ".join(soup)
        
        for gender_str, gender in self.gender_map.items():
            if gender_str in soup:
                return gender

        return "unisex-adults"

    def extract_category(self, response):
        css = ".crumbtrail a::text"
        return response.css(css).extract()    

    def extract_url(self, response):
        css = "[property='og:url']::attr(content)"
        return response.css(css).extract_first()

    def extract_name(self, response):
        css = ".headerDetails .invtdesc2::text"
        return response.css(css).extract_first()

    def extract_description(self, response):
        css ="[name='description']::attr(content), .productSpec .pdxtvalue::text"
        return response.css(css).extract()

    def extract_image_urls(self, response):
        script_x = "//script[contains(., '\"param\": \"\",')]/text()"
        raw_urls = response.xpath(script_x).re_first(r"\[.*\]")

        urls = json.loads(raw_urls)
        return [url for url in urls if url.strip()]

    def extract_skus(self, response):
        skus = []

        price_css = ".oneProductContent [itemprop='price']::text"
        price = response.css(price_css).extract_first()

        currency_css = "[itemprop='priceCurrency']::attr(content)"
        currency = response.css(currency_css).extract_first()

        product_id = self.extract_pid(response).strip()
        colour_css = f"[name='set_oitemxoixtcolour_{product_id}']::attr(value)"
        colour = response.css(colour_css).extract_first()

        common_sku = {
            "currency" : currency,
            "price" : price,
            "colour" : colour
        }

        skus_x = "//script[contains(., 'Venda.Attributes.StoreJSON')]/text()"
        raw_skus = response.xpath(skus_x).re(r"{\"atronhand.*}")

        for raw_sku in raw_skus:
            raw_size = json.loads(raw_sku)
            sku = common_sku.copy()

            size = raw_size["atr1"]
            sku["size"] = size
            
            if not raw_size["atronhand"]:
                sku["out_of_stock"] = True

            sku["sku_id"] = f"{colour}_{size}" if colour else size
            skus.append(sku)

        return skus        


def fix_url(url):
    parsed_url = urlparse(url)
    return f"http://www.russellandbromley.co.uk{parsed_url.path}?{parsed_url.query}"


class RussellCrawlSpider(CrawlSpider):
    parse_spider = RussellParseSpider()
    name = "russell_crawl_spider"
    listing_url_t = "http://fsm.attraqt.com/zones-js.aspx/?" \
                    "siteId=ba6279ce-57d8-4069-8651-04459b92bceb&zone0=category&" \
                    "pageurl={}&config_categorytree={}&config_category={}"

    start_urls = ["http://www.russellandbromley.co.uk/"]
    allowed_domains = ["russellandbromley.co.uk", "fsm.attraqt.com"]
    listings_css = [".mm_ul", ".subCategoryTrend, .subCategory", ".pagnNext"]
    product_css = [".image > .moredetail"]
    rules = (
        Rule(LinkExtractor(restrict_css=(listings_css)), callback="parse_categories"),
        Rule(LinkExtractor(restrict_css=(product_css), process_value=fix_url), 
            callback="parse_item"),
    )  

    def parse_categories(self, response):
        if not response.css('div::attr(lmzone)'):
            return self.parse(response)    

        configuration_x = "//script[contains(., 'LM.config')]/text()"
        raw_category_tree = response.xpath(configuration_x).re_first(r"\"categorytree.*\"")
        category_tree = raw_category_tree.split(",")[1].strip("\"")

        raw_category = response.xpath(configuration_x).re_first(r"\"category\".*\"")
        category = raw_category.split(",")[1].strip("\"")

        listing_url = self.listing_url_t.format(response.url, category_tree, category)
        if "esp_pg" in response.url:
            listing_url = add_or_replace_parameter(listing_url, "mergehash", "true")

        return scrapy.Request(listing_url, callback=self.parse_listings)
    
    def parse_listings(self, response):
        html_text = self.extract_html(response)
        response = HtmlResponse(url=response.url, body=html_text.encode())
        return self.parse(response)

    def parse_item(self, response):
        return self.parse_spider.parse(response)       

    def extract_html(self, response):
        raw_html = re.findall(r'{.*}', response.text)[1]
        return json.loads(raw_html)["html"]    
