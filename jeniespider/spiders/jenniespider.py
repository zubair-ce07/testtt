import scrapy
from jeniespider.items import JeniespiderItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from copy import deepcopy
from scrapy import Request


class JanieSpider(CrawlSpider):
    skus = []
    name = "janiespider"
    allowed_domains = ["janieandjack.com"]
    start_urls = (
        'http://www.janieandjack.com/',
    )
    rules = (
        Rule(LinkExtractor(
            restrict_css='.desktop-only .subcategory')),
        Rule(LinkExtractor(restrict_css='.product-image .thumb-link'),
             callback='parse_product'),

    )

    def parse_product(self, response):
        product = JeniespiderItem()
        product['url'] = response.url
        product['title'] = self.title(response)
        product['market'] = 'US'
        product['brand'] = 'Janie And Jack'
        product['retailer'] = 'janieandjack-us'
        product['description'] = self.description(response)
        product['image_urls'] = self.image_urls(response)
        product['category'] = self.category(response)
        product['skus'] = list()
        response.meta['product'] = product
        yield from self.skus_parse(response)

    @staticmethod
    def title(response):
        title = response.css('h1.product-name::text').extract_first() or ''
        return title.strip()

    @staticmethod
    def description(response):
        xpath = "//div[contains(@class, 'longDescription')]//ul//li/text()"
        description = response.xpath(xpath).extract()
        return description

    @staticmethod
    def image_urls(response):
        xpath = "//div[@class='amp-zoomed-container']//img/@src"
        url = response.xpath(xpath).extract()
        return url

    @staticmethod
    def category(response):
        xpath = "//span//a//span[contains(@itemprop, 'name')]/text()"
        category = response.xpath(xpath).extract()
        return category[len(category) - 1]

    def skus_parse(self, response):
        xpath = "//a[@class='swatchanchor ']/@href"
        sizes = response.xpath(xpath).extract()
        meta = deepcopy(response.meta)
        meta['size_url'] = sizes
        url = meta['size_url'].pop()
        yield Request(url,
                      meta=meta,
                      callback=self.parse_sizes)

    def parse_sizes(self, response):
        product = response.meta['product']
        item = dict()
        item['price'] = self.price(response)
        item['currency'] = 'USD'
        item['previous_prices'] = self.previous_prices(response)
        colour = self.colour(response)
        size = self.size(response)
        item['colour'] = colour
        item['size'] = size
        item['sku_id'] = str(colour) + "_" + str(size)
        product['skus'].append(item)
        meta = deepcopy(response.meta)
        if meta['size_url']:
            url = meta['size_url'].pop()
            yield Request(url,
                          meta=meta,
                          callback=self.parse_sizes)
        else:
            yield product

    @staticmethod
    def price(response):
        xpath = "//span[@class='price-sales']/text()"
        price = response.xpath(xpath).extract_first()
        return price

    @staticmethod
    def colour(response):
        xpath = "//span[contains(@class, 'selected-value') " \
                "and contains(@class, 'color')]/text()"
        colour = response.xpath(xpath).extract_first().replace('\n', '')
        return colour

    @staticmethod
    def size(response):
        xpath = "//li[contains(@class, 'selectable') " \
                "and contains(@class, 'selected')]" \
                "//a[@class='swatchanchor ']/text()"
        size = response.xpath(xpath).extract()
        return "".join(e for e in size[len(size) - 1] if e.isalnum())

    @staticmethod
    def previous_prices(response):
        xpath = "//span[@class='price-standard']/text()"
        previous_prices = response.xpath(xpath).extract()
        return previous_prices
