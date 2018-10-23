from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from fredperry.items import FredperryItem


class FredperryParse:
    visited_products = set()

    gender_map = {'women': 'women', 'men': 'men', 'kid': 'unisex-kids'}

    def parse(self, response):
        product_id = self.retailer_sku(response)

        if self.id_exists(product_id):
            return

        item = FredperryItem()

        item['retailer_sku'] = product_id
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

        colour = self.colour(response)

        if colour:
            common_sku['colour'] = colour
            common_sku['sku_id'] += f"_{common_sku['colour']}"

        out_stock_sizes = self.out_stock_sizes(response)

        for size in self.sizes(response):
            sku = common_sku.copy()
            sku['size'] = size
            sku['sku_id'] += f"_{size}"

            if size in out_stock_sizes:
                sku['out_of_stock'] = True

            skus += [sku]

        return skus

    def colour_requests(self, response):
        requests = []

        for url in self.colour_urls(response):
            requests.append(response.follow(
                url, callback=self.parse_colours, dont_filter=True))

        return requests

    def colour_urls(self, response):
        css = '.colour-swatches :not(.active) > a::attr(href)'
        return response.css(css).extract()

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
        return [t for t, _ in response.meta['trail']]

    def sizes(self, response):
        css = '#configurable_swatch_size a::attr(name)'
        return response.css(css).extract()

    def out_stock_sizes(self, response):
        path = "//li[contains(@class, 'notify')]/a/@name"
        return response.selector.xpath(path).extract()

    def care(self, response):
        css = '.further-reading li::text'
        return response.css(css).extract()

    def description(self, response):
        return response.css('.std ::text').extract()

    def gender(self, response):
        soup = ' '.join([t for t, _ in response.meta['trail']]).lower()

        for gender_str, gender in self.gender_map.items():
            if gender_str.lower() in soup:
                return gender

        return 'Unisex Adults'

    def id_exists(self, product_id):

        if product_id in self.visited_products:
            return True

        self.visited_products.add(product_id)


class FredperryCrawler(CrawlSpider):
    name = 'fredperry_spider'
    allowed_domains = ['fredperry.com']
    start_urls = ['https://www.fredperry.com']
    fredperry_parse = FredperryParse()

    listing_css = ['.skip-links-left', '.pages']
    product_css = ['.product-name']

    rules = [Rule(LinkExtractor(restrict_css=listing_css), callback='parse'),
             Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')]

    def parse(self, response):
        trail = [(response.css('head title::text').extract_first(), response.url)]
        for req in super().parse(response):
            req.meta['trail'] = trail
            yield req

    def parse_item(self, response):
        return self.fredperry_parse.parse(response)
