from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from fredperry.items import FredperryItem


class FredperryParse:
    gender_map = {'women': 'women', 'men': 'men', 'kid': 'unisex-kids'}
    category_map = {'women': 'women', 'men': 'men', 'kid': 'kids'}

    def parse(self, response):
        item = FredperryItem()

        item['retailer_sku'] = self.retailer_sku(response)
        item['brand'] = self.brand(response)
        item['name'] = self.name(response)
        item['trail'] = response.meta['trail']
        item['category'] = self.category(response)
        item['care'] = self.care(response)
        item['gender'] = self.gender(response)
        item['description'] = self.description(response)
        item['image_urls'] = self.image_urls(response)
        item['url'] = response.url
        item['skus'] = self.skus(response)

        item['meta'] = {'requests': self.colour_requests(response)}

        return self.request_or_item(item)

    def parse_colours(self, response):
        item = response.meta['item']
        item['skus'] += self.skus(response)
        item['image_urls'] += self.image_urls(response)

        return self.request_or_item(item)

    def request_or_item(self, item):

        if not item.get('meta'):
            return item

        if item['meta'].get('requests'):
            next_request = item['meta']['requests'].pop()
            next_request.meta['item'] = item
            return next_request

        del item['meta']
        return item

    def skus(self, response):
        skus = []
        common_sku = {'price': self.price(response),
                      'sku_id': self.retailer_sku(response),
                      'currency': self.currency(response)}

        if self.colour(response):
            common_sku['colour'] = self.colour(response)
            common_sku['sku_id'] += '_' + common_sku['colour']

        for size in self.in_stock_sizes(response):
            sku = common_sku.copy()
            sku['size'] = size
            sku['sku_id'] += '_' + size

            skus += [sku]

        for size in self.out_stock_sizes(response):
            sku = common_sku.copy()
            sku['size'] = size
            sku['out_of_stock'] = True
            sku['sku_id'] += '_' + size

            skus += [sku]

        return skus

    def colour_requests(self, response):
        requests = []

        for url in self.colour_urls(response):
            requests.append(response.follow(
                url=url, callback=self.parse_colours, dont_filter=True))

        return requests

    def colour_urls(self, response):
        css = '.colour-swatches a::attr(href)'
        return response.css(css).extract()[1:]

    def brand(self, response):
        css = 'head title::text'
        raw_brand = response.css(css).extract_first()

        if 'Fred Perry' in raw_brand:
            return 'Fred Perry'

    def image_urls(self, response):
        css = '.product-image-gallery img::attr(src)'
        return response.css(css).extract()

    def colour(self, response):
        css = '.label .colour-description ::text'
        raw_colour = response.css(css).extract()

        return ''.join(raw_colour).replace(' ', '')

    def retailer_sku(self, response):
        css = '.product-sku p::text'
        return response.css(css).extract_first()

    def currency(self, response):
        css = '.price::text'
        raw_currency = response.css(css).extract_first()

        if '£' in raw_currency:
            return 'GBP'

    def price(self, response):
        css = '.price::text'
        raw_currency = response.css(css).extract_first()
        return int(raw_currency.strip()[1:])

    def name(self, response):
        css = '.product-name h1 ::text'
        return response.css(css).extract_first()

    def category(self, response):
        soup = ' '.join([trail[0] for trail in response.meta['trail']]).lower()

        for category_str, category in self.category_map.items():
            if category_str.lower() in soup:
                return [category]

    def in_stock_sizes(self, response):
        path = "//li[contains(@class, 'option') and \
        not(contains(@class, 'notify'))]/a/@name"
        return response.selector.xpath(path).extract()

    def out_stock_sizes(self, response):
        path = "//li[contains(@class, 'notify')]/a/@name"
        return response.selector.xpath(path).extract()

    def care(self, response):
        css = '.further-reading li::text'
        return response.css(css).extract()

    def description(self, response):
        css = '.std ::text'
        return response.css(css).extract()

    def gender(self, response):
        soup = ' '.join([trail[0] for trail in response.meta['trail']]).lower()

        for gender_str, gender in self.gender_map.items():
            if gender_str.lower() in soup:
                return gender

        return 'unisex'


class FredperryCrawler(CrawlSpider):
    name = 'fredperry_spider'
    allowed_domains = ['fredperry.com']
    start_urls = ['https://www.fredperry.com']
    fredperry_parse = FredperryParse()

    listing_css = ['.skip-links-left', '.pages']
    product_css = ['.product-name']

    rules = [Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')]

    visited_products = set()

    def parse(self, response):
        trail = [(response.css('head title::text').extract_first(), response.url)]
        for req in super().parse(response):
            req.meta['trail'] = trail
            yield req

    def parse_item(self, response):
        retailer_sku = self.fredperry_parse.retailer_sku(response)

        if retailer_sku in self.visited_products:
            return

        self.visited_products.add(retailer_sku)

        return self.fredperry_parse.parse(response)
