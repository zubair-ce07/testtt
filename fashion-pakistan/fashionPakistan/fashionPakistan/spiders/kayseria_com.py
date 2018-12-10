# -*- coding: utf-8 -*-
import scrapy
from fashionPakistan.items import FashionPakistan


class KayseriaComSpider(scrapy.Spider):
    name = 'kayseria.com'
    start_urls = ['https://www.kayseria.com/']

    def parse(self, response):
        yield scrapy.Request("https://www.kayseria.com/", cookies={"kay-country": "PK"}, callback=self.set_cookies)

    def set_cookies(self, response):
        category_links = response.xpath(
            "//a[@class='level-top']/@href").extract()
        for link in category_links:
            yield scrapy.Request(link, callback=self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath(
            "//a[@class='product-image']/@href").extract()
        for link in product_links:
            yield scrapy.Request(link, self.parse_product_details)

        next_link = response.xpath(
            "//a[@class='next i-next']/@href").extract_first()
        if next_link:
            yield scrapy.Request(next_link, self.parse_product_links)

    def parse_product_details(self, response):
        product = FashionPakistan()
        product["name"] = response.xpath("//div[@class='product-name']/h1/text()").extract_first().strip()
        product["product_sku"] = response.xpath("//table[@id='product-attribute-specs-table']/tbody/tr[1]/td/text()").extract_first().strip()
        product["description"] = self.get_item_description(response)
        product["images"] = response.xpath("//ul[@class='art-vmenu']//img/@src").extract()
        product["attributes"] = self.get_item_attributes(response)
        product["out_of_stock"] = False
        product["skus"] = self.get_item_skus(response)
        product["url"] = response.url
        yield product

    def get_item_description(self, response):
        description = response.xpath(
            "//div[@id='product_tabs_description_tabbed_contents']//text()").extract()[1:-1]
        return [desc.strip() for desc in description]

    def get_item_attributes(self, response):
        attrib_keys = response.xpath(
            "//table[@id='product-attribute-specs-table']/tbody/tr/th/text()").extract()[1:]
        attrib_values = response.xpath(
            "//table[@id='product-attribute-specs-table']/tbody/tr/td/text()").extract()[1:]
        attributes = {}
        for key, value in zip(attrib_keys, attrib_values):
            attributes[key] = value.strip()
        return attributes

    def get_item_sizes(self, response):
        sizes = response.xpath(
            "//ul[@id='configurable_swatch_size']/li/a/@name").extract()
        return [size.strip() for size in sizes]

    def get_item_meter_attribute(self, response):
        meter_prices = response.xpath("//select[contains(@id, 'select_')]/option/@price").extract()[1:]
        meter_values = response.xpath("//select[contains(@id, 'select_')]/option/text()").extract()[1:]
        meter_values = [val.split("+")[0].strip() for val in meter_values]
        return meter_values, meter_prices

    def get_item_skus(self, response):
        color_name = response.xpath("//ul[@id='configurable_swatch_color']/li/a/@name").extract()
        if not(color_name):
            attrib_keys = response.xpath(
                "//table[@id='product-attribute-specs-table']/tbody/tr/th/text()").extract()[1:]
            attrib_values = response.xpath(
                "//table[@id='product-attribute-specs-table']/tbody/tr/td/text()").extract()[1:]
            if "Color" in attrib_keys:
                index = attrib_keys.index("Color")
                color_name = [attrib_values[index]]
        available_sizes = self.get_item_sizes(response)
        meter_attrib, meter_prices = self.get_item_meter_attribute(response)
        price = response.xpath("//span[contains(@id, 'product-price-')]//text()").extract_first()
        if price is None:
            price = response.xpath("//span[contains(@id, 'product-price-')]/span/text()").extract_first()
        if price:
            price = price.strip().strip("PKR ").replace(",", "")
        prev_price = response.xpath(
            "//span[contains(@id, 'old-price-')]//text()").extract_first()
        skus = {}
        if meter_attrib:
            for color in color_name:
                for meter, meter_price in zip(meter_attrib, meter_prices):
                    meter = meter.replace(" ", '_')
                    new_price = int(price) + int(meter_price)
                    skus[color+"_"+meter] = {
                        "color": color,
                        "meter" : meter,
                        "new_price": str(new_price),
                        "currency_code": "PKR",
                    }
                    if prev_price:
                        prev_price = prev_price.strip().strip("PKR ").replace(",", "")
                        prev_new_price = int(prev_price) + int(meter_price)
                        skus[color+"_"+meter]["prev_price"] = str(prev_new_price)
                    if available_sizes:
                        skus[color+"_"+meter]["available_sizes"] = available_sizes
        else:
            for color in color_name:
                skus[color] = {
                    "color": color,
                    "new_price": price,
                    "currency_code": "PKR",
                }
                if prev_price:
                    skus[color]["prev_price"] = prev_price.strip().strip("PKR ").replace(",", '')
                if available_sizes:
                    skus[color]["available_sizes"] = available_sizes
        return skus
