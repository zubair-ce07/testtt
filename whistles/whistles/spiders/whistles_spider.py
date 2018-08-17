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
        for href in response.css("li[class*='meganav-link'] a::attr(href)"):
            yield response.follow(href, callback=self.parse)

        next_page_href = response.css("a[class*='name-link']::attr(href)")
        next_page_href.extend(response.css("a[class*='page-next']::attr(href)"))
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
        return response.css("h1[class*='product-name']::text").extract_first()

    @staticmethod
    def get_brand(response):
        return response.css("meta[property*='product:brand']::attr(content)").extract_first()

    @staticmethod
    def get_image_urls(response):
        return response.css("img[class*='productthumbnail']::attr(src)").extract()

    @staticmethod
    def get_product_sku(response):
        return response.css("p:contains('Product Key:')::text").extract_first()

    @staticmethod
    def get_care(response):
        return [
            "material: {}".format(response.css("p:contains('Composition:')::text").extract_first()),
            "wash-care: {}".format(response.css("p:contains('Wash care:')::text").extract_first())
        ]

    @staticmethod
    def get_color(response):
        return response.css('p:contains("Colour:")::text').extract_first()

    @staticmethod
    def get_price(response):
        sale_price = response.css("span[title*='Sale Price']::text").extract_first(),
        regular_price = response.css("span[title*='Regular Price']::text").extract_first()
        if isinstance(sale_price, str):
            return {
                'unit': sale_price[0],
                'price': sale_price[1:],
                'previous_price': regular_price[1:]
            }
        return {
            'unit': regular_price[0],
            'price': regular_price[1:]
        }

    @staticmethod
    def get_description(response):
        description = response.css("div[class*='product-tabs'] ul:first-child")
        return list(filter((lambda x: len(x)), map(str.strip, description.css("div div p::text").extract())))

    @classmethod
    def get_skus(cls, response):
        color = cls.get_color(response)
        price = cls.get_price(response)
        skus = list()
        sizes_info = response.css("li[class*='emptyswatch']")
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
            size = size_info.css("a span::text").extract_first()
            # Status eg: Out Of Stock => out_of_stock
            status = size_info.css("a::attr(title)").extract_first().replace(' ', '_').lower()
            sku = {
                'color': color,
                'size': size,
                status: True,
                'sku_id': "{}_{}".format(color.replace(' ', '_'), size)
            }
            sku.update(price)
            skus.append(sku)
        return skus
