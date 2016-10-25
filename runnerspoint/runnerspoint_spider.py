# -*- coding: utf-8 -*-
import re
import math
import json
from urlparse import urljoin

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.selector import Selector
from scrapy.utils.url import add_or_replace_parameter

from skuscraper.spiders.base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin(object):
    market = 'DE'
    retailer = 'runnerspoint-de'
    brand = 'Runners Point'
    lang = 'de'
    allowed_domains = ['www.runnerspoint.de', 'runnerspoint.scene7.com']
    start_urls = [
        'https://www.runnerspoint.de/de/damen/',
        'https://www.runnerspoint.de/de/herren/'
    ]


class RunnersPointParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = "//*[@itemprop='price']/@content|//*[@class='fl-price--old--value']//text()"
    care_materials = [
        'obermaterial'
    ]

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate(garment, response, response)

        raw_product = self.raw_product(response)
        garment['brand'] = self.product_brand(raw_product)
        garment['gender'] = self.product_gender(raw_product)
        garment['category'] = self.product_category(raw_product)
        garment['name'] = self.product_name(response, raw_product)
        garment['description'] = self.product_description(response)
        garment['care'] = self.product_care(response)
        garment_meta = {
            'color': self.product_color(raw_product),
            'currency': self.currency(response),
            'requests_queue': [
                self.images_request(product_id),
                self.size_request(response)
            ]
        }
        garment_meta['previous_price'], garment_meta['price'], _ = self.product_pricing(response)
        garment['meta'] = garment_meta

        return self.next_request_or_garment(garment, drop_meta=False) + self.color_requests(response)

    def raw_product(self, response):
        xpath = "//script[contains(text(), '// tracking function exists')]"
        script_elements = response.xpath(xpath).extract()
        for script in script_elements:
            regex = '_st\(\'addTagProperties\',(.+?)\);'
            raw_products = re.findall(regex, script)
            if raw_products:
                return json.loads(raw_products[0].replace('\'', '"'))

    def raw_description(self, response):
        return clean(response.css('[itemprop="description"] ::text'))

    def product_care(self, response):
        return [x for x in self.raw_description(response) if self.care_criteria_simplified(x)]

    def product_description(self, response):
        description = [x for x in self.raw_description(response) if not self.care_criteria_simplified(x)]
        css = '.fl-product-details--description--attributes-label'
        for desc in response.css(css):
            field = desc.css('b ::text').extract_first()
            val = desc.css('p ::text').extract_first()
            if not val:
                css = 'following::*//*[contains(@class, "item__selected")]//text()'
                val = desc.xpath(css).extract_first()
            description += [field + val]

        return description

    def product_brand(self, raw_product):
        return raw_product['brand'] if raw_product['brand'] else 'Runners Point'

    def currency(self, response):
        css = '[itemprop=priceCurrency]::attr(content)'
        return clean(response.css(css))[0]

    def product_id(self, response):
        css = '.fl-rating ::attr(data-ratings-externalid)'
        return clean(response.css(css))[0]

    def product_category(self, raw_product):
        return clean(raw_product['category'].split('/'))

    def product_gender(self, raw_product):
        return raw_product['gender']

    def product_color(self, raw_product):
        return ''.join([c for c in raw_product['variant'] if c.isalpha()])

    def product_name(self, response, raw_product):
        css = '.fl-product-details--headline ::text'
        title = response.css(css).extract()[0]
        return clean(title.strip(raw_product['brand']))

    def images_request(self, product_id):
        prefix = 'https://runnerspoint.scene7.com/is/image/rpe/'
        url = urljoin(prefix, product_id)
        url = add_or_replace_parameter(url, 'req', 'set,json')

        return Request(url, callback=self.parse_images)

    def color_requests(self, response):
        css = '[data-color-selection-item]:not([class*=active]) ::attr(href)'
        request_urls = response.css(css).extract()

        return [Request(url, callback='parse_item') for url in request_urls]

    def size_request(self, response):
        css = '#add-to-cart-form ::attr("data-request")'
        url = response.css(css).extract()[0]

        return Request(url, callback=self.parse_skus)

    def parse_images(self, response):
        garment = response.meta['garment']
        garment['image_urls'] = self.image_urls(response)

        return self.next_request_or_garment(garment)

    def image_urls(self, response):
        raw_urls = re.findall('s7jsonResponse\((.+?),\"\"\);', response.text)[0]
        raw_urls = json.loads(raw_urls.replace('\'', '"'))

        image_urls = []
        prefix = 'https://runnerspoint.scene7.com/is/image/'
        for img in raw_urls['set']['item']:
            if not ('i' in img or 'n' in img['i']):
                continue
            url = urljoin(prefix, img['i']['n'])
            url = add_or_replace_parameter(url, 'wid', '1600')
            url = add_or_replace_parameter(url, 'hei', '900')
            image_urls += [url]

        return image_urls

    def parse_skus(self, response):
        garment = response.meta['garment']
        garment['skus'] = self.skus(response)

        return self.next_request_or_garment(garment)

    def skus(self, response):
        raw_skus = json.loads(response.text)
        selector = Selector(text=raw_skus['content'])
        garment_meta = response.meta['garment']['meta']
        skus = {}
        for size_var in selector.css('.fl-product-size button'):
            sku = {
                'colour': garment_meta['color'],
                'price': garment_meta['price'],
                'currency': garment_meta['currency'],
                'size': clean(size_var.css('::text'))[0]
            }
            if garment_meta['previous_price']:
                sku['previous_prices'] = [garment_meta['previous_price']]

            css = '.fl-product-size--item__not-available'
            if size_var.css(css):
                sku['out_of_stock'] = True
            skus[garment_meta['color'] + '_' + sku['size'].replace(' ', '_')] = sku

        return skus


class RunnersPointCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = RunnersPointParseSpider()
    products_css = [
        '.fl-product-tile',
        '[data-color-selection-item]:not([class*=active])'
    ]
    listings_css = '.fl-navigation--title-category'
    products_per_page = 60
    deny_re = [
        '/Sportern%c3%a4hrung/',
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
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse_paging'),
    )

    def total_products(self, response):
        css = '.fl-product-list--header--title-count ::text'
        articles_count = str(response.css(css).extract_first())
        articles_search_res = re.search(r'\d+', articles_count)
        if articles_search_res:
            return int(articles_search_res.group())

    def pagination_url(self, response):
        css = '[data-ajaxcontent="productpagebutton"] ::attr(data-ajaxcontent-url)'
        return response.css(css).extract_first()

    def parse_paging(self, response):
        total_products = self.total_products(response)
        if not total_products or total_products < self.products_per_page:
            return

        total_pages = math.ceil(total_products / self.products_per_page)
        url = self.pagination_url(response)
        for page_num in range(1, total_pages):
            yield Request(
                add_or_replace_parameter(url, 'PageNumber', page_num),
                self.parse_products, meta={'trail': self.add_trail(response)})

    def parse_products(self, response):
        js = json.loads(response.text)
        content_selector = Selector(text=js['content'])
        css = ".fl-product-tile--container ::attr(href)"
        for product in content_selector.css(css).extract():
            yield Request(product, callback=self.parse_item, meta={
                'trail': self.add_trail(response)
            })
