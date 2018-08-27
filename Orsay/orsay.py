import json
import re
from urllib.parse import urlencode, urlparse, parse_qsl

import scrapy

from Orsay.items import ProductItem, SizeItem


class OrsaySpider(scrapy.Spider):
    name = 'orsay'
    page_size = 72
    start_urls = [
        'http://www.orsay.com/de-de/'
    ]

    def parse(self, response):
        for level_1_selector in response.css('nav.header-navigation > .navigation.level-1 > li:not(.hidden-xlg)'):
            anchor_selector = level_1_selector.css('a.level-1')
            cat_1 = anchor_selector.css('::text').extract_first().strip('\n')
            level_1_url = anchor_selector.css('::attr(href)').extract_first()
            level_2 = level_1_selector.css('li.level-2:not(.hidden-xlg)')

            if not level_2:
                url = response.urljoin(level_1_url)
                yield scrapy.Request(url,
                                     meta={'category': [cat_1], 'link': url},
                                     callback=self.parse_listing_page,
                                     dont_filter=True)

            for level_2_selector in level_2:
                anchor_selector = level_2_selector.css('a.level-2')
                cat_2 = anchor_selector.css('::text').extract_first().strip('\n')
                level_2_url = anchor_selector.css('::attr(href)').extract_first()
                level_3 = level_2_selector.css('li.level-3:not(.hidden-xlg)')

                if not level_3:
                    url = response.urljoin(level_2_url)
                    yield scrapy.Request(url,
                                         meta={'category': [cat_1, cat_2], 'link': url},
                                         callback=self.parse_listing_page,
                                         dont_filter=True)

                for level_3_selector in level_3:
                    anchor_selector = level_3_selector.css('a.level-3')
                    cat_3 = anchor_selector.css('::text').extract_first().strip('\n')
                    level_3_url = anchor_selector.css('::attr(href)').extract_first()
                    url = response.urljoin(level_3_url)
                    yield scrapy.Request(url,
                                         meta={'category': [cat_1, cat_2, cat_3], 'link': url},
                                         callback=self.parse_listing_page,
                                         dont_filter=True)

    def parse_listing_page(self, response):
        total_products = response.css('.pagination ::attr(data-count)').extract_first('0')
        product_links = response.css('a.thumb-link::attr(href)').extract()

        for product in product_links:
            product_link = response.urljoin(product)
            yield scrapy.Request(product_link, meta=response.meta, callback=self.parse_data)

        for start in range(self.page_size, int(total_products), self.page_size):
            query = {'sz': self.page_size, 'start': start, 'format': 'page-element'}
            parsed_link = urlparse(response.url)._replace(query=urlencode(query)).geturl()
            yield scrapy.Request(parsed_link,
                                 meta=response.meta,
                                 callback=self.parse_listing_page)

    def parse_data(self, response):
        if not re.findall('\d{12}', response.url):
            return

        product = ProductItem()
        # Assign website details its name & url through meta
        product['referrer_url'] = response.meta['link']
        # Initialize the dict to store the color & size information
        product['skus'] = {}
        product['image_urls'] = []
        product['url'] = response.url
        product['retailer_sku'] = re.findall('\d{6}', response.url)[0]
        product['brand'] = 'Orsay'
        product['care'] = response.css('div.product-material p::text').extract()

        detail = json.loads(response.css('div::attr(data-product-details)').extract_first())
        product['category'] = response.meta.pop('category')
        product['product_name'] = detail.get('name') or 'Anonymous'
        product['currency'] = detail.get('currency_code') or 'EUR'

        product['description'] = response.css('div.product-details > div > ::text').extract()

        # Parse Colors
        color_links = [response.urljoin(link) for link in
                       response.css('ul.swatches.color li.selectable a::attr(href)').extract()]

        yield self.item_or_request({'product': product, 'color_links': color_links})

    def parse_color(self, response):
        if not re.findall('\d{12}', response.url):
            return

        product = response.meta['product']
        size_links = []
        key = 'size' if response.css('.size').extract() else 'shoeSize'
        # Check if there are sizes of the product or not
        for size in response.css('.{} li.selectable'.format(key)):
            size_url = size.css('a::attr(href)').extract_first()

            if not size.css('.selected'):
                size_links.append(response.urljoin(size_url))
                continue

            size_data = response.css('::attr(data-attributes)').extract_first()
            size_data = json.loads(size_data)
            size_code = size_data[key]['value']
            params = {
                'dwvar_{}_{}'.format(product['retailer_sku'], key): size_code
            }
            url_query = dict(parse_qsl(urlparse(size_url).query))
            url_query.update(params)
            size_url = urlparse(size_url)._replace(query=urlencode(url_query)).geturl()
            size_links.append(size_url)

        if not size_links:
            size_item = self.fill_size_item(response, 0)
            color_id = re.findall('\d{6}', response.css('li.selected a::attr(href)').extract_first())[1]
            product['skus'].update({color_id: size_item})

        product['image_urls'].append(response.css('img.productthumbnail::attr(src)').extract())
        response.meta.update({'size_links': size_links})

        yield self.item_or_request(response.meta)

    def parse_size(self, response):
        product = response.meta['product']
        # Create Unique Key (Combining 'PID_Size') for every Product Size
        key = 'size' if 'size' in response.url else 'shoeSize'
        url_query = dict(parse_qsl(urlparse(response.url).query))
        color_key = 'dwvar_{}_{}'.format(product['retailer_sku'], 'color')
        size_key = 'dwvar_{}_{}'.format(product['retailer_sku'], key)
        color_id = url_query[color_key]
        size_id = url_query[size_key]
        sku_code = '{}_{}'.format(color_id, size_id)

        # Populating attributes of Size Item
        size_item = self.fill_size_item(response, size_id)

        product['skus'].update({sku_code: size_item})

        yield self.item_or_request(response.meta)

    def fill_size_item(self, response, size_id):
        size_item = SizeItem()
        size_item['size_id'] = size_id
        size_item['size_name'] = response.css(
            'li.selected a.js-color-link::text').extract_first('One Size').strip('\n')
        size_item['color'] = response.css('div.label span.selected-value::text').extract_first()
        size_item['stock'] = 1
        size_item['full_price'] = response.css('span.price-sales::text').extract_first().strip('\n')
        size_item['sale_price'] = response.css('span.price-standard::text').extract_first(
                                                                                size_item['full_price']).strip('\n')
        return size_item

    def item_or_request(self, res_meta):
        size_links = res_meta.get('size_links')
        color_links = res_meta.get('color_links')
        if size_links:
            link = size_links.pop()
            return scrapy.Request(link, meta=res_meta, callback=self.parse_size)
        if color_links:
            link = color_links.pop()
            return scrapy.Request(link, meta=res_meta, callback=self.parse_color)
        return res_meta['product']

