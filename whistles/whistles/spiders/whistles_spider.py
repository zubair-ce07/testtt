# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider

from whistles.items import WhistlesItem


class WhistlesSpider(CrawlSpider):
    """
    Crawl spider to scrap `www.whistles.com`
    """
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
    }
    name = 'whistles'
    allowed_domains = ['www.whistles.com']
    start_urls = ['http://www.whistles.com/']

    def parse(self, response):
        items_pages = response.css("li[class*='meganav-link'] a::attr(href)")
        items_pages.extend(response.css("a[class*='page-next']::attr(href)"))
        for href in items_pages:
            yield response.follow(href, callback=self.parse)

        for href in response.css("a[class*='name-link']::attr(href)"):
            yield response.follow(href, callback=self.parse_item)

    def parse_item(self, response):
        item = WhistlesItem()
        item['url'] = response.url
        item['name'] = self.extract_name(response)
        item['brand'] = self.extract_brand(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['product_sku'] = self.extract_product_sku(response)
        item['care'] = self.extract_care(response)
        item['description'] =  self.extract_description(response)
        item['skus'] = self.extract_skus(response)
        yield item

    @staticmethod
    def extract_name(response):
        return response.css("h1[class*='product-name']::text").extract_first()

    @staticmethod
    def extract_brand(response):
        return response.css("meta[property*='product:brand']::attr(content)").extract_first()

    @staticmethod
    def extract_image_urls(response):
        return response.css("img[class*='productthumbnail']::attr(src)").extract()

    @staticmethod
    def extract_product_sku(response):
        return response.css("p:contains('Product Key:')::text").extract_first()

    @staticmethod
    def extract_care(response):
        return [
            "material: {}".format(response.css("p:contains('Composition:')::text").extract_first()),
            "wash-care: {}".format(response.css("p:contains('Wash care:')::text").extract_first())
        ]

    @staticmethod
    def extract_color(response):
        return response.css('p:contains("Colour:")::text').extract_first()

    @staticmethod
    def extract_price(response):
        regular_price = response.css("span[title*='Sale Price']::text").extract_first()
        previous_price = response.css("span[title*='Regular Price']::text").extract_first()
        if not regular_price:
            regular_price = previous_price
            previous_price = []
        return {
            'currency': regular_price[0],
            'price': regular_price[1:],
            'previous_prices': [previous_price[1:]]
        }

    @staticmethod
    def extract_description(response):
        description = response.css("div[class*='product-tabs'] ul:first-child")
        return list(filter((lambda x: len(x)), map(str.strip, description.css("div div p::text").extract())))

    def extract_skus(self, response):
        color = self.extract_color(response)
        price = self.extract_price(response)
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
