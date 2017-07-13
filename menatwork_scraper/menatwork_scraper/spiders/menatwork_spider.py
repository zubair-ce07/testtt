import re
from urllib import parse

from scrapy import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from w3lib.url import url_query_cleaner

from menatwork_scraper.items import Item


class MenAtWorkSpider(CrawlSpider):
    name = 'menatwork'
    start_urls = ['https://www.menatwork.nl']
    allowed_domains = ['menatwork.nl']
    rules = (
        Rule(LinkExtractor(restrict_css='.headerlist__item', process_value=url_query_cleaner)),
        Rule(LinkExtractor(restrict_css='.thumb-link', process_value=url_query_cleaner),
             callback='parse_item', ),
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

        color_urls = response.css('.color li:not(.selected) a::attr(href)').extract()
        color_urls = self.append_ajax(color_urls)
        if color_urls:
            yield Request(url=color_urls.pop(), callback=self.parse_colors,
                          meta={'item': item, 'color_urls': color_urls})
        else:
            yield item

    def parse_colors(self, response):
        item = response.meta['item']
        color_urls = response.meta['color_urls']

        item['skus'].update(self.get_skus(response))

        if color_urls:
            yield Request(url=color_urls.pop(), callback=self.parse_colors,
                          meta={'item': item, 'color_urls': color_urls})
        else:
            yield item

    def get_skus(self, response):
        skus = {}
        raw_size_variants = response.css('.variation-select option::text').extract()
        size_variants = self.clean(raw_size_variants)
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

    def get_description(self, response):
        descriptions = response.css("#tab1 *::text").extract()
        cleaned_descriptions = self.clean(descriptions)
        return cleaned_descriptions[:-1]

    def get_category(self, response):
        return response.css('.breadcrumb a::text').extract()

    def get_image_urls(self, response):
        return response.css(".product-thumbnails a::attr(href)").extract()

    def get_brand(self, response):
        return parse.unquote(response.css("div::attr(data-brand)").extract_first())

    def get_name(self, response, brand):
        product_title = response.css('.product-name::text').extract_first()
        brand_pattern = re.compile(re.escape(brand), re.IGNORECASE)
        return brand_pattern.sub('', product_title).strip()

    def get_color(self, response):
        return response.css('.selected-value::text').extract_first()

    def get_price(self, response):
        return response.css('.product-price span::text').extract()[0]

    def get_retailer_sku(self, response):
        return response.css("#pid::attr(value)").extract()[0]

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

    def clean(self, items):
        cleaned_items = []
        for item in items:
            item = item.strip().replace('\n', '')
            if item:
                cleaned_items.append(item)
        return cleaned_items

    def append_ajax(self, urls):
        ajax = '&Quantity=1&format=ajax&productlistid=undefined'
        return [url + ajax for url in urls]
