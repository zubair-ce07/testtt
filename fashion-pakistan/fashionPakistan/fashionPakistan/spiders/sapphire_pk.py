# -*- coding: utf-8 -*-
import scrapy
from fashionPakistan.items import FashionPakistan


class SapphirePkSpider(scrapy.Spider):
    name = 'sapphire.pk'
    start_urls = ['https://pk.sapphireonline.pk']

    def parse(self, response):
        category_links = response.xpath(
            "//ul[@id='_menuBar']//ul/li/a/@href").extract()
        for link in category_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath(
            "//a[@class='product-grid-image']/@href").extract()
        for link in product_links:
            yield scrapy.Request(response.urljoin(link), self.parse_product_details)

        next_link = response.xpath(
            "//ul[@class='pagination-page abs']/li/a/i[@class='fa fa-angle-right']").extract()
        if next_link:
            next_link = response.xpath(
                "//ul[@class='pagination-page abs']/li/a/@href").extract()[-1]
            yield scrapy.Request(response.urljoin(next_link), self.parse_product_links)

    def parse_product_details(self, response):
        product = FashionPakistan()
        product["name"] = self.get_item_name(response)
        product["product_sku"] = self.get_item_sku(response)
        product["description"] = self.get_item_description(response)
        product["images"] = self.get_item_images(response)
        product["attributes"] = self.get_item_attributes(response)
        product["out_of_stock"] = self.is_out_of_stock(response)
        product["skus"] = self.get_item_skus(response)
        product["url"] = response.url
        yield product

    def is_out_of_stock(self, response):
        value = response.xpath(
            "//link[@itemprop='availability']/@href").extract_first().split("/")[-1]
        return False if value.strip() == "InStock" else True

    def get_item_name(self, response):
        return response.xpath("//h2[@itemprop='name']/span/text()").extract_first()

    def get_item_sku(self, response):
        return response.xpath("//span[@class='variant-sku']/text()").extract_first()[4:]

    def get_item_description(self, response):
        return response.xpath("//div[@class='short-description']/p/text()").extract()

    def get_item_images(self, response):
        images = response.xpath(
            "//div[@class='MagicToolboxSelectorsContainer']//img/@src").extract()
        return images

    def get_item_attributes(self, response):
        attribute = response.xpath(
            "//div[@id='collapse-tab2']//h4/text()").extract()
        attributes = {}
        for i, attrib in enumerate(attribute):
            desc = response.xpath(
                "//div[@id='collapse-tab2']//ul[{}]//text()".format(i+1)).extract()
            attributes[attrib] = desc

        fabric = response.xpath(
            "//div[@class='short-description']/p/text()").extract()
        if fabric[-1].strip().split(":")[0] == "Fabric":
            attributes["fabric"] = fabric[-1].strip().split(":")[1]
        return attributes

    def get_item_skus(self, response):
        currency = response.xpath(
            "//meta[@itemprop='priceCurrency']/@content").extract_first()
        attribs = response.xpath(
            "//div[@class='swatch clearfix']/div[@class='header']/text()").extract()
        attrib_values_data = response.xpath(
            "//select[@id='product-selectors']/option//text()").extract()
        attrib_values = attrib_values_data[::2]
        prices = attrib_values_data[1::2]
        attrib_values = [attrib.replace(
            "/", "_").replace(" ", '').strip() for attrib in attrib_values]
        color_scheme = {}
        for attrib_value, price in zip(attrib_values, prices):
            attrib_value_split = attrib_value.split("_")
            key = str(attrib_value.strip("-"))
            for val, attrib in zip(attrib_value_split, attribs):
                sub_key = str(attrib).strip("-")
                color_scheme[key][attrib] = str(val).strip("-")

            color_scheme[key]["currency_code"] = currency
            color_scheme[key]["new_price"] = price.strip(
                "Rs.").replace(",", '')

        return color_scheme
