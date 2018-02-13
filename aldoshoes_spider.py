# -*- coding: utf-8 -*-
import scrapy
from aldoshoes.items import AldoshoesItem
import re
from collections import deque


class AldoshoesSpiderSpider(scrapy.Spider):
    name = 'aldoshoes_spider'
    allowed_domains = ['aldoshoes.com']
    main_url = 'https://www.aldoshoes.com'

    def start_requests(self):
        yield scrapy.Request("https://www.aldoshoes.com/uk/en_UK", callback=self.parse)
        yield scrapy.Request("https://www.aldoshoes.com/us/en_US", callback=self.parse)

    def parse(self, response):
        nav_urls = response.xpath("//nav[contains(@class, 'c-navigation--primary')]"
                                  "//a[@class='c-navigation__link']/@href").extract()
        for url in nav_urls:
            request_url = self.main_url+url
            yield scrapy.Request(url=request_url, callback=self.parse_products)

    def parse_products(self, response):
        product_urls = response.xpath("//div[contains(@class, 'c-product-tile')]//@href").extract()

        for url in product_urls:
            request_url = self.main_url + url
            yield scrapy.Request(url=request_url, callback=self.parse_product_details)

    def parse_product_details(self, response):
        product = AldoshoesItem()
        product['category_names'] = self.get_categorynames(response)
        product['brand'] = self.get_brand(response)
        product['currency'] = self.get_currency(response)
        product['url'] = response.url
        product['title'] = self.get_title(response)
        product['language_code'] = self.get_languagecode(response)
        product['base_sku'] = self.get_basesku(response)
        product['identifier'] = self.get_identifier(response)
        product['image_urls'] = self.get_imageurls(response)
        product['description_text'] = self.get_descriptiontext(response)
        product['referer_url'] = response.request.headers['Referer']
        product['color_name'] = self.get_colorname(response)
        product['color_code'] = self.get_colorcode(response)
        product['old_price_text'] = self.get_oldprice(response)
        product['new_price_text'] = self.get_newprice(response)

        availability, size_info = self.get_sizeinfo(response)
        product['size_infos'] = size_info
        product['available'] = availability

        colors = response.xpath("//div[@class='c-product-option']//@href").extract()
        color_urls = []
        for color in colors:
            color_url = self.main_url + color
            color_urls.append(color_url)

        queue = deque(color_urls)
        if queue:
            next_url = queue[0]
            request = scrapy.Request(url=next_url, callback=self.get_skus)
            request.meta['urls'] = queue
            request.meta['product'] = product
            queue.popleft()
            yield request
        else:
            yield product

    def get_skus(self, response):
        product = response.meta['product']
        product['url'] = response.url
        product['identifier'] = self.get_identifier(response)
        product['image_urls'] = self.get_imageurls(response)
        product['color_name'] = self.get_colorname(response)
        product['color_code'] = self.get_colorcode(response)
        product['old_price_text'] = self.get_oldprice(response)
        product['new_price_text'] = self.get_newprice(response)
        availability, size_info = self.get_sizeinfo(response)
        product['size_infos'] = size_info
        product['available'] = availability

        queue = response.meta['urls']
        if queue:
            next_url = queue[0]
            request = scrapy.Request(url=next_url, callback=self.get_skus)
            request.meta['urls'] = queue
            request.meta['product'] = product
            queue.popleft()
            yield request

        yield product

    def get_sizeinfo(self, response):
        size_codes = response.xpath("//select[@id='PdpProductSizeSelectorOptsDropdown']//@value").extract()
        size_codes = size_codes[1:]
        size_names = response.xpath("//select[@id='PdpProductSizeSelectorOptsDropdown']//text()").extract()
        size_names = size_names[1:]

        count_sizes = len(size_codes)
        if count_sizes > 0:
            stock_path = "//text()[contains(.,{})]".format(size_codes[0])
            stock_count = response.xpath(stock_path).re('"stockLevel":(\d+)')
            len_stock_count = len(stock_count)
            count = len_stock_count - count_sizes
            size_info = []
            available = False

            for i in range(len_stock_count - 1, count - 1, -1):
                size = {}
                size['size_identifier'] = size_codes[count_sizes - 1]
                size['size_name'] = size_names[count_sizes - 1]
                size['stock'] = stock_count[i]
                if int(stock_count[i]) > 0:
                    available = True
                size_info.append(size)
                count_sizes -= 1
            return available, size_info
        else:
            return True, "One Size"

    def get_categorynames(self, response):
        return response.xpath("//div[contains(@class,'c-product-detail__info')]//li/a/text()").extract()

    def get_brand(self, response):
        return response.xpath("//title/text()").extract_first().split(sep='|')[1]

    def get_title(self, response):
        return response.xpath("//title/text()").extract_first().split(sep='|')[0]

    def get_languagecode(self, response):
        return response.xpath("//@lang").extract_first()

    def get_basesku(self, response):
        base_sku = re.search('.*p.(\d+)-(\d+)', response.url)
        if base_sku:
            return base_sku.group(1)

    def get_identifier(self, response):
        return re.search('.*p.([\d-]+)', response.url).group(1)

    def get_descriptiontext(self, response):
        return set(response.xpath("//li[contains(@class, 'c-product-description__section-list"
                                                         "-column')]//text()").extract())

    def get_colorname(self, response):
        return response.xpath("//div[@class='c-product-option']//span[@data-qa-selection='true']/text()").extract()

    def get_colorcode(self, response):
        return re.search('.*p.(\d+)-(\d+)', response.url).group(2)

    def get_oldprice(self, response):
        old_price = response.xpath("//span[contains(@class, 'price--original')]/text()").extract_first()
        if not old_price:
            old_price = response.xpath("//span[contains(@class,'c-product-price')]/text()").extract_first()
        return old_price

    def get_newprice(self, response):
        new_price =  response.xpath("//span[contains(@class, 'price--is-reduced')]/text()").extract_first()
        if not new_price:
            new_price = response.xpath("//span[contains(@class,'c-product-price')]/text()").extract_first()
        return new_price

    def get_imageurls(self, response):
        image_urls = response.xpath("//div[@class='c-carousel__product-tile']//picture[contains(@class, 'c-picture')]"
                                    "//@data-srcset").extract()
        return image_urls

    def get_currency(self, response):
        return response.xpath("//meta[contains(@property,'price:currency')]/@content").extract_first()
