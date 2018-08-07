# -*- coding: utf-8 -*-
import re
from urllib.parse import parse_qsl, urljoin

import scrapy
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from items import WoolrichItem


class WoolrichSpider(CrawlSpider):
    name = 'woolrich'
    allowed_domains = ['woolrich.com']
    start_urls = ['http://www.woolrich.com/woolrich/?countryCode=CA']

    download_delay = 0.5

    request_url = 'http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp'
    genders = ['Men', 'Women']

    listing_css = ['.nav.navbar-nav .upper', '.clear.addMore']
    rules = (
        Rule(LinkExtractor(restrict_css=listing_css, tags=(
            'a', 'div'), attrs=('href', 'nextpage'))),
        Rule(LinkExtractor(restrict_css=('.productCard')), callback='parse_item')
    )

    def parse_item(self, response):
        item = WoolrichItem()
        item['retailer_sku'] = self._get_retailer_sku(response)
        item['gender'] = self._get_gender(response)
        item['category'] = self._get_category(response)
        item['brand'] = self._get_brand(response)
        item['url'] = response.url
        item['name'] = self._get_name(response)
        item["description"] = self._get_description(response)
        item['care'] = self._get_care(response)
        item['image_urls'] = self._get_image_urls(response)
        item['skus'] = []

        item['meta'] = {
            'queued_reqs': self._color_requests(response, item)
        }
        return self.next_request(item)

    def next_request(self, item):
        if item['meta']['queued_reqs']:
            req = item['meta']['queued_reqs'].pop()
            req.meta['item'] = item
            return req

        del item['meta']
        return item

    def _color_requests(self, response, item):
        color_ids = response.css(
            '.colorlist .link img::attr(colorid)').extract()
        color_reqs = []
        for color_id in color_ids:
            formdata = {'productId': item['retailer_sku'], 'colorId': color_id}
            req = self.make_request(formdata, self._process_color)
            color_reqs.append(req)

        return color_reqs

    def _size_requests(self, response):
        sizes = response.css('.sizelist li a::attr(title)').extract()
        size_ids = response.css('.sizelist li a::attr(id)').extract()
        size_reqs = []
        for size, size_id in zip(sizes, size_ids):
            formdata = dict(parse_qsl(response.request.body.decode()))
            formdata['selectedSize'] = size
            formdata['skuId'] = size_id

            req = self.make_request(formdata, self._process_size)
            size_reqs.append(req)

        return size_reqs

    def _fitting_requests(self, response):
        fittings = response.css('.dimensionslist a::attr(title)').extract()
        fitting_ids = response.css('.dimensionslist a::attr(id)').extract()
        fitting_reqs = []
        for fit, fit_id in zip(fittings, fitting_ids):
            formdata = dict(parse_qsl(response.request.body.decode()))
            formdata['selectedDimension'] = fit
            formdata['skuId'] = fit_id

            req = self.make_request(formdata, self._process_fitting)
            fitting_reqs.append(req)

        return fitting_reqs

    def _process_color(self, response):
        item = response.meta.get('item')

        item['meta']['queued_reqs'] += self._size_requests(response)
        return self.next_request(item)

    def _process_size(self, response):
        item = response.meta.get('item')

        fitting_reqs = self._fitting_requests(response)
        if not fitting_reqs:
            item['skus'].append(self._get_sku(response))

        item['meta']['queued_reqs'] += fitting_reqs
        return self.next_request(item)

    def _process_fitting(self, response):
        item = response.meta.get('item')
        item['skus'].append(self._get_sku(response))

        return self.next_request(item)

    def _get_retailer_sku(self, response):
        return response.css('[itemprop="productID"]::text').extract_first().strip()

    def _get_gender(self, response):
        prod_name = self._get_name(response)
        for gender in self.genders:
            if gender in prod_name:
                return gender

        return 'Unisex-Adults'

    def _get_category(self, response):
        return response.css('.breadcrumb a::text').extract()[1:]

    def _get_brand(self, response):
        return response.css('[itemprop="brand"]::attr(content)').extract_first()

    def _get_name(self, response):
        return response.css('[itemprop="name"]::text').extract_first()

    def _get_description(self, response):
        description = response.css('[itemprop="description"]::text').extract()
        return [self.clean_text(d) for d in description]

    def _get_care(self, response):
        care = response.css('.span4 .text li::text').extract()
        return [self.clean_text(c) for c in care]

    def _get_image_urls(self, response):
        img_links = response.css(
            '.zoom .product-image-link img::attr(src)').extract()
        return [urljoin(response.url, l) for l in img_links]

    def _get_sku(self, response):
        sku = self._extract_sku_pricing(response)
        sku['color'] = self._extract_color(response)
        sku['size'] = self._get_size(response)
        sku['id'] = self._get_sku_id(response)

        if self._sku_stock_level(response) == '0':
            sku['out_of_stock'] = True

        return sku

    def _extract_sku_pricing(self, response):
        return {
            'price': self._extract_price(response),
            'previous price': self._extract_prev_price(response),
            'currency': self._extract_currency(response)
        }

    def _extract_color(self, response):
        return response.css('.colorName::text').extract_first().strip()

    def _extract_currency(self, response):
        return response.css('[itemprop="priceCurrency"]::attr(content)').extract_first()

    def _extract_price(self, response):
        price = int(response.css(
            '[itemprop="price"]::attr(content)').extract_first())
        return self.to_cent(price)

    def _extract_prev_price(self, response):
        previous_price = response.css('.strikethrough::text').extract_first()
        if previous_price:
            previous_price = int(self.clean_text(previous_price).split()[-1])
            return self.to_cent(previous_price)

    def _get_size(self, response):
        size_css = '.sizelist a.selected::attr(title), .dimensionslist a.selected::attr(title)'
        return '/'.join(response.css(size_css).extract())

    def _get_sku_id(self, response):
        sku_id_css = '.sizelist a.selected::attr(id), .dimensionslist a.selected::attr(id)'
        return response.css(sku_id_css).extract()[-1]

    def _sku_stock_level(self, response):
        stock_css = '.sizelist a.selected::attr(stocklevel), .dimensionslist a.selected::attr(stocklevel)'
        return response.css(stock_css).extract()[-1]

    def make_request(self, formdata, callback):
        return FormRequest(url=self.request_url, callback=callback, formdata=formdata)

    def to_cent(self, price):
        return round(price*100)

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text)
