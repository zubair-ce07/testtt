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
            yield scrapy.Request(href, callback=self.parse_products)

    def parse_products(self, response):
        for href in response.xpath('//a[contains(@class,"product-card-info")]/@href'):
            url = "https://kith.com{}".format(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

        next_page_url = response.xpath('//span[contains(@class,"next")]/a/@href').extract_first()
        if next_page_url:
            next_page_url = next_page_url[:-1]
            last_page_number = int(response.xpath('//div[contains(@class,"pagination")]/span[5]/a/text()').extract_first())
            for page_num in range(2, last_page_number):
                next_page = next_page_url + str(page_num)
                yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_dir_contents(self, response):
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
        description_list = self.cleanse_description(response)
        for description in description_list:
            if description != u'\xa0':
                sub_string_style = re.search('Style: (.+?)$', description)
                if sub_string_style:
                    description_list.remove(description)
                    product_id = sub_string_style.group(1)

        for description in description_list:
            if description != u'\xa0' or description != '':
                sub_string_material = re.search('Material: (.+?)$', description)
                if sub_string_material:
                    description_list.remove(description)
                    material = sub_string_material.group(1)

        for description in description_list:
            if description != u'\xa0':
                sub_string_color = re.search('Color: (.+?)$', description)
                if sub_string_color:
                    description_list.remove(description)
        description = description_list + response.xpath('//div[contains(@class, '
                                                        '"product-single-details-rte rte mb0")]/ul/li/text()').extract()
        return product_id, material, description
