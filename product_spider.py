import itertools
import lxml.etree
import re
import ast
from urllib.parse import urlparse
from datetime import datetime

import scrapy
import js2xml
import ccy
from parsel import Selector


class ProductSpider(scrapy.Spider):
    name = 'product'

    start_urls = [
        'https://www.jacklemkus.com/',
        # 'https://www.jacklemkus.com/mens-apparel/t-shirts',
        # 'https://www.jacklemkus.com/accessories/sneaker-cleaner/crep-ultimate-pack',
        # 'https://www.jacklemkus.com/apparel/clrdo-og-sweats-borang',
    ]

    def parse(self, response):
        categories = response.css('#nav li a:nth-child(2)::attr("href")').getall()
        for category in categories:
            yield response.follow(category, self.parse_product_grid)

    def parse_product_grid(self, response):
        product_links = response.css('#products-grid .product-image::attr("href")').getall()

        if len(product_links) == 16:
            url = response.url.split('?p=')
            yield response.follow(f'?p={2 if len(url) == 1 else int(url[1]) + 1}', self.parse_product_grid)

        for product_link in product_links:
            yield response.follow(product_link, self.parse_product)

    def parse_product(self, response):
        retailer_sku = response.css('span.sku::text').get().strip()

        trail_anchors = response.css('#breadcrumbs li a')
        trail = [[trail_anchor.css('::text').get().strip(), trail_anchor.css('::attr("href")').get().strip()]
                 for trail_anchor in trail_anchors]

        url = response.css('head link[rel="canonical"]::attr("href")').get()

        date = response.headers["Date"].decode('utf-8')
        date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT').strftime('%Y-%m-%dT%H:%M:%S.%f')

        category = [t[0] for t in itertools.islice(trail, 1, None)]

        url_original = response.url

        product_name = response.css('div.product-name h1::text').get().strip()

        gender = None
        brand = None
        description = []
        care = []
        care_words = {'synthetic', 'composition'}
        # all text present in description tab and its descendants
        description_tab_data = response.css('#description-tab .std *::text').getall()
        for data in description_tab_data:
            data = data.strip()
            if data != '':
                description.append(data)
                for care_word in care_words:
                    if care_word in data:
                        care.append(data)
                        break
        for tr in response.css('#product-attribute-specs-table tr'):
            entry_id = tr.css('th::text').get().strip()
            entry_value = tr.css('td::text').get().strip()
            description.append(entry_id)
            description.append(entry_value)
            if entry_id == 'Gender':
                gender = re.split(r'[\\ \']', entry_value)[0]
                # gender = entry_value.split()[0]
            elif entry_id == 'Item Brand':
                brand = entry_value

        image_urls = response.css('li.span1 img::attr("src")').getall()

        price = response.css('.regular-price .price::text').get()

        javascript = response.css('#search_mini_form > div > script::text').get()
        xml = lxml.etree.tostring(js2xml.parse(javascript), encoding='utf-8').decode('utf-8')
        selector = Selector(text=xml)
        currency = selector.css('property[name="currencycode"] string::text').get()

        market = ccy.currency(currency).default_country

        retailer = f'{urlparse(response.url).netloc.split(".")[1]}-{market.lower()}'

        product_data = ast.literal_eval(response.css('div.product-data-mine::attr("data-lookup")').get())
        skus = [{'price': price, 'currency': currency, 'size': data.get('size'), 'out_of_stock': True,
                 'sku_id': data.get('id')} if data['stock_status'] == 0
                else {'price': price, 'currency': currency, 'size': data.get('size'),
                      'sku_id': data.get('id')}
                for data in product_data.values()]

        crawl_start_time = self.crawler.stats._stats['start_time'].strftime('%Y-%m-%dT%H:%M:%S.%f')

        yield {
            'retailer_sku': retailer_sku,
            'trail': trail,
            'gender': gender,
            'category': category,
            'brand': brand,
            'url': url,
            'date': date,
            'market': market,
            'retailer': retailer,
            'url_original': url_original,
            'name': product_name,
            'description': description,
            'care': care,
            'image_urls': image_urls,
            'skus': skus,
            'price': price,
            'currency': currency,
            'spider_name': ProductSpider.name,
            'crawl_start_time': crawl_start_time
        }
