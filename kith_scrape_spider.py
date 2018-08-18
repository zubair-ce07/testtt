import re
import scrapy
from KITH.items import KithItem


class KithSpider(scrapy.Spider):
    name = "kith"
    allowed_domains = ["kith.com"]
    start_urls = ['https://kith.com/']
    description_list = []

    def parse(self, response):
        href_list = response.xpath('//ul[contains(@class, "ksplash-mega-list")]/li/a/@href').extract()
        for href in href_list:
            yield scrapy.Request(href, callback=self.parse_products)

    def parse_products(self, response):
        for href in response.xpath('//a[contains(@class,"product-card-info")]/@href'):
            url = "https://kith.com" + href.extract()
            yield scrapy.Request(url, callback=self.parse_dir_contents)

        next_page_url = response.xpath('//span[contains(@class,"next")]/a/@href').extract_first()
        if next_page_url:
            next_page_url = next_page_url[:-1]
            last_page_number = int(response.xpath('//div[contains(@class,"pagination")]/span[5]/a/text()').extract_first())
            for pages in range(2, last_page_number):
                next_pages = next_page_url + str(pages)
                yield scrapy.Request(url=next_pages, callback=self.parse)

    def parse_dir_contents(self, response):
        item = KithItem()
        item['product_ID'] = self.parse_product_id(response)
        item['material'] = self.parse_material()
        item['name'] = self.parse_name(response)
        item['color'] = self.parse_color(response)
        item['price'] = self.parse_price(response)
        item['img_urls'] = self.parse_img_urls(response)
        item['currency'] = self.parse_currency(response)
        item['sizes'] = self.parse_sizes(response)
        item['url'] = self.parse_url(response)
        item['description'] = self.parse_description(response)

        yield item

    def parse_name(self, response):
        return response.xpath('//h1[contains(@class,"product-header-title")]/text()').extract_first().strip()

    def parse_color(self, response):
        return response.xpath('//span[contains(@class, "product-header-title -variant")]/text()').extract_first()\
            .strip()

    def parse_price(self, response):
        return response.xpath('//span[@id="ProductPrice"]/text()').extract_first().strip()

    def parse_img_urls(self, response):
        return response.xpath('//img[contains(@class, "js-super-slider-photo-img super-slider-photo-img")]/@src')\
            .extract()

    def parse_currency(self, response):
        price = response.xpath('//span[@id="ProductPrice"]/text()').extract_first().strip()
        return price[:1]

    def parse_sizes(self, response):
        return response.xpath('//div[contains(@class,"product-single-form-item -dropdown -full")]'
                              '/select/option/text()').extract()

    def parse_url(self, response):
        return response.url

    def parse_description(self, response):
        for index in self.description_list:
            if index != u'\xa0':
                sub_string_color = re.search('Color: (.+?)$', index)
                if sub_string_color:
                    self.description_list.remove(index)
        return self.description_list + response.xpath('//div[contains(@class, '
                                                      '"product-single-details-rte rte mb0")]/ul/li/text()').extract()

    def parse_product_id(self, response):
        self.description_list = response.xpath('//div[contains(@class, '
                                               '"product-single-details-rte rte mb0")]/p/text()').extract()
        self.description_list = filter(lambda name: name.strip(), self.description_list)
        self.description_list = filter(None, self.description_list)
        for index in self.description_list:
            if index != u'\xa0':
                sub_string_style = re.search('Style: (.+?)$', index)
                if sub_string_style:
                    self.description_list.remove(index)
                    return sub_string_style.group(1)
        
    def parse_material(self):
        for index in self.description_list:
            if index != u'\xa0' or index != '':
                sub_string_material = re.search('Material: (.+?)$', index)
                if sub_string_material:
                    self.description_list.remove(index)
                    return sub_string_material.group(1)





