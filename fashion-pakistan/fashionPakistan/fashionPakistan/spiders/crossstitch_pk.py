# -*- coding: utf-8 -*-
import scrapy
from fashionPakistan.items import FashionPakistan


class CrossstitchComSpider(scrapy.Spider):
    name = 'crossstitch.pk'
    start_urls = ['https://www.crossstitch.pk']

    def parse(self, response):
        category_links = response.xpath(
            "//ul[@class='top-menu']/li/a/@href").extract()
        for link in category_links:
            yield scrapy.Request(response.urljoin(link)+"?pagenumber=1", self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath(
            "//div[@class='picture ']/a/@href").extract()
        for link in product_links:
            yield scrapy.Request(response.urljoin(link), self.parse_product_details)

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
        product["out_of_stock"] = False
        product["skus"] = self.get_item_skus(response)
        product["url"] = response.url
        yield product

    def get_item_name(self, response):
        return response.xpath("//span[@data-ui-id]/text()").extract_first()

    def get_item_sku(self, response):
        return response.xpath("//div[@itemprop='sku']/text()").extract_first()

    def get_item_description(self, response):
        return response.xpath("//div[@itemprop='description']//text()").extract()

    def get_item_images(self, response):
        images = response.xpath(
            "//div[@class='MagicToolboxSelectorsContainer']//img/@src").extract()
        images.append(response.xpath(
            "//img[@itemprop='image']/@src").extract_first())
        return images

    def get_item_attributes(self, response):
        material = response.xpath(
            "//td[@data-th='Material']/text()").extract_first()
        if material:
            return {
                "Material": material,
            }
        else:
            return {}

    def get_item_sizes(self, response):
        size_string = re.findall(
            r'swatchOptions\":[\W\w]*,\"position\":\"0\"}},|$', response.text)[0]
        size_string = size_string.strip("swatchOptions\":")
        size_string = size_string.strip(",")
        size_string = size_string+"}"
        sizes = []
        if size_string != "}":
            print("find me ", size_string)
            json_string = json.loads(size_string)
            for option in json_string["attributes"]["142"]["options"]:
                sizes.append(option["label"])

        return sizes

    def get_item_skus(self, response):
        color_name = response.xpath(
            "//td[@data-th='Color']/text()").extract_first()
        price = response.xpath("//span[@class='price']/text()").extract_first()
        currency = response.xpath(
            "//meta[@itemprop='priceCurrency']/@content").extract_first()
        sizes = self.get_item_sizes(response)
        if sizes:
            return {
                color_name: {
                    "color": color_name,
                    "price": price,
                    "available_size": sizes,
                    "currency_code": currency,
                }
            }
        else:
            return {
                color_name: {
                    "color": color_name,
                    "price": price,
                    "currency_code": currency,
                }
            }
