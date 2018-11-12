# -*- coding: utf-8 -*-
import scrapy
from fashionPakistan.items import FashionPakistan


class KayseriaComSpider(scrapy.Spider):
    name = 'kayseria.com'
    start_urls = ['https://www.kayseria.com/']

    def parse(self, response):
        yield scrapy.Request("https://www.kayseria.com/", cookies={"kay-country": "PK"}, callback=self.set_cookies)

    def set_cookies(self, response):
        category_links = response.xpath("//a[@class='level-top']/@href").extract()
        for link in category_links:
            yield scrapy.Request(link, callback=self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath(
            "//a[@class='product-image']/@href").extract()
        for link in product_links:
            yield scrapy.Request(link, self.parse_product_details)

        next_link = response.xpath("//a[@class='next i-next']/@href").extract_first()
        if next_link:
            yield scrapy.Request(next_link, self.parse_product_links)

    def parse_product_details(self, response):
        product = FashionPakistan()
        product["name"] = self.get_item_name(response)
        product["product_sku"] = self.get_item_sku(response)
        product["description"] = self.get_item_description(response)
        product["images"] = self.get_item_images(response)
        product["attributes"] = self.get_item_attributes(response)
        product["out_of_stock"] = "inStock"
        product["skus"] = self.get_item_skus(response)
        product["url"] = response.url
        yield product

    def get_item_name(self, response):
        return response.xpath("//div[@class='product-name']/h1/text()").extract_first().strip()

    def get_item_sku(self, response):
        return response.xpath("//table[@id='product-attribute-specs-table']/tbody/tr[1]/td/text()").extract_first().strip()

    def get_item_description(self, response):
        description = response.xpath("//div[@id='product_tabs_description_tabbed_contents']//text()").extract()[1:-1]
        return [desc.strip() for desc in description]

    def get_item_images(self, response):
        images = response.xpath(
            "//ul[@class='art-vmenu']//img/@src").extract()
        return images

    def get_item_attributes(self, response):
        attrib_keys = response.xpath("//table[@id='product-attribute-specs-table']/tbody/tr/th/text()").extract()[1:]
        attrib_values = response.xpath("//table[@id='product-attribute-specs-table']/tbody/tr/td/text()").extract()[1:]
        attributes = {}
        for key, value in zip(attrib_keys, attrib_values):
            attributes[key] = value.strip()
        return attributes

    def get_item_sizes(self, response):
        sizes = response.xpath("//ul[@id='configurable_swatch_size']//span[@class='swatch-label swatch-label_hover']/text()").extract()
        return [size.strip() for size in sizes]
    
    def get_item_skus(self, response):
        color_name = response.xpath("//span[@id='select_label_']/text()").extract_first()
        if not(color_name):
            attrib_keys = response.xpath("//table[@id='product-attribute-specs-table']/tbody/tr/th/text()").extract()[1:]
            attrib_values = response.xpath("//table[@id='product-attribute-specs-table']/tbody/tr/td/text()").extract()[1:]
            if "Color" in attrib_keys:
                index = attrib_keys.index("Color")
                color_name = attrib_values[index]
        available_sizes = self.get_item_sizes(response)
        price = response.xpath("//span[contains(@id, 'product-price-')]/text()").extract_first().strip()
        prev_price = response.xpath("//span[contains(@id, 'old-price-')]/text()").extract_first()
        skus = {}
        if prev_price:
            skus[color_name] = {
                "color": color_name,
                "prev_price": prev_price.strip(),
                "price_now": price,
                "available_sizes": available_sizes,
                "currency_code": "PKR",
            }
        else:
            skus[color_name] = {
                "color": color_name,
                "price_now": price,
                "available_sizes": available_sizes,
                "currency_code": "PKR",
            }
        if not(available_sizes):
            del skus[color_name]["available_sizes"]
        return skus
        