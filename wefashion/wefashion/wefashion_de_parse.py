import re

import scrapy

from wefashion.items import WefashionItem


class ProductParser(scrapy.Spider):
    name = 'wefashion-de-parser'
    brand = "WE"

    def parse(self, response):
        item = HunkemollerItem()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['trail'] = self.extract_trails(response)
        item['gender'] = self.gender
        item['category'] = self.extract_category(response)
        item['brand'] = self.brand
        item['url'] = response.url
        item['name'] = self.extract_product_name(response)
        item['description'] = self.extract_product_description(response)
        item['care'] = self.extract_product_care(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['skus'] = self.extract_skus(response)
        item['price'] = self.extract_price(response)
        item['currency'] = self.extract_currency(response)
        return item

    def extract_retailer_sku(self, response):
        return response.css('.pdp-main::attr(data-product-id)').extract_first()

    def extract_gender(self, response):
        return response.css("meta[itemprop='name']::attr(content)").extract_first().split('-')[0]

    def extract_trails(self, response):
        return response.meta.get('trail')

    def extract_product_name(self, response):
        return response.css(".product-details .product-name h2::text").extract_first().strip()

    def extract_product_description(self, response):
        description = response.css("div[itemprop='description']  *::text").extract()
        return description[:description.index('Waschanleitung')]

    def extract_product_care(self, response):
        description = response.css("div[itemprop='description']  *::text").extract()
        return description[description.index('Waschanleitung'):]

    def extract_price(self, response):
        return response.css("meta[itemprop='price']::attr(content)").extract_first()

    def extract_currency(self, response):
        return response.css("meta[itemprop='priceCurrency']::attr(content)").extract_first()

    def extract_color(self, response):
        color_id = self.extract_retailer_sku(response).split('_')[1]
        return response.css(f".color a[data-value='{color_id}']::text").extract_first().strip()
        # color_urls = response.css('.color a::attr(href)').extract()
        # for url in color_urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def extract_category(self, response):
        categories = response.css(".breadcrumb > li *::text").extract()
        return list(filter(lambda category: category.strip(), categories))

    def extract_image_urls(self, response):
        return response.css('.productcarouselslides *::attr(data-image-replacement)').extract()

    def extract_skus(self, response):
        skus = {}
        sku_info = {
            'color': self.extract_color(response),
            'currency': self.extract_currency(response),
            'price': self.extract_price(response)
        }
        for size in response.css('.size li'):
            sku = sku_info.copy()
            sku['size'] = size.css('::attr(title)').extract_first()
            skus[size.css('::attr(data-value)').extract_first()] = sku
        return skus
