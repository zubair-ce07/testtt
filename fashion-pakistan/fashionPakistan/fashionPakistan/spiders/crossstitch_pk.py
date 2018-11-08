# -*- coding: utf-8 -*-
import json
import scrapy
from fashionPakistan.items import FashionPakistan


class CrossstitchComSpider(scrapy.Spider):
    name = 'crossstitch.pk'
    my_public_ip = "116.58.62.58"       #used to set local currency
    start_urls = ['https://www.crossstitch.pk/Common/SetCurrencyByIp?ip='+my_public_ip]

    def parse(self, response):
        yield scrapy.Request("https://www.crossstitch.pk", self.crawl_crossstitch)
        

    def crawl_crossstitch(self, response):
        category_links = response.xpath(
            "//ul[@class='top-menu']/li/a/@href").extract()
        for link in category_links:
            yield scrapy.Request(response.urljoin(link)+"?pagenumber=1", self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath(
            "//div[@class='picture ']/a/@href").extract()
        for link in product_links:
            yield scrapy.Request(response.urljoin(link), self.parse_product_details, dont_filter=True)

        if product_links:
            pagenumber = int(response.url[response.url.find("=")+1:])
            pagenumber = pagenumber + 1
            yield scrapy.Request(response.urljoin("?pagenumber="+str(pagenumber)), self.parse_product_links)

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
        id = response.xpath("//div[@data-productid]/@data-productid").extract_first()
        value = response.xpath("//input[@id='add-to-cart-button-{}']/@value".format(id))
        if value == "Out of Stock":
            return True
        else:
            return False

    def get_item_name(self, response):
        return response.xpath("//h1[@itemprop='name']/text()").extract_first().strip()

    def get_item_sku(self, response):
        return response.xpath("//span[@itemprop='sku']/text()").extract_first()

    def get_item_description(self, response):
        return response.xpath("//div[@itemprop='description']/p/text()").extract()

    def get_item_images(self, response):
        images = response.xpath("//div[@class='owl-carousel']//img/@src").extract()
        return images

    def get_item_attributes(self, response):
        attribute = response.xpath("//ul[@id='tabs']//a/text()").extract()
        attributes = {}
        for attrib in attribute:
            attributes[attrib] = [desc.strip() for desc in response.xpath("//div[@id='{}']/p/text()".format(attrib)).extract()]
        return attributes

    def get_item_sizes(self, response):
        sizes = response.xpath("//select[contains(@id, 'product_attribute_')]/option/text()").extract()
        return sizes

    def get_item_skus(self, response):
        id = int(response.xpath("//div[@data-productid]/@data-productid").extract_first())
        available_sizes = self.get_item_sizes(response)
        prev_price = response.xpath("//div[@class='old-product-price']/span/text()").extract_first()
        currency_code = response.xpath("//meta[@itemprop='priceCurrency']/@content").extract_first()
        color_scheme = {}
        if prev_price:
            color_scheme={
                "prev_price": prev_price,
                "new_price" : response.xpath("//span[@id='spanprice']/text()").extract_first().strip(),
                "available_sizes": available_sizes,
                "currency_code": currency_code,
            }
        else:
            color_scheme={
                "price" : response.xpath("//span[@id='spanprice']/text()").extract_first().strip(),
                "available_sizes": available_sizes,
                "currency_code": currency_code,
            }
        return color_scheme