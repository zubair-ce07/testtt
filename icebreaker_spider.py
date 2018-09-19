import json

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class IceBreakerMixin:
    retailer = 'ice-breaker'

    allowed_domains = ['uk.icebreaker.com']
    start_urls = [
        'https://uk.icebreaker.com/en/home',
    ]

    default_brand = "ICEBREAKER"
    market = "UK"


class CommonParseSpider(BaseParseSpider):
    price_css = '.product-price ::text'
    details_css = '.product-box::attr(data-selectedproduct)'

    def parse(self, response):
        raw_product = self.raw_product(response)
        pid = raw_product['id']

        garment = self.new_unique_garment(pid)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment["gender"] = self.product_gender(raw_product, response)
        garment["skus"] = {}
        garment['image_urls'] = self.product_images(response)
        garment['meta'] = {'requests_queue': self.color_requests(response)}

        return self.next_request_or_garment(garment)

    def color_requests(self, response):
        color_urls = clean(response.css('ul.color a::attr(href)'))
        return [Request(f"{url}&format=ajax", callback=self.parse_colors) for url in color_urls]

    def parse_colors(self, response):
        garment = response.meta["garment"]
        garment['image_urls'] += self.product_images(response)
        size = clean(response.css('.size .selected a::attr(title)'))

        if size:
            garment["skus"].update(self.skus(response))

        else:
            garment['meta']['requests_queue'] += self.size_requests(response)

        return self.next_request_or_garment(garment)

    def size_requests(self, response):
        css = 'ul.size a.swatchanchor ::attr(href)'
        sizes = response.css(css).extract()
        return [Request(url=f"{size_url}&format=ajax", callback=self.parse_sizes) for size_url in sizes]

    def parse_sizes(self, response):
        garment = response.meta["garment"]
        garment["skus"].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def skus(self, response):
        sku = self.product_pricing_common(response)
        sku['colour'] = clean(response.css('.color .selected a::attr(title)'))[0]
        size = clean(response.css('.size .selected a::attr(title)'))
        sku['size'] = size[0] if size else self.one_size
        availability_xpath = '//*[@class="availability-msg"]/*[contains(.,"out of stock")]/text()'
        is_sold_out = clean(response.xpath(availability_xpath))

        if is_sold_out:
            sku['out_of_stock'] = True

        return {f'{sku["colour"]}_{sku["size"]}': sku}

    def product_images(self, response):
        css = '[class="thumbnail-tile"]::attr(href),.primary-image::attr(src)'
        return clean(response.css(css))

    def raw_product(self, response):
        json_text = clean(response.css(self.details_css))[0]
        return json.loads(json_text)

    def product_name(self, response):
        name = clean(response.css(self.details_css))[0]
        return json.loads(name).get("name")

    def product_category(self, response):
        return clean(response.css('.breadcrumb a::text'))

    def product_gender(self, raw_product, response):
        raw_gender = raw_product["gender"]
        categories = self.product_category(response)
        soup = f"{' '.join(categories)} {raw_gender}"

        return self.gender_lookup(soup) or "unisex-adults"

    def product_description(self, response, **kwargs):
        css_1 = ".description ::text"
        css_2 = ".product-bullets span ::text,.product-bullets a ::text"
        raw_description = clean(response.css(css_1))
        raw_description += [' '.join(clean(response.css(css_2)))]

        return raw_description

    def product_care(self, response, **kwargs):
        care_css = '.attributes-box ::text'
        return [' '.join(clean(response.css(care_css)))]


class CommonCrawlSpider(BaseCrawlSpider):
    listings_css = [
        ".nav-item .sub-nav-column-container",
        ".infinite-scroll-placeholder"

    ]
    product_css = '.product-image'

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, attrs=["href", "data-grid-url"]),
             callback='parse'),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )


class IceBreakerParseSpider(CommonParseSpider, IceBreakerMixin):
    name = IceBreakerMixin.retailer + '-parse'


class IceBreakerCrawlSpider(CommonCrawlSpider, IceBreakerMixin):
    name = IceBreakerMixin.retailer + '-crawl'
    parse_spider = IceBreakerParseSpider()
