import json
import urllib.parse

import re
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = "shoecarnival-us"
    market = 'US'
    allowed_domains = ['shoecarnival.com', 'i1.adis.ws']

    start_urls = [
        'http://www.shoecarnival.com/']

    colour_req_t = "http://www.shoecarnival.com/browse/gadgets/pickerContents.jsp?_DARGS=/browse/gadgets/pickerContents.jsp.colorsizerefreshform" \
                   "&_dyncharset=UTF-8&_dynSessConf=-4196040722391773449&productId={0}&categoryId={1}&selectedColor={2}"

    size_req_t = "http://www.shoecarnival.com/browse/gadgets/pickerContents.jsp?_DARGS=/browse/gadgets/pickerContents.jsp.colorsizerefreshform" \
                 "&_dyncharset=UTF-8&_dynSessConf=-4196040722391773449&productId={0}&categoryId={1}&selectedColor={2}&selectedWidth=&selectedSize={3}"

    image_url_t = "http://i1.adis.ws/s/scvl/{0}.js?&v=1&deep=true&timestamp=962277038988&arg=%{0}%27&func=amp.jsonReturn"

    gender = [
        'Women',
        'Men',
        'Girls',
        'Boys'
    ]


class ShoecarnivalParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + "-parse"
    price_css = '.product-price span:not([class="item-price-meta-save"])::text'

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)

        if not garment:
            return

        self.boilerplate_normal(garment, response)
        garment['gender'] = self.product_gender(response)
        garment['image_urls'] = []

        garment['skus'] = {}

        garment['meta'] = {
            'requests_queue': self.image_requests(response) + self.colour_requests(response) + self.size_requests(
                response)}

        return self.next_request_or_garment(garment)

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['meta']['requests_queue'] += self.size_requests(response) + self.image_requests(response)

        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))

        return self.next_request_or_garment(garment)

    def parse_images(self, response):
        garment = response.meta['garment']
        garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return response.css('span.atg_store_pickerLabel::text').extract_first().split('# ')[1]

    def raw_name(self, response):
        return clean(response.css('.pdp-name::text'))[0]

    def product_brand(self, response):
        return response.css('.pdp-logo img::attr(alt)').extract_first()

    def product_name(self, response):
        raw_name = self.raw_name(response).upper()
        raw_name = raw_name.replace(self.product_brand(response), "")

        return raw_name.lower()

    def product_category(self, response):
        return clean(response.css('div[id="atg_store_breadcrumbs"] a::text'))

    def product_gender(self, response):
        gender_u = " ".join(self.product_category(response) + [self.product_name(response)])

        for raw_gender in self.gender:
            if raw_gender in gender_u:
                return raw_gender.lower()
        return "unisex-adults"

    def raw_description(self, response):
        return clean(response.css('section[id="product-description"] ::text'))

    def product_description(self, response):
        return [rd for rd in self.raw_description(response) if not self.care_criteria(rd)]

    def product_care(self, response):
        return [rd for rd in self.raw_description(response) if self.care_criteria(rd)]

    def image_urls(self, response):
        raw_images = "{" + re.findall('MSET",(.*)\);', response.text)[0]
        raw_images = json.loads(raw_images)["items"]

        return [img['src'] for img in raw_images]

    def skus(self, response):
        sku = {'colour': response.css('div.atg_store_pickerLabel span::text').extract_first()}
        sku['size'] = response.css('option.charcoal.size_chart[selected]::attr(value)').extract_first()
        sku.update(self.product_pricing_common_new(response))

        return {sku['colour'] + "_" + sku['size']: sku}

    def category_id(self, response):
        return response.css('input[name="categoryId"]::attr(value)').extract_first()

    def colour_requests(self, response):
        color_requests = []
        colours = response.css('.color-wrapper div:not([class="swatch active"]) a::attr(data-color-name)').extract()

        for colour in colours:
            colour = urllib.parse.quote(colour).replace("/", "%2F")

            colour_url = self.colour_req_t.format(self.product_id(response), self.category_id(response), colour)
            color_requests.append(Request(colour_url, callback=self.parse_colour))

        return color_requests

    def size_requests(self, response):
        size_requests = []

        colour = response.css('div[class="swatch active"] a::attr(data-color-name)').extract_first()
        sizes = response.css('option.charcoal.size_chart:not(disabled)::attr(value)').extract()

        for size in sizes:
            size = urllib.parse.quote(size).replace("/", "%2F")

            size_url = self.size_req_t.format(self.product_id(response), self.category_id(response), colour, size)
            size_requests.append(Request(size_url, callback=self.parse_size))

        return size_requests

    def image_requests(self, response):
        colour_id = response.css('div[class="swatch active"] a::attr(data-set)').extract_first()
        return [Request(self.image_url_t.format(colour_id), callback=self.parse_images)]


class ShoecarnivalCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + "-crawl"
    parse_spider = ShoecarnivalParseSpider()

    products_css = '.grid.grid-three'

    listing_css = [
        '.inline-list',
        '.hawk-arrowRight.hawk-pageLink'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, deny=('/company')),
             callback='parse'),

        Rule(LinkExtractor(restrict_css=products_css, deny=('/global')), callback='parse_item'),
    )

