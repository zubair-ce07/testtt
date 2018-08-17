# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider

from whistles.items import WhistlesItem


class WhistlesSpider(CrawlSpider):
    """
    Crawl spider to scrap `www.whistles.com`
    """
    name = 'whistles'
    allowed_domains = ['www.whistles.com']
    start_urls = ['http://www.whistles.com/']

    def parse(self, response):
        for href in response.xpath("//li[contains(@class, 'meganav-link')]/a/@href"):
            yield response.follow(href, callback=self.parse)

        next_page_href = response.xpath("//a[contains(@class,'name-link')]/@href")
        next_page_href.extend(response.xpath("//a[contains(@class,'page-next')]/@href"))
        for href in next_page_href:
            yield response.follow(href, callback=self.parse_item)

    def parse_item(self, response):
        item = WhistlesItem()
        item['url'] = response.url
        item['name'] = self.get_name(response)
        item['brand'] = self.get_brand(response)
        item['image_urls'] = self.get_image_urls(response)
        item['product_sku'] = self.get_product_sku(response)
        item['care'] = self.get_care(response)
        item['description'] =  self.get_description(response)
        item['skus'] = self.get_skus(response)
        yield item

    @staticmethod
    def get_name(response):
        return response.xpath("//h1[contains(@class,'product-name')]/text()").extract_first()

    @staticmethod
    def get_brand(response):
        return response.xpath("//meta[contains(@property, 'product:brand')]/@content").extract_first()

    @staticmethod
    def get_image_urls(response):
        return response.xpath("//img[contains(@class, 'productthumbnail')]/@src").extract()

    @staticmethod
    def get_product_sku(response):
        return response.xpath("//p[contains(., 'Product Key:')]/text()").extract_first()

    @staticmethod
    def get_care(response):
        return [
            "material: {}".format(response.xpath("//p[contains(., 'Composition:')]/text()").extract_first()),
            "wash-care: {}".format(response.xpath("//p[contains(., 'Wash care:')]/text()").extract_first())
        ]

    @staticmethod
    def get_color(response):
        return response.xpath("//p[contains(., 'Colour:')]/text()").extract_first()

    @staticmethod
    def get_price(response):
        sale_price = response.xpath("//span[contains(@title, 'Sale Price')]/text()").extract_first(),
        regular_price = response.xpath("//span[contains(@title, 'Regular Price')]/text()").extract_first()
        if isinstance(sale_price, str):
            return {
                'price': sale_price,
                'previous_price': regular_price
            }
        return {
            'price': regular_price
        }

    @staticmethod
    def get_description(response):
        description = response.xpath("(//div[contains(@class,'product-tabs')]/ul/li)")[0]
        return list(filter((lambda x: len(x)), map(str.strip, description.xpath("./div/div/p/text()").extract())))

    @classmethod
    def get_skus(cls, response):
        color = cls.get_color(response)
        price = cls.get_price(response)
        skus = list()
        sizes_info = response.xpath("//li[contains(@class, 'emptyswatch')]")
        if not sizes_info:  # In case on one size only, eg: For `bags`
            sku = {
                'color': color,
                'sku_id': "{}_regular".format(color),
                'size': "regular"
            }
            sku.update(price)
            skus.append(sku)
            return skus
        for size_info in sizes_info:
            size = size_info.xpath("./a/span/text()").extract_first()
            # Status eg: Out Of Stock => out_of_stock
            status = size_info.xpath("./a/@title").extract_first().replace(' ', '_').lower()
            sku = {
                'color': color,
                'size': size,
                status: True,
                'sku_id': "{}_{}".format(color, size)
            }
            sku.update(price)
            skus.append(sku)
        return skus

