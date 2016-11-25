# -*- coding: utf-8 -*-
import scrapy
from drykorn.items import DrykornItem
from scrapy.contrib.linkextractors import LinkExtractor
from parsel import Selector
import requests
from scrapy import Request
import re
from collections import namedtuple
import time
from datetime import datetime
import pdb


class DrykornDeSpider(scrapy.Spider):
    name = "drykorn_de"
    allowed_domains = ["drykorn.com"]
    start_urls = ['https://www.drykorn.com/de-de']

    def parse(self, response):
        category_links = LinkExtractor(restrict_css='div#header-nav li.level2 a.level2').extract_links(response)
        for link in category_links:
            request = Request(link.url, callback=self.parse_category_page)
            yield request

    def parse_category_page(self, response):
        product_links = LinkExtractor(
            restrict_css='div.category-products ul.products-grid li div.plist-item-image a.product-image',
            unique=True
        ).extract_links(response)

        for link in product_links:
            request = Request(link.url, callback=self.extract_product_details)
            request.meta["siblings_processing"] = False
            request.meta["siblings"] = []
            yield request

    def extract_product_details(self, response):

        product = DrykornItem()

        product["skus"] = self.get_product_skus(response)
        product["date"] = self.get_unix_current_timestamp()
        product["lang"] = "de"

        price_tag = self.get_product_price_and_currency(response)
        product["price"] = price_tag.amount

        product["name"] = self.get_product_name(response)
        product["industry"] = ""
        product["crawl_id"] = "drykorn-de-%s-%s-awrx" % (self.get_current_date(), self.get_unix_current_timestamp())
        product["image_urls"] = self.get_product_image_urls(response)
        product["product_hash"] = ""
        product["gender"] = "men"
        product["retailer_sku"] = self.get_material_number_of_product(response)
        product["market"] = "DE"
        product["url_original"] = response.url
        product["trail"] = self.get_product_route_trace(response)
        product["category"] = self.get_product_categories(response)
        product["uuid"] = None
        product["description"] = self.get_product_description(response)
        product["brand"] = "Drykorn"
        product["url"] = response.url
        product["spider_name"] = self.name
        product["currency"] = price_tag.currency
        product["crawl_start_time"] = self.get_utc_current_timestamp()
        product["retailer"] = "drykorn de"
        product["care"] = self.get_material_info_of_product(response)

        if response.meta["siblings_processing"]:
            sibling_product = response.meta["product"]
            product = self.merge_sibling_palettes_details(product, sibling_product)

        entity_to_yield = product
        other_palettes_links = self.get_links_for_other_palettes(response)

        if other_palettes_links:
            yield self.initiate_request_for_sibling_palettes(product, other_palettes_links)
            entity_to_yield = None

        yield entity_to_yield

    def get_unix_current_timestamp(self):
         return int(time.time())

    def get_current_date(self):
        date = datetime.now()
        return date.strftime("%Y%m%d")

    def get_utc_current_timestamp(self):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    def merge_sibling_palettes_details(self, product, sibling):
        product["skus"].update(sibling["skus"])
        product["image_urls"] += sibling["image_urls"]

        return product

    def initiate_request_for_sibling_palettes(self, product, siblings_palettes):
        request = Request(siblings_palettes.pop(), callback=self.extract_product_details)
        request.meta["product"] = product

        request.meta["siblings"] = siblings_palettes
        request.meta["siblings_processing"] = True

        return request

    def get_links_for_other_palettes(self, response):
        color_links = []

        if response.meta["siblings_processing"]:
            color_links = response.meta["siblings"]
        else:
            extracted_links = LinkExtractor(restrict_css='div.product-shop div.color-content').extract_links(response)
            for link in extracted_links:
                color_links.append(link.url)

        return color_links

    def get_material_info_of_product(self, response):
        infos = response.xpath(
            '//div[contains(@class, "product-additionals")]//div[@id="product-attribute-specs-table"]//div//text()'
        ).extract()

        infos = [info.strip() for info in infos if info.strip()]
        return infos

    def get_product_categories(self, response):
        categories = response.css('div#header-nav ol.nav-primary li.active.parent > a span::text').extract()

        return categories

    def get_product_description(self, response):
        description = response.css('div.product-additionals div.info-block ul li::text').extract()

        return description

    def get_product_route_trace(self, response):
        required_route = []

        breadcrumb = LinkExtractor(restrict_css='div.main-container div.breadcrumbs ul li').extract_links(response)
        for link in breadcrumb:
            required_route.append((link.text.strip(), link.url))

        return required_route

    def get_product_image_urls(self, response):
        image_urls = response.xpath(
            '//div[@class="product-view"]//div[@class="product-image-gallery"]//ul//li//img//@data-zoom-image'
        ).extract()

        return image_urls

    def get_material_number_of_product(self, response):
        material_number = response.xpath(
            '//div[contains(@class, "product-additionals")]//div[contains(@class, "material-wrapper")]'
            '//div[@class="data material"]//text()'
        ).extract_first()

        return material_number.strip()

    def get_product_name(self, response):
        name = response.xpath(
            '//div[contains(@class, "sticky-object")]//div[@class="product-name"]//h1//text()'
        ).extract_first()

        return name.strip()

    def get_product_price_and_currency(self, response):
        price_tag = response.xpath(
            '//div[contains(@class, "sticky-object")]//div[@class="price-info"]//span[@class="price"]//text()'
        ).extract_first()

        if not price_tag:
            price_line = response.css('div.cart-totals-wrapper p#total-price::text').extract_first()
            price_tag = " ".join(price_line.split(':')[-1].split())

        price_and_currency = namedtuple("Price", "amount currency")
        price_and_currency.amount, price_and_currency.currency = price_tag.split()

        return price_and_currency

    def check_if_product_in_stock(self, size_option):
        stock_status = size_option.xpath("@class").extract_first()

        return stock_status.lower() == "available"

    def get_product_color_from_material_info(self, response):
        color = response.css('div.product-infos div.data-table div.color::text').extract_first()

        return color.strip().capitalize()

    def get_product_color_from_page_title(self, response):
        title = response.xpath('//title//text()').extract_first()
        color = re.search("\d{4,}(.*)\|", title).group(1)

        return color.strip().capitalize()

    def get_product_skus(self, response):
        skus = {}

        color = self.get_product_color_from_material_info(response)
        sizes_option = response.xpath(
            '//div[@class="sticky-object"]//div[@id="product-options-wrapper"]//select//option'
        )

        for size in sizes_option[1:]:
            data = {}

            size_label = size.xpath("@data-label").extract_first()
            key = "%s_%s" % (color, size_label)

            data[key] = {}

            data[key]["out_of_stock"] = self.check_if_product_in_stock(size)
            data[key]["size"] = size_label
            data[key]["color"] = color

            price_info = self.get_product_price_and_currency(response)
            data[key]["price"], data[key]["currency"] = price_info.amount, price_info.currency

            skus.update(data)

        return skus
