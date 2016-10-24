# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.selector import Selector
from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, clean
from scrapy.utils.url import add_or_replace_parameter
from urlparse import urljoin
from scrapy import Request
import re
import math
import json


class Mixin(object):
    market = 'DE'
    retailer = 'runnerspoint-de'
    brand = 'Runners Point'
    lang = 'de'
    allowed_domains = ['www.runnerspoint.de', 'runnerspoint.scene7.com']
    start_urls = ['https://www.runnerspoint.de/de/damen/',
                  'https://www.runnerspoint.de/de/herren/']
    care_materials = [
        'obermaterial'
    ]


class RunnersPointParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = "//*[@itemprop='price']/@content|//*[@class='fl-price--old--value']//text()"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate(garment, response, response)
        product_info = self.product_info(response)
        print 'Prod info', product_info
        garment['brand'] = self.product_brand()
        garment['gender'] = self.product_gender(product_info)
        garment['category'] = self.product_category(product_info)
        garment['name'] = self.product_name(response, product_info)
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)
        meta = {
            'color': self.product_color(product_info),
            'currency': self.currency(response),
            'requests_queue': [
                self.image_set_request(product_id),
                self.size_request(response)
            ]
        }
        meta['previous_price'], meta['price'], _ = self.product_pricing(response)
        garment['meta'] = meta
        return self.next_request_or_garment(garment, drop_meta=False) + self.color_requests(response)

    def product_info(self, response):
        script_elements = response.xpath("//script[contains(text(), '// tracking function exists')]").extract()
        for script in script_elements:
            garment_search_result = re.search('_st\(\'addTagProperties\',(.+?)\);', script)
            if garment_search_result:
                return json.loads(
                    garment_search_result.group(1).replace('\'', '"'))

    def raw_description(self, response):
        return clean(response.css('[itemprop="description"] ::text'))

    def additional_description(self, response):
        description = []
        for desc in response.css('.fl-product-details--description--attributes-label'):
            field = desc.css(' b ::text').extract_first()
            val = desc.css(' p ::text').extract_first()
            if not val:
                val = desc.xpath('following::*//*[contains(@class, "item__selected")]//text()').extract_first()
            description += [field + val]
        return description

    def product_care(self, response):
        return [x for x in self.raw_description(response) if self.care_criteria_simplified(x)]

    def product_description(self, response):
        return [x for x in self.raw_description(response) if not self.care_criteria_simplified(x)] + \
               self.additional_description(response)

    def product_brand(self):
        return self.brand

    def currency(self, response):
        return clean(response.css('[itemprop=priceCurrency]::attr(content)'))[0]

    def product_id(self, response):
        return clean(response.css('.fl-rating ::attr(data-ratings-externalid)'))[0]

    def product_category(self, garment):
        return clean(garment['category'].split('/'))

    def product_gender(self, garment):
        return garment['gender']

    def product_color(self, product):
        return ''.join([c for c in product['variant'] if c.isalpha()])

    def product_name(self, response, garment):
        return clean(response.css(
            '.fl-product-details--headline ::text').extract_first().strip(garment['brand']))

    def image_set_request(self, product_id):
        url = urljoin('https://runnerspoint.scene7.com/is/image/rpe/', product_id)
        return Request(add_or_replace_parameter(url, 'req', 'set,json'), callback=self.parse_image_urls)

    def color_requests(self, response):
        request_urls = response.css('[data-color-selection-item]:not([class*=active]) ::attr(href)').extract()
        return [Request(url, callback='parse_item') for url in request_urls]

    def size_request(self, response):
        url = response.css(
            '[data-lazyloading-success-handler="productVariationSelectionInitElement"]::attr("data-request")') \
            .extract_first()
        return Request(url, callback=self.parse_skus)

    def parse_image_urls(self, response):
        image_search_res = re.search('s7jsonResponse\((.+?),\"\"\);',response.text)
        if image_search_res:
            image_set = json.loads(image_search_res.group(1).replace('\'', '"'))
            image_urls = []
            for img in image_set['set']['item']:
                url = urljoin('https://runnerspoint.scene7.com/is/image/', img['i']['n'])
                url = add_or_replace_parameter(url, 'wid', '1600')
                url = add_or_replace_parameter(url, 'hei', '900')
                image_urls += [url]
            response.meta['garment']['image_urls'] = image_urls

        return self.next_request_or_garment(response.meta['garment'])

    def parse_skus(self, response):
        skus = {}
        js = json.loads(response.text)
        garment_meta = response.meta['garment']['meta']
        content_selector = Selector(text=js['content'])
        for size_var in content_selector.css('.fl-product-size button'):
            sku = {
                'colour': garment_meta['color'],
                'price': garment_meta['price'],
                'currency': garment_meta['currency'],
                'size': clean(size_var.css(' ::text'))[0]
            }
            if garment_meta['previous_price']:
                sku['previous_prices'] = [garment_meta['previous_price']]

            if size_var.css('.fl-product-size--item__not-available'):
                sku['out_of_stock'] = True
            skus[garment_meta['color'] + '_' + sku['size'].replace(' ', '_')] = sku

        response.meta['garment']['skus'] = skus
        return self.next_request_or_garment(response.meta['garment'])


class RunnersPointCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = RunnersPointParseSpider()
    products_css = [
        '.fl-product-tile',
        '[data-color-selection-item]:not([class*=active])'
    ]
    listings_css = '.fl-navigation--title-category'
    products_per_page = 60
    deny_re = ['/Sportern%c3%a4hrung/',
               '/Zubeh%c3%b6r/',
               '/Zubeh%C3%B6r/',
               '/Einlegesohlen/',
               '/Sicherheit/',
               '/Trinksysteme/',
               '/Pflegemittel/',
               '/B%c3%bccher--Literatur/',
               '/sonstiges-Laufzubeh%c3%b6r/',
               '/Sets/',
               ]

    rules = (
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item'),
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_pages'),
    )

    def total_products(self, response):
        css = '.fl-product-list--header--title-count ::text'
        articles_count = str(response.css(css).extract_first())
        articles_search_res = re.search(r'\d+', articles_count)
        if articles_search_res:
            return int(articles_search_res.group())

    def pagination_url(self, response):
        return response.css(
            '[data-ajaxcontent="productpagebutton"] .fl-btn__default::attr(data-ajaxcontent-url)').extract_first()

    def parse_pages(self, response):
        total_products = self.total_products(response)
        if not total_products or total_products < self.products_per_page:
            return

        total_pages = math.ceil(total_products / self.products_per_page)
        url = self.pagination_url(response)
        for page_num in range(1, total_pages):
            yield Request(
                add_or_replace_parameter(url, 'PageNumber', page_num),
                self.parse_product_links, meta={'trail': self.add_trail(response)})

    def parse_product_links(self, response):
        js = json.loads(response.text)
        content_selector = Selector(text=js['content'])
        for product in content_selector.xpath("//div[contains(@class,'fl-product-tile--container')]//@href").extract():
            yield Request(product, callback=self.parse_item, meta={'trail': self.add_trail(response)})
