import copy
import re
import json
import datetime

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

import schutzcrawler.items as items
from schutzcrawler.price_parser import PriceParser
from schutzcrawler.description_parser import DescriptionParser
from schutzcrawler.utilities import Utilities


class LiebeskindMixins:
    name = 'liebeskind'
    allowed_domains = ['liebeskind-berlin.com']
    start_urls = ['http://de.liebeskind-berlin.com/']


class ParseSpider(CrawlSpider, LiebeskindMixins, Utilities):
    name = f"{LiebeskindMixins.name}-parse"

    price_extractor = PriceParser()
    description_extractor = DescriptionParser()
    time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M")
    url_next = ""

    def parse(self, response):
        product = items.ProductItem()

        product["url"] = response.url.split('?')[0]
        product["retailer_sku"] = self.retailer_sku(response)
        product["gender"] = "women"
        product["retailer"] = "leibskind-de"
        product["category"] = self.category(response)
        product["url_original"] = response.url
        product["name"] = self.product_name(response)
        product["spider_name"] = self.name
        product["description"] = self.description(response)
        product["care"] = self.care(response)
        product["trail"] = response.meta.get('trail', [])
        product["skus"] = self.skus(response)
        product["crawl_start_time"] = self.time
        product["image_urls"] = []
        product["requests"] = []

        product["requests"].extend(self.generate_color_requests(response, product))
        yield self.next_request_or_product(product)

    def generate_color_requests(self, response, product):
        requests = []
        color_range_css = '.filter__colors__boxes input'
        color_range = response.css(color_range_css)

        quantity = response.xpath('//input[@name="Quantity"]/@value').extract_first()
        rendering_type = response.xpath('//input[@name="renderingType"]/@value').extract_first()
        page_type = response.xpath('//input[@name="pageType"]/@value').extract_first()
        fit_guide_name = response.xpath('//input[@name="fitguideName"]/@value').extract_first()
        fit_guide_use = response.xpath('//input[@name="fitguideUse"]/@value').extract_first()
        vogel_data = response.xpath('//input[@name="stickvogelData"]/@value').extract_first()
        pid = response.xpath('//input[@name="pid"]/@value').extract_first()
        cgid = response.xpath('//input[@name="cgid"]/@value').extract_first()

        for color in color_range:
            variant_name = color.css('input::attr(name)').extract_first()
            variant_value = color.css('input::attr(value)').extract_first()
            data_action = color.css('input::attr(data-action)').extract_first()

            self.url_next = (
                    f"https://de.liebeskind-berlin.com/on/demandware.store/Sites-liebeskindEU-Site/en/SPV-Dispatch?"
                    + f"view=ajax&Quantity={quantity}&renderingType={rendering_type}&pageType={page_type}&"
                    + f"fitguideName={fit_guide_name}&fitguideUse={fit_guide_use}&stickvogelData={vogel_data}&"
                    + f"{variant_name}={variant_value}&pid={pid}&cgid={cgid}&{data_action}={data_action}")

            requests.append(
                Request(url=self.url_next, callback=self.parse_image_urls, dont_filter=True, meta={'item': product}))
        return requests

    def parse_image_urls(self, response):
        product = response.meta['item']
        image_css = '.ta_imageSelector img::attr(src)'
        images = response.css(image_css).extract()
        product["image_urls"].extend(images)
        yield self.next_request_or_product(product)

    def retailer_sku(self, response):
        retailer_sku_css = '.js-productvariations-swatchbase::attr(data-product)'
        return response.css(retailer_sku_css).extract_first()

    def category(self, response):
        categories_css = '.breadcrumbs__category_name::text'
        categories = response.css(categories_css).extract()
        return [c.strip('\n') for c in categories]

    def product_name(self, response):
        return response.css('.ta_productName::text').extract_first()

    def price(self, response):
        return self.price_extractor.prices(response.css('.pdp__product-price ::text').extract())

    def skus(self, response):
        raw_colors = response.css('.filter__colors__boxes span::text').extract()
        colors = [c for c in raw_colors if re.match('^[a-zA-Z]+', c)]
        common_sku = self.price(response)
        skus = {}
        sizes = response.css('.js-productvariations-swatchbase-color a::attr(data-sizes)').extract_first()
        sizes = json.loads(sizes)

        for color, size in [(color, size) for color in colors for size in sizes]:
            sku = copy.deepcopy(common_sku)
            sku['color'] = color
            sku['size'] = size
            skus[f"{color}{size}"] = sku
        return skus

    def raw_description(self, response):
        raw_description = response.css('#pdp-details-longdesc ::text').extract()
        return [d for d in raw_description if '\n' not in d]

    def description(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description if not self.description_extractor.is_care(rd)]

    def care(self, response):
        raw_description = self.raw_description(response)
        return [rd for rd in raw_description if self.description_extractor.is_care(rd)]


class LiebeskindSpider(CrawlSpider, LiebeskindMixins):
    name = f"{LiebeskindMixins.name}-crawl"

    parser = ParseSpider()
    category_css = 'div.mainnav__level'
    pagination_css = '.pagination__btn--next'
    products_css = 'div.productlist__product .pdlist__image'

    rules = [Rule(LinkExtractor(restrict_css=[category_css, pagination_css]), callback='parse'),
             Rule(LinkExtractor(restrict_css=products_css), callback=parser.parse)]

    def parse(self, response):
        trail = response.meta.get('trail', [])
        trail.append(response.url)

        for request in list(super(LiebeskindSpider, self).parse(response)):
            trail = copy.deepcopy(trail)
            request.meta['trail'] = trail
            yield request

        # follow all pagination links
        url = response.url.split('?')[0]
        pagination_xpath = '//span[@class="pagination__btn pagination__btn--next fakelink"]/@data-pagingparams'
        pagination = response.xpath(pagination_xpath).extract_first()
        if pagination:
            pagination = json.loads(pagination)
            trail = copy.deepcopy(trail)
            next_url = f"{url}?start={pagination['start']}"
            yield Request(url=next_url, callback=self.parse, meta={'trail': trail})
