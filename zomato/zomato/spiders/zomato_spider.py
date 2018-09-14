import logging
import json
import datetime
from collections import namedtuple
import csv
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class Item(scrapy.Item):
    source = scrapy.Field()
    url = scrapy.Field()
    restaurant = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    category_description = scrapy.Field()
    subcategory_description = scrapy.Field()
    special_category = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    size = scrapy.Field()
    veg = scrapy.Field()
    price = scrapy.Field()
    discounted_price = scrapy.Field()
    store_id = scrapy.Field()
    pincode = scrapy.Field()
    locality = scrapy.Field()
    city = scrapy.Field()
    sku = scrapy.Field()
    thumbnail = scrapy.Field()
    date_of_crawl = scrapy.Field()
    promotion = scrapy.Field()
    offer = scrapy.Field()
    average_rating = scrapy.Field()
    num_of_ratings = scrapy.Field()
    min_order = scrapy.Field()
    search_pincode = scrapy.Field()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ZomatoParser(scrapy.Spider):
    name = "zomato_parse"
    special_categories = ['EveryDay Value Offers', 'Bestsellers']

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/63.0'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.zomato.com/',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.zomato.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    def start_requests(self):
        form_data = {
            'res_id': '51824',
            'case': 'getdata'
        }

        yield scrapy.FormRequest('https://www.zomato.com/php/o2_handler.php',
                                 formdata=form_data,
                                 callback=self.parse, headers=self.headers)

    def parse(self, response):
        raw_restaurant = json.loads(response.text)

        common_fields = {
            'source': 'zomato.com',
            'url': raw_restaurant['restaurant']['url'],
            'restaurant': raw_restaurant['restaurant']['name'],
            'store_id': raw_restaurant['restaurant']['id'],
            'pincode': self.get_restaurant_pincode(raw_restaurant),
            'locality': raw_restaurant['restaurant']['location']['locality'],
            'city': raw_restaurant['restaurant']['location']['city'],
            'min_order': raw_restaurant['minOrder'],
            'average_rating': raw_restaurant['restaurant']['userRating']['aggregate_rating'],
            'num_of_ratings': raw_restaurant['restaurant']['userRating']['votes'],
            'date_of_crawl': self.fetch_date_of_crawl()
        }

        if response.meta.get('location'):
            common_fields['search_pincode'] = response.meta['location'].pincode

        for menu in raw_restaurant['menus']:
            for category in menu['menu']['categories']:
                for product in category['category']['items']:
                    if category['category']['name'] in self.special_categories:
                        special_items = self.generate_special_items(menu, product, common_fields)
                        yield from (item for item in special_items)
                    else:
                        items = self.generate_items(menu, product, common_fields, category)
                        yield from (item for item in items)

    def generate_items(self, menu, product, common_fields, category):
        item_fields = {
            'category': menu['menu']['name'],
            'subcategory': category['category']['name'],
            'title': product['item']['name'],
            'description': product['item']['desc'],
            'special_category': self.check_special_category(menu['menu']['name'])
        }

        variants = self.get_item_variants(product, '', [])

        for variant in variants:
            item = ProductLoader(item=Item())

            item.add_value('size', variant['size'])
            item.add_value('price', variant['price'])
            item.add_value('veg', self.check_veg(product))

            for field in common_fields.keys():
                item.add_value(field, common_fields[field])

            for field in item_fields.keys():
                item.add_value(field, item_fields[field])

            yield item.load_item()

    def generate_special_items(self, menu, product, common_fields):
        item_fields = {
            'category': menu['menu']['name'],
            'subcategory': product['item']['name'],
            'description': product['item']['desc'],
            'sku': product['item']['id'],
            'special_category': 'Y'
        }

        variants = self.get_item_variants(product, '', [])

        for variant in variants:
            item = ProductLoader(item=Item())

            item.add_value('title', variant['name'])
            item.add_value('price', variant['price'])
            item.add_value('veg', self.check_veg(product))

            for field in common_fields.keys():
                item.add_value(field, common_fields[field])

            for field in item_fields.keys():
                item.add_value(field, item_fields[field])

            yield item.load_item()

    @staticmethod
    def get_restaurant_pincode(raw_restaurant):
        pincode = raw_restaurant['restaurant']['location'].get('zipcode')

        if pincode and pincode != '0':
            return pincode

    @staticmethod
    def check_veg(item):
        if not item['item'].get('item_tag_image'):
            return

        return 'non_veg' not in item['item']['item_tag_image']

    def check_special_category(self, value):
        return 'Y' if value in self.special_categories else 'N'

    @staticmethod
    def fetch_date_of_crawl():
        return datetime.datetime.now().strftime('%d %b %Y')

    def get_item_variants(self, product, size, items):
        if not product['item'].get('groups') or product['item']['price']:
            items.append({
                'size': size,
                'price': product['item']['price'],
                'name': product['item']['name']
            })

            return items

        for group in product['item']['groups']:
            if group['group']['name'] in ['Sizes', 'Choose a type']:
                for item in group['group']['items']:
                    self.get_item_variants(item, item['item']['name'], items)
            else:
                item = group['group']['items'][0]
                self.get_item_variants(item, '', items)

        return items


class ZomatoCrawler(scrapy.Spider):
    name = "zomato"
    parser = ZomatoParser()
    Location = namedtuple('Location', ['city', 'pincode'])

    custom_settings = {
        'DOWNLOAD_DELAY': 1.25,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
    }

    def start_requests(self):
        yield scrapy.Request('https://www.zomato.com/php/o2_handler.php', callback=self.parse,
                             headers=self.parser.headers, method='POST')

    def parse(self, response):
        locations = self.read('locations.csv')

        for location in locations:
            url = 'https://www.zomato.com/php/liveSuggest.php?q={}&type=locality'.format(
                location.city)
            request = scrapy.Request(url, callback=self.parse_location)
            request.meta['location'] = location
            yield request

    def parse_location(self, response):
        location_type = re.findall(r'data-entity_type=\\"(.+?)\\"', response.text)
        location_id = re.findall(r'data-entity_id=\\"(\d+)\\"', response.text)

        restaurants = ['Burger King', 'KFC', "Domino's Pizza", "Mc'Donalds"]

        if not location_type:
            logging.warning(response.meta['location'].city)
            logging.warning('NO LOCATION FOUND')
            logging.warning(response.text)
            return

        for restaurant in restaurants:
            url = 'https://www.zomato.com/php/liveSuggest.php?type=keyword&q={}&entity_id={}' \
                  '&entity_type={}'.format(restaurant, location_id[0], location_type[0])
            request = scrapy.Request(url, callback=self.parse_chains)
            request.meta['location'] = response.meta['location']
            yield request

    def parse_chains(self, response):
        restaurant_chains = response.xpath(
            '//a[contains(@data-entity-type, "chain")]/@data-entity-id').extract()
        for restaurant_chain in restaurant_chains:
            url = 'https://www.zomato.com/index.php?chain={}'.format(restaurant_chain.strip('\\"'))
            request = scrapy.Request(url, callback=self.parse_listing)
            request.meta['location'] = response.meta['location']
            yield request

    def parse_listing(self, response):
        raw_listing = response.xpath('//script[contains(text(), "search_results")]').re(r'{.+}')[0]
        raw_listing = json.loads(raw_listing)

        for restaurant_id in raw_listing['results']:
            form_data = {
                'res_id': restaurant_id,
                'case': 'getdata'
            }

            request = scrapy.FormRequest('https://www.zomato.com/php/o2_handler.php',
                                         formdata=form_data,
                                         callback=self.parser.parse, headers=self.parser.headers)
            request.meta['location'] = response.meta['location']
            yield request

        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page:
            request = response.follow(next_page, callback=self.parse_listing)
            request.meta['location'] = response.meta['location']
            yield request

    @staticmethod
    def is_valid_reading(reading):
        required_fields = ['City', 'Postal Code']
        return all(reading[field] for field in required_fields)

    def read(self, file_name):
        with open(file_name, 'r') as f:
            return [self.Location(r['City'], r['Postal Code']) for r in
                    csv.DictReader(f) if self.is_valid_reading(r)]
