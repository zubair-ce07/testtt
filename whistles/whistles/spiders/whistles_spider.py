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
        items_pages = response.css("li[class*='meganav-link'] a::attr(href), a[class*='page-next']::attr(href)")
        for listing_url in items_pages:
            yield response.follow(listing_url, callback=self.parse)

        for product_url in response.css("a[class*='name-link']::attr(href)"):
            yield response.follow(product_url, callback=self.parse_item)

    def parse_item(self, response):
        item = WhistlesItem()
        item['url'] = response.url
        item['name'] = self.extract_name(response)
        item['brand'] = self.extract_brand(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['product_sku'] = self.extract_product_sku(response)
        item['care'] = self.extract_care(response)
        item['description'] = self.extract_description(response)
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
            response.css("p:contains('Composition:')::text").extract_first(),
            response.css("p:contains('Wash care:')::text").extract_first()
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
            previous_price = None
        price_dict = {
            'currency': regular_price[0],
            'price': regular_price[1:],
        }
        if previous_price:
            price_dict['previous_prices'] = [previous_price]
        return price_dict

    @staticmethod
    def extract_description(response):
        description = response.css("div[class*='product-tabs'] ul:first-child")
        return list(filter((lambda x: len(x)), map(str.strip, description.css("div div p::text").extract())))

    def extract_skus(self, response):
        color = self.extract_color(response)
        price = self.extract_price(response)
        skus = list()
        sizes_info = response.css("li[class*='emptyswatch']")
        if not sizes_info:
            sku = {
                'color': color,
                'sku_id': "{}_one_size".format(color),
                'size': "One Size"
            }
            sku.update(price)
            skus.append(sku)
            return skus
        for size_info in sizes_info:
            size = size_info.css("a span::text").extract_first()
            status = size_info.css("a::attr(title)").extract_first().replace(' ', '_').lower()
            sku = {
                'color': color,
                'size': size,
                'sku_id': "{}_{}".format(color.replace(' ', '_'), size)
            }
            if status == 'out_of_stock':
                sku[status] = True,
            sku.update(price)
            skus.append(sku)
        return skus
