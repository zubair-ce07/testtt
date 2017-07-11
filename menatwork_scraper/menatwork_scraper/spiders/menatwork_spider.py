import re
from urllib import parse

import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule

from menatwork_scraper.items import Item


class MenAtWorkSpider(CrawlSpider):
    name = 'menatwork'
    start_urls = ['https://www.menatwork.nl']
    allowed_domains = ['menatwork.nl']
    rules = (
        Rule(LinkExtractor(restrict_css='.headerlist__item')),
        Rule(LinkExtractor(restrict_css='.name-link'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = Item()

        item['retailer_sku'] = self.get_retailer_sku(response)
        if item['retailer_sku'] is None:
            return

        item['brand'] = self.get_brand(response)
        item['category'] = self.get_category(response)
        item['description'] = self.get_description(response)
        item['gender'] = self.get_gender(item['category'])
        item['image_url'] = self.get_image_urls(response)
        item['name'] = self.get_name(response, item['brand'])
        item['retailer'] = self.get_retailer()
        item['url'] = response.url
        item['skus'] = self.get_skus(response)

        color_urls = response.xpath('//ul[contains(@class,"color")]/li[@class="selectable"]/a/@href').extract()
        if color_urls:
            yield scrapy.Request(url=color_urls.pop(), callback=self.parse_colors,
                                 meta={'item': item, 'color_urls': color_urls})

        yield item

    def parse_colors(self, response):
        item = response.meta['item']
        color_urls = response.meta['color_urls']

        item['skus'].update(self.get_skus(response))

        if color_urls:
            yield scrapy.Request(url=color_urls.pop(), callback=self.parse_colors,
                                 meta={'item': item, 'color_urls': color_urls})
        yield item

    def get_skus(self, response):
        skus = {}
        raw_size_variants = response.css('select.variation-select option::text').extract()
        size_variants = self.clean_objects(raw_size_variants)
        color = self.get_color(response)
        currency = self.get_currency()
        price = self.get_price(response)

        for size in size_variants:
            sku_id = "{color}_{size}".format(color=color, size=size)
            skus[sku_id] = {
                "currency": currency,
                "size": size,
                "colour": color,
                "price": price,
            }
        return skus

    def clean_objects(self, objects):
        cleaned_object = []
        for obj in objects:
            obj = obj.strip().replace('\n', '')
            if obj is not '':
                cleaned_object.append(obj)
        return cleaned_object

    def get_description(self, response):
        descriptions = response.css("#tab1 *::text").extract()
        descriptions = self.clean_objects(descriptions)
        descriptions = descriptions[:-1]  # removing last element as it was non-relevant
        return descriptions

    def get_category(self, response):
        return response.css('.breadcrumb a::text').extract()

    def get_image_urls(self, response):
        image_urls = response.css(".product-thumbnails a::attr(href)").extract()
        return image_urls

    def get_brand(self, response):
        return parse.unquote(response.css("div::attr(data-brand)").extract_first())

    def get_name(self, response, brand):
        product_title = response.xpath('//h1[@class="product-name"]/text()').extract_first()
        brand_pattern = re.compile(re.escape(brand), re.IGNORECASE)
        name = brand_pattern.sub('', product_title).strip()
        return name

    def get_color(self, response):
        return response.css('li.selected-value::text').extract_first()

    def get_price(self, response):
        return response.css('span.price-sales::text').extract()[0]

    def get_retailer_sku(self, response):
        return response.css("input#pid::attr(value)").extract()[0]  # remove first

    def get_currency(self):
        return "EURO"

    def get_retailer(self):
        return 'Men At Work'

    def get_gender(self, category):
        if any("Heren" in cate for cate in category):
            return 'Men'
        if any("Dames" in cate for cate in category):
            return 'Women'
        return 'Unisex'
