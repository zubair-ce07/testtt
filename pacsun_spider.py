from scrapy.http import Request
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseCrawlSpider, BaseParseSpider, clean


class Mixin:
    retailer = "pacsun"
    market = "US"
    allowed_domains = ["pacsun.com"]
    start_urls = ["http://www.pacsun.com/"]


class PacsunParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"
    price_css = '.product-price ::text'

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['image_urls'] = self.image_urls(response)
        garment['gender'] = self.product_gender(garment)
        garment['merch_info'] = self.merch_info(response)
        garment['skus'] = {}
        garment['meta'] = {
            'requests_queue': self.colour_requests(response) +
                              self.size_requests(response)
        }
        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['meta']['requests_queue'] += self.size_requests(response)
        garment['image_urls'] += self.image_urls(response)
        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def skus(self, response):
        sku = self.product_pricing_common_new(response)
        size = response.css('#va-sizeCode a.selected::text').extract_first()
        colour = clean(response.css('.swatch-value::text').extract_first() or \
                 response.css('.colorcode a.selected::text').extract_first())
        if size and "1SZ" in size:
            size = self.one_size
        sku_id = f'{colour}_ {size}'.replace(' ', '')
        sku['colour'] = colour
        sku['size'] = size
        if self.is_out_of_stock(response):
            sku['out_of_stock'] = True
        return {sku_id: sku}

    def colour_requests(self, response):
        colour_urls = response.css('.colorcode a:not(.selected)::attr(href)').extract()
        return [Request(url=url, callback=self.parse_colour) for url in colour_urls]

    def size_requests(self, response):
        size_urls = response.css('#va-sizeCode ::attr(href)').extract()
        return [Request(url=url, callback=self.parse_size) for url in size_urls]

    def product_id(self, response):
        return response.css('#masterid ::attr(data-id)').extract_first()

    def product_name(self, response):
        return clean(response.css('.product-name::text'))[0]

    def product_description(self, response):
        return clean(response.xpath('//*[contains(@class,"pdp-desc-container")]/p[1]/text()'))

    def product_brand(self, response):
        return response.css('.brand ::text').extract_first(default="Pacsun")

    def is_out_of_stock(self, response):
        return not bool(response.xpath('//*[contains(@class,"in-stock-msg") and contains(text(), "In Stock")]'))

    def product_care(self, response):
        xpath = '//*[contains(text(),"CARE")]/../following-sibling::ul[1]/li/text()'
        return clean(response.xpath(xpath))

    def image_urls(self, response):
        return clean(response.css('.productthumbnail ::attr(src)'))

    def product_category(self, response):
        return clean(response.css('.breadcrumb-element ::text'))

    def product_gender(self, garment):
        soup = ' '.join([garment['name']] + garment['category'])
        return self.gender_lookup(soup)

    def merch_info(self, response):
        return clean(response.xpath('//*[contains(@class,"callout-message")][2]/text()'))


class PacsunCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = PacsunParseSpider()

    listings_css = [
        '.menu-category',
        '.infinite-scroll-placeholder',
    ]

    listings_tags = [
        'a', 'area', 'div'
    ]

    listings_attrs = [
        'href', 'data-grid-url'
    ]

    products_css = ['.product-image']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, tags=listings_tags, attrs=listings_attrs), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
    )

