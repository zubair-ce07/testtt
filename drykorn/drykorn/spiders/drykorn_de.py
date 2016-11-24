# -*- coding: utf-8 -*-
import scrapy
from drykorn.items import DrykornItem
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
    start_urls = ['https://www.drykorn.com/de-de/herren/kleidung/hosen/chino.html']

    def parse(self, response):
        document = Selector(text=response.body.decode("UTF-8"))

        product_links = document.xpath(
            '//div[@class="category-products"]//ul[contains(@class, "products-grid")]//li'
            '//a[@class="product-image"]//@href'
        ).extract()

        for link in product_links:
            request = Request(link, callback=self.extract_product_details)
            request.meta["is_first_sibling"] = True

            yield request

    def extract_product_details(self, response):
        document = Selector(text=response.body.decode("UTF-8"))

        product = DrykornItem()

        product["skus"] = self.get_product_skus(document)
        product["date"] = self.get_unix_current_timestamp()
        product["lang"] = "de"

        price_tag = self.get_product_price_and_currency(document)
        product["price"] = price_tag.amount

        product["name"] = self.get_product_name(document)
        product["industry"] = ""
        product["crawl_id"] = "drykorn-de-%s-%s-awrx" % (self.get_current_date(), self.get_unix_current_timestamp())
        product["image_urls"] = self.get_product_image_urls(document)
        product["product_hash"] = ""
        product["gender"] = "men"
        product["retailer_sku"] = self.get_material_number_of_product(document)
        product["market"] = "DE"
        product["url_original"] = response.url
        product["trail"] = self.get_product_route_trace(document)
        product["category"] = self.get_product_categories(document)
        product["uuid"] = None
        product["description"] = self.get_product_description(document)
        product["brand"] = "Drykorn"
        product["url"] = response.url
        product["spider_name"] = self.name
        product["currency"] = price_tag.currency
        product["crawl_start_time"] = self.get_utc_current_timestamp()
        product["retailer"] = "drykorn de"
        product["care"] = self.get_material_info_of_product(document)

        # if response.meta["is_first_sibling"]:
        #     self.collect_info_for_other_pallets(document)

        palette_info = self.collect_info_for_other_colors(document)
        if palette_info.have_multiple_colors:
            product["skus"].update(palette_info.skus)
            product["image_urls"] += palette_info.image_urls

        return product

    def get_unix_current_timestamp(self):
         return int(time.time())

    def get_current_date(self):
        date = datetime.now()
        return date.strftime("%Y%m%d")

    def get_utc_current_timestamp(self):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    def collect_info_for_other_pallets(self, document):
        color_links = document.xpath(
            '//div[contains(@class, "product-shop")]//div[contains(@class, "color-content")]//@href'
        ).extract()

        pallets_requests = []

        for link in color_links:
            request = Request(link, callback=self.extract_product_details)
            request.meta["is_first_sibling"] = False

            pallets_requests.append(request)

        return pallets_requests

    def collect_info_for_other_colors(self, document):
        color_links = document.xpath(
            '//div[contains(@class, "product-shop")]//div[contains(@class, "color-content")]//@href'
        ).extract()

        info = namedtuple("Info", "skus image_urls have_multiple_colors")
        info.skus = {}
        info.image_urls = []
        info.have_multiple_colors = False

        for link in color_links:
            response = requests.get(link)
            document = Selector(text=response.text)

            info.skus.update(self.get_product_skus(document))
            info.image_urls += self.get_product_image_urls(document)

            info.have_multiple_colors = True

        return info

    def get_material_info_of_product(self, document):
        infos = document.xpath(
            '//div[contains(@class, "product-additionals")]//div[@id="product-attribute-specs-table"]//div//text()'
        ).extract()

        infos = [info.strip() for info in infos if info.strip()]
        return infos

    def get_product_categories(self, document):
        categories = document.xpath(
            '//div[@id="header-nav"]//ol[@class="nav-primary"]//li[contains(@class, "active parent")]'
            '/a[1]//span[1]//text()'
        ).extract()

        return categories

    def get_product_description(self, document):
        description = document.xpath(
            '//div[contains(@class, "product-additionals")]//div[@class="info-block"]//ul[1]//li//text()'
        ).extract()

        return description

    def get_product_route_trace(self, document):
        breadcrumb = document.xpath('//div[contains(@class, "main-container")]//div[@class="breadcrumbs"]//ul//li//a')

        required_route = []

        home = (breadcrumb[0].xpath("span/text()").extract_first(), breadcrumb[0].xpath("@href").extract_first())
        required_route.append(home)

        if len(breadcrumb) > 1:
            category = (breadcrumb[-1].xpath("span/text()").extract_first(),
                        breadcrumb[-1].xpath("@href").extract_first())
            required_route.append(category)

        return required_route

    def get_product_image_urls(self, document):
        image_urls = document.xpath(
            '//div[@class="product-view"]//div[@class="product-image-gallery"]//ul//li//img//@src'
        ).extract()

        return image_urls

    def get_material_number_of_product(self, document):
        material_number = document.xpath(
            '//div[contains(@class, "product-additionals")]//div[contains(@class, "material-wrapper")]'
            '//div[@class="data material"]//text()'
        ).extract_first()

        return material_number.strip()

    def get_product_name(self, document):
        name = document.xpath(
            '//div[contains(@class, "sticky-object")]//div[@class="product-name"]//h1//text()'
        ).extract_first()

        return name.strip()

    def get_product_price_and_currency(self, document):
        price_tag = document.xpath(
            '//div[contains(@class, "sticky-object")]//div[@class="price-info"]//span[@class="price"]//text()'
        ).extract_first()

        price_and_currency = namedtuple("Price", "amount currency")
        price_and_currency.amount, price_and_currency.currency = price_tag.split()

        return price_and_currency

    def check_if_product_in_stock(self, size_option):
        stock_status = size_option.xpath("@class").extract_first()

        return True if stock_status.lower() == "available" else False

    def get_product_color_from_page_title(self, document):
        title = document.xpath('//title//text()').extract_first()
        color = re.search("\d{4,}(.*)\|", title).group(1)

        return color.strip().capitalize()

    def get_product_skus(self, document):
        skus = {}

        color = self.get_product_color_from_page_title(document)
        sizes_option = document.xpath(
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

            price_info = self.get_product_price_and_currency(document)
            data[key]["price"], data[key]["currency"] = price_info.amount, price_info.currency

            skus.update(data)

        return skus
