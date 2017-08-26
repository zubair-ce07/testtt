# -*- coding: utf-8 -*-
import re

from scrapy import FormRequest
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from task4.items import Product


class WoolWorthsSpider(CrawlSpider):
    name = 'woolworths'
    allowed_domains = ['woolworths.co.za']
    start_urls = ['http://www.woolworths.co.za', ]
    size_url = "http://www.woolworths.co.za/store/fragments/product-common/ww/price.jsp?productItemId={0}&colourSKUId={1}&sizeSKUId={2}"
    color_url = "http://www.woolworths.co.za/store/fragments/product-common/ww/product-item.jsp"
    download_delay = 1
    rules = (
        Rule(LinkExtractor(restrict_css=['nav.horizontal-menu.accordion--max-medium', 'ol.pagination__pages',
                                         'ul.nav-list.nav-list--main', ]), follow=True),
        Rule(LinkExtractor(deny_extensions=['.jsp', ], restrict_css=['div.product-list__list div.grid']),
             callback='parse_product'),
    )

    def parse_product(self, response):
        item = Product()
        item['brand'] = self.parse_brand(response)
        item['care'] = self.parse_care(response)
        item['category'] = self.parse_category(response)
        item['description'] = self.parse_description(response)
        item['gender'] = self.parse_gender(response)
        item['image_urls'] = [self.parse_image_urls(response)]
        item['skus'] = dict()
        item['name'] = self.parse_name(response)
        item['retailer_sku'] = self.parse_retailer_sku(response)
        item['url_original'] = self.parse_url(response)
        item['url'] = [self.parse_url(response)]
        response.meta['item'] = item

        next_color_urls = []
        current_color_id = 0
        color_queries = response.css('ul.nav-list-x.nav-list-x--wrap li img::attr(onclick)').extract()
        for raw_color_url in color_queries:
            color_id = re.findall("\((\d+)", raw_color_url)[0]
            if color_id not in response.css('img.active::attr(onclick)').extract_first():
                next_color_urls.append(color_id)
            else:
                current_color_id = color_id
        item['skus'] = self.get_skus(response, current_color_id)

        sizes = {}
        for raw_size_url in response.css('ul.nav-list-x.product__size-selector li a.product-size').extract():
            size = re.findall('">(.*)?<', raw_size_url)[0]
            size_id = re.findall('ProductSize\(\d+,(\d+)?,', raw_size_url)[0]
            sizes[size] = size_id

        if sizes:
            size = list(sizes)[0]
            url = self.size_url.format(item['retailer_sku'], current_color_id, sizes[size])
            del sizes[size]
            requirements = {"size": size, "colorid": current_color_id, "colormeta": item,
                            "next_color_urls": next_color_urls, "sizes": sizes}
            yield Request(url, callback=self.parse_size, meta=requirements)

    def parse_next_color_items(self, response):
        next_color_urls = response.meta['next_color_urls']
        item = response.meta['item']
        item['url'].append(self.parse_url(response))
        item['image_urls'].append(self.parse_image_urls(response))
        current_color_id = response.meta['current_color_id']
        item['skus'] = self.get_skus(response, current_color_id)

        sizes = {}
        for raw_size_url in response.css('ul.nav-list-x.product__size-selector li a.product-size').extract():
            size = re.findall('">(.*)?<', raw_size_url)[0]
            size_id = re.findall('ProductSize\(\d+,(\d+)?,', raw_size_url)[0]
            sizes[size] = size_id
        if sizes:
            size = list(sizes)[0]
            url = self.size_url.format(item['retailer_sku'], current_color_id, sizes[size])
            del sizes[size]
            requirements = {"size": size, "colorid": current_color_id, "colormeta": item,
                            "next_color_urls": next_color_urls, "sizes": sizes}
            yield Request(url, callback=self.parse_size, meta=requirements)

    def parse_brand(self, response):
        return response.css(
            'div[itemtype="http://schema.org/Product"] meta[itemprop="brand"]::attr(content)').extract_first()

    def parse_care(self, response):
        return response.xpath('//div[@class="accordion__segment--chrome"][2]/div/img/@src').extract_first()

    def parse_category(self, response):
        return "/".join(response.css('ol.breadcrumb li a::text').extract())

    def parse_description(self, response):
        description = response.xpath('//div[@class="accordion__segment--chrome"][1]/div/p[2]/text()').extract()
        description += response.xpath(
            '//div[@class="accordion__segment--chrome"][1]/div/ul[not(@class)]/li/text()').extract()
        return "\n".join(description)

    def parse_gender(self, response):
        category = "/".join(response.css('ol.breadcrumb li a::text').extract())
        if any(x in category for x in ["Girls", "Women"]):
            return "Female"
        if any(x in category for x in ["Boys", "Men"]):
            return "Male"

    def parse_image_urls(self, response):
        return response.css('div.pdp__image img::attr(src)').extract_first()

    def parse_name(self, response):
        return response.css('input[id="gtmProductDisplayName"]::attr(value)').extract_first()

    def parse_retailer_sku(self, response):
        return response.css('input[id="gtmProductId"]::attr(value)').extract_first()

    def parse_color(self, response):
        return response.css('p:contains("First select a colour:")+input::attr(value)').extract_first()

    def parse_currency(self, response):
        return "ZAR (South African Rand)"

    def parse_price(self, response):
        return response.css(
            'div[itemtype="http://schema.org/Product"] meta[itemprop="price"]::attr(content)').extract_first()

    def parse_available_sizes(self, response):
        sizes = []
        for size_element in response.css('ul.nav-list-x.product__size-selector li a.product-size').extract():
            sizes.append(re.findall('">(.*)?<', size_element)[0])
        return sizes

    def get_skus(self, response, current_color_id):
        skus = response.meta['item']['skus']
        sizes_of_item = self.parse_available_sizes(response)
        for size in sizes_of_item:
            item_characterstics = dict(
                colour=self.parse_color(response),
                currency=self.parse_currency(response),
            )
            key = self.get_key(current_color_id, size)
            item_characterstics['size'] = size
            skus[key] = item_characterstics
        return skus

    def parse_url(self, response):
        return response.url

    def get_key(self, key_part, size):
        return u"{0}_{1}".format(key_part, size)

    def parse_size(self, response):
        price = response.xpath('//span[@class="price"]/@content').extract_first()
        item = response.meta['colormeta']
        skus = item['skus']
        current_color_id = response.meta['colorid']
        size = response.meta['size']
        item_characterstics = skus[self.get_key(current_color_id, size)]
        item_characterstics['price'] = price

        next_color_urls = response.meta["next_color_urls"]
        sizes = response.meta['sizes']

        if sizes:
            size = list(sizes)[0]
            url = self.size_url.format(item['retailer_sku'], current_color_id, sizes[size])
            del sizes[size]
            requirements = {"size": size, "colorid": current_color_id, "colormeta": item,
                            "next_color_urls": next_color_urls, "sizes": sizes}
            yield Request(url, callback=self.parse_size, meta=requirements)
        else:
            if not next_color_urls:
                yield item
            else:
                next_color_page_id = next_color_urls.pop(0)
                formdata = {
                    'productItemId': item['retailer_sku'],
                    'colourSKUId': next_color_page_id,
                    'pageSource': "",
                }
                formrequest = FormRequest(
                    'http://www.woolworths.co.za/store/fragments/product-common/ww/product-item.jsp',
                    callback=self.parse_next_color_items,
                    formdata=formdata, priority=0)
                formrequest.meta['item'] = item
                formrequest.meta['next_color_urls'] = next_color_urls
                formrequest.meta['current_color_id'] = next_color_page_id
                yield formrequest
