import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner

from ..items import Product


class CottonParseSpider(scrapy.Spider):
    name = "cotton_parse_spider"
    seen_ids = []
    gender_map = {
            "women": "women",
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

        url = self.extract_product_url(response)
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

        self.seen_ids.append(product_id)    

    def extract_pid(self, response):
        css = "span::attr(data-masterid)"
        return response.css(css).extract_first()

    def detect_gender(self, response):
        soup = self.extract_category(response) + \
               self.extract_description(response) + \
               [self.extract_product_url(response)]
        soup = " ".join(soup)

        for gender_str, gender in self.gender_map.items():
            if gender_str in soup:
                return gender

        return "unisex-adults"

    def extract_category(self, response):
        css = ".b-breadcrumb_link::text"
        return response.css(css).extract()

    def extract_product_url(self, response):
        css = "[property='og:url']::attr(content)"
        return response.css(css).extract_first()

    def extract_name(self, response):
        css = "[property='og:title']::attr(content)"
        return response.css(css).extract_first()

    def extract_description(self, response):
        css = ".b-tabs_product-description li::text, .b-tabs_product-description::text"
        return response.css(css).extract()

    def extract_image_urls(self, response):
        css = ".b-pdp-main_image-carousel_thumbnails-list img::attr(data-src)"
        raw_images = response.css(css).extract()

        return [url_query_cleaner(url) for url in raw_images]

    def extract_skus(self, response):
        skus = []
        in_stocks = ["in-stock", "low-stock", "in stock", "low stock"]

        price_css = "[property='og:product:price:amount']::attr(content)"
        price = response.css(price_css).extract_first()

        currency_css = "[property='og:product:price:currency']::attr(content)"
        currency = response.css(currency_css).extract_first()

        common_skus = {
            "price": price,
            "currency": currency
        }

        size_css = ".b-product_variations-size_value > span::text"
        sizes = response.css(size_css).extract() or ["One size"]

        skus_css = ".b-product_variations-table_row"
        skus_s = response.css(skus_css) or [response]

        for sku_s in skus_s:
            colour_css = ".b-product_variations-color_link::attr(data-color), \
                          .b-pdp-summary_selected_attribute_id:contains(Colour) + span::text"
                              
            colour = sku_s.css(colour_css).extract_first()
            common_skus["colour"] = colour

            stock_css = ".b-product_variations-value::attr(data-initial-classes), \
                         .availability-msg > span::text"
                         
            stocks = sku_s.css(stock_css).extract()

            for stock, size in zip(stocks, sizes):
                sku = common_skus.copy()
                sku["size"] = size

                if stock.strip().lower() not in in_stocks:
                    sku["out_of_stock"] = True

                sku["sku_id"] = f"{colour}_{size}" if colour else f"{size}"

                skus.append(sku)
        return skus


class CottonCrawlSpider(CrawlSpider):
    name = "cotton_crawl_spider"
    start_urls = [
        "https://www.cottontraders.com/on/demandware.store/Sites-cotton-uk-Site/ \
         en_IE/Header-Change?siteId=cotton-uk&localeMnemonic=en_IE"
    ]

    allowed_domains = ["cottontraders.com"]
    parse_spider = CottonParseSpider()

    listings_css = [".h-mobile .b-categories_navigation-level_2-link",
                    ".b-loadmore_container"]
    product_css = ".b-search-result_product .b-product-tile_product-name"

    rules = (
        Rule(LinkExtractor(restrict_css=(listings_css))),
        Rule(LinkExtractor(restrict_css=(product_css)),
             callback="parse_item"),
    )

    def parse_item(self, response):
        return self.parse_spider.parse(response)

