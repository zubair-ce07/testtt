import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity


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


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    @staticmethod
    def strip(value):
        return value[0].strip()

    categories_out = Identity()
    description_out = strip


class FoodPandaParser(scrapy.Spider):
    name = "foodpanda"

    start_urls = ['https://www.foodpanda.in/location-suggestions?cityId=462546&'
                  'area=Jayanagar+6th+Block+(Jaya+Nagar)&area_id=464687&'
                  'pickup=&sort=&tracking_id=a0422341806e4a8eba1b4f290d03827b']

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        pages = response.xpath('//*[contains(@class, "js-pagination")]//'
                               '*[contains(@class, "infscroll-page")]/@value').extract()

        for page in pages:
            yield scrapy.Request(f'https://www.foodpanda.in/restaurants?user_search='
                                 f'&sort=&sort=&page={page}', callback=self.parse_listing)

    def parse_listing(self, response):
        product_urls = response.xpath('//a[contains(@class, "vendor")][descendant-or-self::'
                                      '*[contains(.,"Domino\'s") or contains(.,"KFC") or'
                                      ' contains(.,"McDonald\'s") or contains(.,"Burger King")]]'
                                      '//@href').extract()
        
        for url in product_urls:
            yield response.follow(url, callback=self.parse_product)

    def parse_product(self, response):
        common_fields = {
            'restaurant': response.css('.vendor__title [itemprop="name"]::text').extract_first(),
            'url': response.url, 'source': 'foodpanda.in',
            'average_rating': self.fetch_average_rating(response),
            'num_of_ratings': self.fetch_num_of_ratings(response),
            'store_id': re.findall(r'foodpanda\.in/restaurant/(.*)/', response.url),
            'date_of_crawl': datetime.datetime.now().strftime('%d %b %Y'),
            'min_order': response.xpath('//script[contains(text(), "minimum_order")]').re(
                '"minimum_order_amount":(\d+)') or None,
            'locality': ', '.join(response.css(
                '.vendor-info__address__content span::text').extract()),
            'pincode': response.css('*[itemprop="postalCode"]::text').extract_first(),
            'city': response.css('*[itemprop="addressRegion"]::text').extract_first()
        }

        items = self.fetch_items(common_fields, response)

        for item in items:
            yield item.load_item()

    def fetch_items(self, common_fields, response):
        items = []
        raw_categories = response.css('.menu__category')

        for raw_category in raw_categories:
            category_title = raw_category.css('.menu__category__title::text')\
                             .extract_first().strip()
            special_category = self.check_special_category(category_title)

            if special_category and "Domino's" in common_fields['restaurant']:
                raw_sub_categories = raw_category.css('.menu__category > [class^="menu-item"]')

                for raw_sub_category in raw_sub_categories:
                    item = ProductLoader(item=Item(), response=response)
                    item.add_value('category', category_title)
                    item.add_value('special_category', 'Y' if special_category else 'N')
                    item.add_value('subcategory', raw_sub_category.css(
                        '.menu-item__title::attr(title)').extract_first())
                    item.add_value('subcategory_description', raw_sub_category.css(
                        '.menu-item__title::attr(title)').extract_first())
                    item.add_value('thumbnail', raw_sub_category.css(
                        '.menu-item__image img::attr(data-src)').re(r'(https://.+)\?'))

                    for field in common_fields.keys():
                        item.add_value(field, common_fields[field])

                    items.append(item)
            else:
                raw_items = raw_category.css('.menu__category > [class^="menu-item"]')

                for raw_item in raw_items:
                    raw_sizes = raw_item.css('.menu-item__variation')

                    for raw_size in raw_sizes:
                        item = ProductLoader(item=Item(), response=response)

                        item.add_value('title', raw_item.css(
                            '.menu-item__title::attr(title)').extract_first())
                        item.add_value('description', raw_item.css(
                            '.menu-item__description::text').extract_first())
                        item.add_value('price', raw_item.css(
                            '[class^="menu-item__variation__price"]::text').extract_first().strip())
                        item.add_value('category', category_title)
                        item.add_value('subcategory', category_title)
                        item.add_value('special_category', 'Y' if special_category else 'N')
                        item.add_value('thumbnail', raw_item.css(
                            '.menu-item__image img::attr(data-src)').re(r'(https://.+)\?'))
                        item.add_value('sku', raw_size.css(
                            '.menu-item__variation::attr(data-clicked_product_id)')
                                       .extract_first().strip())
                        item.add_value('size', self.fetch_size(raw_size.css(
                            '.menu-item__variation__title::text').extract_first().strip()))
                        veg_title = raw_item.css('.menu-item__dish-characteristics '
                                                 'span::attr(data-title)').extract_first() or ''
                        item.add_value('veg', self.fetch_veg(
                            [item.get_output_value('category'), item.get_output_value('title'),
                             veg_title]
                        ))
                        item.add_value(
                            'promotion', True if raw_item.css('.popular-dish') else False)

                        for field in common_fields.keys():
                            item.add_value(field, common_fields[field])

                        items.append(item)

        return items

    @staticmethod
    def check_special_category(category_title):
        offers = ['Value Offers', 'Trending Now']
        return any(offer in category_title for offer in offers)

    @staticmethod
    def fetch_size(size_title):
        size_map = ['Medium', 'Small', 'Regular', 'Large']

        if not size_title:
            return

        for size in size_map:
            if size in size_title:
                return size

        return size_title

    @staticmethod
    def fetch_veg(titles):
        non_veg_re = re.compile(r'((non[ \-]veg)|(chicken))', flags=re.I)

        if any(non_veg_re.findall(title) for title in titles):
            return False

        return True

    @staticmethod
    def fetch_num_of_ratings(response):
        ratings = response.css('.review [itemprop="ratingCount"]::text')
        return ratings.extract() if ratings else '0'

    @staticmethod
    def fetch_average_rating(response):
        full_stars = len(response.css('.vendor__ratings .active-star.icon-star-ratings-full'))
        half_stars = len(response.css('.vendor__ratings .active-star.icon-star-ratings-half'))

        return float(full_stars) + float(half_stars) * 0.5
