# -*- coding: utf-8 -*-
import scrapy
from fashionPakistan.items import FashionPakistan


class SapphirePkSpider(scrapy.Spider):
    name = 'sapphire.pk'
    start_urls = ['https://pk.sapphireonline.pk']

    def parse(self, response):
        category_links = response.xpath("//ul[@id='_menuBar']//ul/li/a/@href").extract()
        for link in category_links:
            yield scrapy.Request(response.urljoin(link)+"?view=all", callback=self.parse_product_links)

    def parse_product_links(self, response):
        product_links = response.xpath(
            "//a[@class='product-grid-image']/@href").extract()
        for link in product_links:
            yield scrapy.Request(response.urljoin(link), self.parse_product_details)
        
        next_link = response.xpath("//ul[@class='pagination-page abs']/li/a/i[@class='fa fa-angle-right']").extract()
        if next_link:
            next_link = response.xpath("//ul[@class='pagination-page abs']/li/a/@href").extract()[-1]
            yield scrapy.Request(next_link, self.parse_product_links)


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
        value = response.xpath("//link[@itemprop='availability']/@href").extract_first().split("/")[-1]
        return value

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
        attribute = response.xpath("//div[@id='collapse-tab2']//h4/text()").extract()
        attributes = {}
        for i, attrib in enumerate(attribute):
            desc = response.xpath("//div[@id='collapse-tab2']//ul[{}]//text()".format(i+1)).extract()
            attributes[attrib] = desc
        
        return attributes

    def get_item_sizes(self, response):
        size_string = re.findall(r'swatchOptions\":[\W\w]*,\"position\":\"0\"}},|$',response.text)[0]
        size_string = size_string.strip("swatchOptions\":")
        size_string = size_string.strip(",")
        size_string = size_string+"}"
        sizes = []
        if size_string != "}":
            json_string = json.loads(size_string)
            for option in json_string["attributes"]["142"]["options"]:
                sizes.append(option["label"])
        
        return sizes

    def get_item_types(self, response):
        pass

    def get_item_skus(self, response):
        color_name = response.xpath("//div[@class='short-description']/p/text()").extract()
        price = response.xpath("//span[@itemprop='price']//text()").extract_first()
        currency = response.xpath(
            "//meta[@itemprop='priceCurrency']/@content").extract_first()
        if color_name[-1].strip().split(":")[0] == "Color":
            color_name = color_name[-1].strip().split(":")[1]
        elif color_name[-2].strip().split(":")[0] == "Color":
            color_name = color_name[-2].strip().split(":")[1]
        else:
            color_name = response.xpath("//div[contains(@class, 'swatch-element')]/div[@class='tooltip']/text()").extract_first()
        if not(color_name):
            color_name = "no_color"
        product_types = self.get_item_types(response)
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
