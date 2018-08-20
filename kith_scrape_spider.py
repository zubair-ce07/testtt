import unicodedata
import re
import scrapy
from KITH.items import KithItem


class KithSpider(scrapy.Spider):
    name = "kith"
    allowed_domains = ["kith.com"]
    start_urls = ['https://kith.com/']

    def parse(self, response):
        href_list = response.xpath('//ul[contains(@class, "ksplash-mega-list")]/li/a/@href').extract()
        for href in href_list:
            yield scrapy.Request(href, callback=self.parse_page_urls)

    def parse_page_urls(self, response):
        list_urls = []
        list_urls.append(response.url)
        last_page_number = response.xpath('//div[contains(@class,"pagination")]/span[5]/a/text()').extract_first()
        if last_page_number:
            last_page_number = int(last_page_number)
            for index in range(2, last_page_number):
                if response.url.endswith('/'):
                    list_urls.append(response.url[:-1] + "?page=" + str(index))
                else:
                    list_urls.append(response.url + "?page=" + str(index))
        for url in list_urls:
            yield scrapy.Request(url, callback=self.parse_products)

    def parse_products(self, response):
        for href in response.xpath('//a[contains(@class,"product-card-info")]/@href'):
            url = "https://kith.com{}".format(href.extract())
            yield scrapy.Request(url, callback=self.parse_product_item)

    def parse_product_item(self, response):
        item = KithItem()
        item['product_ID'], item['material'], item['description'] = self.parse_description(response)
        item['name'] = self.parse_name(response)
        item['color'] = self.parse_color(response)
        item['price'] = self.parse_price(response)
        item['img_urls'] = self.parse_img_urls(response)
        item['currency'] = self.parse_currency(response)
        item['sizes'] = self.parse_sizes(response)
        item['url'] = self.parse_url(response)

        yield item

    def parse_name(self, response):
        return response.xpath('//h1[contains(@class,"product-header-title")]/text()').extract_first().strip()

    def parse_color(self, response):
        return response.xpath('//span[contains(@class, "product-header-title -variant")]/text()').extract_first().strip()

    def parse_price(self, response):
        return response.xpath('//span[@id="ProductPrice"]/text()').extract_first().strip()

    def parse_img_urls(self, response):
        return response.xpath('//img[contains(@class, "js-super-slider-photo-img super-slider-photo-img")]/@src').extract()

    def parse_currency(self, response):
        price = response.xpath('//span[@id="ProductPrice"]/text()').extract_first().strip()
        return price[:1]

    def parse_sizes(self, response):
        return response.xpath('//div[contains(@class,"product-single-form-item -dropdown -full")]'
                              '/select/option/text()').extract()

    def parse_url(self, response):
        return response.url

    def cleanse_description(self, response):
        description_list = response.xpath('//div[contains(@class, "product-single-details-rte rte mb0")]/p/text()').extract()
        description_list = filter(lambda name: name.strip(), description_list)
        description_list = filter(None, description_list)
        return description_list

    def parse_description(self, response):
        information_list = self.cleanse_description(response)
        description_list = []
        product_id = ''
        material = ''
        if information_list:
            for description in information_list:
                sub_string_style = re.search(r'^Style: (.+?)$', description)
                sub_string_color = re.search(r'^Color: (.+?)$', description)
                sub_string_material = re.search(r'^Material: (.+?)$', description)
                if sub_string_style:
                    product_id = sub_string_style.group(1)
                elif sub_string_color:
                    pass
                elif sub_string_material:
                    material = sub_string_material.group(1)
                else:
                    description_list.append(description)
        if description_list:
            description = description_list
        else:
            description = response.xpath('//div[contains(@class, '
                                         '"product-single-details-rte rte mb0")]/ul/li/text()').extract()
        return product_id, material, description
