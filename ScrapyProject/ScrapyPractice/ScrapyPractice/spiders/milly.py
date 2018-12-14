# coding: utf-8
"""
Scrapy spider for Milly.
"""

import json

from copy import deepcopy
from scrapy import Request

from scrapyproduct.items import ProductItem, SizeItem
from scrapyproduct.spiderlib import SSBaseSpider
from scrapyproduct.toolbox import category_mini_item


class MillySpider(SSBaseSpider):
    name = 'milly'
    long_name = 'Milly'
    base_url = 'http://www.milly.com/'
    max_stock_level = 1
    version = '3.0.0'

    seen_base_skus = []
    category_blacklist = ['#millymoment']

    def start_requests(self):
        meta = {
            'country_code': 'us',
            'language_code': 'en',
            'currency': 'USD'
        }
        yield Request(self.base_url, meta=meta, callback=self.parse_homepage)

    def make_request(self, selectors, response, type=1):
        """
        make requests for category levels
        """
        category_level_label = [sel.xpath("./a/text()").extract_first('').strip() for sel in selectors]
        if type == 2:
            category_level_label[-1] = selectors[-1].xpath("./a/h4/text()").extract_first('').strip()

        url = selectors[-1].xpath("./a/@href").extract_first()
        meta = deepcopy(response.meta)
        meta['categories'] = category_level_label
        return Request(
            url=response.urljoin(url),
            callback=self.parse_products,
            meta=meta,
        )

    def parse_homepage(self, response):
        for level1 in response.css("#main-nav > div"):
            level1_label = level1.xpath("./a/text()").extract_first('').strip()
            if level1_label in self.category_blacklist:
                continue
            yield self.make_request([level1], response)

            for level2 in level1.css("div .header__main-nav-branch"):
                yield self.make_request([level1, level2], response)

                for level3 in level2.xpath("./ul/li"):
                    yield self.make_request([level1, level2, level3], response)

            for level2 in level1.css("div .header__main-nav-img-branch"):
                yield self.make_request([level1, level2], response, type=2)

    def parse_products(self, response):
        next_url = response.css('#last-rendered-paginate-link::attr(href)').extract_first()
        if next_url:
            yield Request(
                response.urljoin(next_url),
                meta=response.meta,
                callback=self.parse_products
            )

        for product in response.css("#last-rendered-list>div"):
            base_sku = product.css(".collection-card__img::attr(data-src)").extract_first().split('/')[-1].split('_')[0]
            item = ProductItem(
                url=''.join([self.base_url[:-1], product.css("a::attr(href)").extract_first()]),
                referer_url=response.url,
                country_code=response.meta['country_code'],
                base_sku=base_sku,
                language_code=response.meta['language_code'],
                category_names=response.meta['categories'],
                currency=response.meta['currency'],
            )

            yield category_mini_item(item)
            if item['base_sku'] in self.seen_base_skus:
                continue

            self.seen_base_skus.append(item['base_sku'])
            meta = deepcopy(response.meta)
            meta['item'] = item

            yield Request(
                url='{}.js'.format(item['url']),
                meta=meta,
                callback=self.parse_details,
            )

    def parse_details(self, response):
        item = response.meta['item']
        details = json.loads(response.text)

        item['use_size_level_prices'] = True
        item['available'] = details['available']
        item['description_text'] = details['description'] or 'N/A'
        item['brand'] = details['vendor']
        item['title'] = details['title']

        colors = [option['values'] for option in details['options'] if option["name"] == "Color"][0]
        colors = [color for color in colors if 'ns' not in color and 'NS' not in color]
        for color in colors:
            color_item = deepcopy(item)
            color_item['color_name'] = color
            color_item['identifier'] = "{}_{}".format(item["base_sku"], color)
            color_item['available'] = True

            sizes = [size for size in details['variants'] if color in size['options']]
            self.extract_size(color_item, sizes)

            if not color_item['image_urls']:
                color_item['image_urls'] = details['images']

            yield color_item

    def extract_size(self, color_item, sizes):
        image = sizes[0].get('featured_image')
        for size in sizes:
            color_item['image_urls'].append(image['src']) if image else ''
            old_price, cur_price = self.extract_prices(size)
            color_item['size_infos'].append(
                SizeItem(
                    size_name=size['public_title'].split('/')[-1],
                    size_identifier=size['id'],
                    size_original_price_text=old_price,
                    size_current_price_text=cur_price,
                    stock=1 if size['available'] else 0,
                )
            )

    def extract_prices(self, size):
        cur_price = str(size['price'])[:-2]
        old_price = str(size['compare_at_price'])[:-2] if size['compare_at_price'] else cur_price

        return old_price, cur_price
