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

    @staticmethod
    def strip(value):
        return value[0].strip()


class ZomatoParser(scrapy.Spider):
    name = "zomato"

    special_categories = ['EveryDay Value Offers', 'Bestsellers']

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        # 'COOKIES_ENABLED': False,
        'COOKIES_DEBUG': True,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/63.0'
    }

    def start_requests(self):
        form_inputs = [
            # Commercial Street BGL
            # KFC
            {
                'res_id': '51824',
                'case': 'getdata'
            },
            # Domino
            {
                'res_id': '51659',
                'case': 'getdata'
            },
            # MAC
            # Burger King
            {
                'res_id': '18088641',
                'case': 'getdata'
            },
            # Velachery, Chennai
            # KFC
            {
                'res_id': '65283',
                'case': 'getdata'
            },
            # Domino
            {
                'res_id': '71522',
                'case': 'getdata'
            },
            # MAC
            {
                'res_id': '65345',
                'case': 'getdata'
            },
            # Burger King
            {
                'res_id': '18225860',
                'case': 'getdata'
            },
            # Mylapore, Chennai
            # KFC
            {
                'res_id': '65287',
                'case': 'getdata'
            },
            # Domino
            {
                'res_id': '71594',
                'case': 'getdata'
            },
            # MAC
            {
                'res_id': '18387727',
                'case': 'getdata'
            },
            # Burger King
            {
                'res_id': '73090',
                'case': 'getdata'
            }
        ]

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

        for form_data in form_inputs:
            yield scrapy.FormRequest('https://www.zomato.com/php/o2_handler.php',
                                     formdata=form_data,
                                     callback=self.parse, headers=headers)

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
            'date_of_crawl': self.fetch_date_of_crawl(),
            'search_pincode': response.meta['location'].pincode
        }

        for menu in raw_restaurant['menus']:
            for category in menu['menu']['categories']:
                for product in category['category']['items']:
                    if category['category']['name'] in self.special_categories:
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
                    else:
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
                    if size:
                        self.get_item_variants(item, '|'.join([size, item['item']['name']]), items)
                    else:
                        self.get_item_variants(item, item['item']['name'], items)
            else:
                item = group['group']['items'][0]

                if size:
                    self.get_item_variants(item, '', items)
                else:
                    self.get_item_variants(item, '', items)

        return items


class ZomatoCrawler(scrapy.Spider):
    name = "zomato_crawl"
    parser = ZomatoParser()
    Location = namedtuple('Location', ['city', 'pincode'])

    custom_settings = {
        'DOWNLOAD_DELAY': 1.25,
        # 'COOKIES_ENABLED': False,
        # 'COOKIES_DEBUG': True,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
    }

    start_urls = ['https://www.zomato.com/']

    def start_requests(self):
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

        yield scrapy.Request('https://www.zomato.com/php/o2_handler.php', callback=self.parse,
                             headers=headers, method='POST')

    def parse(self, response):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        locations = self.read('locations.csv')

        for location in locations:
            url = 'https://www.zomato.com/php/liveSuggest.php?q={}&type=locality'.format(
                location.city)
            request = scrapy.Request(url, callback=self.parse_location, headers=headers)
            request.meta['location'] = location
            yield request

    def parse_location(self, response):
        location_type = re.findall(r'data-entity_type=\\"(.+?)\\"', response.text)[0]
        location_id = re.findall(r'data-entity_id=\\"(\d+)\\"', response.text)[0]

        restaurants = ['Burger King', 'KFC', "Domino's Pizza", "Mc'Donalds"]

        for restaurant in restaurants:
            url = 'https://www.zomato.com/php/liveSuggest.php?type=keyword&q={}&entity_id={}' \
                  '&entity_type={}'.format(restaurant, location_id, location_type)
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

        for restaurant_id in raw_listing['results']:
            form_data = {
                'res_id': restaurant_id,
                'case': 'getdata'
            }

            request = scrapy.FormRequest('https://www.zomato.com/php/o2_handler.php',
                                         formdata=form_data,
                                         callback=self.parser.parse, headers=headers)
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
