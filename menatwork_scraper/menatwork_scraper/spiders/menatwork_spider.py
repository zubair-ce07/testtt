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
        Rule(LinkExtractor(restrict_css='link[rel="next"]',)),
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
        color_urls = self.append_ajax_query(color_urls)

        yield self.yield_or_pasrse_more_colors(item, color_urls)

    def yield_or_pasrse_more_colors(self, item, color_urls):
        if color_urls:
            return Request(url=color_urls.pop(), callback=self.parse_colors,
                           meta={'item': item, 'color_urls': color_urls})
        else:
            return item

    def parse_colors(self, response):
        item = response.meta['item']
        color_urls = response.meta['color_urls']

        item['skus'].update(self.get_skus(response))

        yield self.yield_or_pasrse_more_colors(item, color_urls)

    def get_skus(self, response):
        color = self.get_color(response)
        currency = self.get_currency()
        price = self.get_price(response)

        avail_variants_css = '.variation-select option:not([disabled])::text'
        raw_avail_size_variants = response.css(avail_variants_css).extract()
        avail_size_variants = self.clean(raw_avail_size_variants)

        non_avail_variants_css = '.variation-select option[disabled]::text'
        raw_non_avail_size_variants = response.css(non_avail_variants_css).extract()
        non_avail_size_variants = self.clean(raw_non_avail_size_variants)

        skus = self.initialize_skus(avail_size_variants, color,
                                    currency, price, availability=True)

        non_avail_skus = self.initialize_skus(non_avail_size_variants, color,
                                              currency, price, availability=False)
        skus.update(non_avail_skus)

        return skus

    def initialize_skus(self, size_variants, color, currency, price, availability):
        skus = {}
        for size in size_variants:
            sku_id = "{color}_{size}".format(color=color, size=size)
            skus[sku_id] = {
                "availability": availability,
                "currency": currency,
                "size": size,
                "colour": color,
                "price": price,
            }
        return skus

    def get_description(self, response):
        descriptions = response.css("#tab1 *::text").extract()
        cleaned_description = self.clean(descriptions)[:-1]
        if len(cleaned_description[-1]) < 2:
            cleaned_description.pop()
        return cleaned_description

    def get_category(self, response):
        return response.css('.breadcrumb a::text').extract()

    def get_image_urls(self, response):
        return response.css(".product-thumbnails a::attr(href)").extract()

    def get_brand(self, response):
        return parse.unquote(response.css("div::attr(data-brand)").extract_first())

    def get_name(self, response, brand):
        product_title = response.css('.product-name::text').extract_first()
        brand_pattern = re.compile(re.escape(brand), re.IGNORECASE)
        name = brand_pattern.sub('', product_title)
        return name.strip() if name else None

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

    def append_ajax_query(self, urls):
        ajax = '&Quantity=1&format=ajax&productlistid=undefined'
        return [url + ajax for url in urls]
