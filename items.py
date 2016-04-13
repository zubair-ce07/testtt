# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlueflyItem(scrapy.Item):
    # define the fields for your item here like:
    brand = scrapy.Field()
    care = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    market = scrapy.Field()
    merch_info = scrapy.Field()
    name = scrapy.Field()
    retailer = scrapy.Field()
    skus = scrapy.Field()
    retailer_sku = scrapy.Field()
    url = scrapy.Field()
    url_original = scrapy.Field()

    pass

# code {'brand': u'Hayden',
# 'care': [u'Hand Wash or Dry Clean', u'100% Cashmere'],
# 'category': [u'Women', u'Clothing', u'Sweaters', u'Cashmere'],
# 'description': [u'All you need for the fall is a cozy cashmere sweater to keep you warm on those cool nights courtesy of Hayden.',
# u'Hayden',
# u'Lightweight 2-ply 12gg cashmere knit',
# u'Foldover ribbed turtleneck',
# u'Long sleeve',
# u'Ribbed banded cuffs and hem',
# u'Contemporary fit',
# u"27'' from shoulder seam to hem&
# quot;,
#                   u'Approximate measurements taken from a size S, and may vary by size',
#                   u'China',
#                   u'Style # 351480403'],
#   'gender': 'women',
#   'image_urls': [u'//cdn-tp4.mozu.com/12106-m2/cms/files/351480403?maxWidth=1800&maxHeight=2160&v=89';,
#                  u'//cdn-tp4.mozu.com/12106-m2/cms/files/351480403_alt01?maxWidth=&maxHeight=537&v=89';],
#   'market': 'US',
#   'merch_info': [u'Includes An Extra 60% Off'],
#   'name': u'Purple Cashmere Turtleneck Sweater',
#   'retailer': 'bluefly',
#   'retailer_sku': u'351480403',
#   'skus': {u'560': {'colour': u'Purple',
#                     'currency': 'USD',
#                     'previous_prices': [28000],
#                     'price': 3600,
#                     'size': u'XS'},
#            u'562': {'colour': u'Purple',
#                     'currency': 'USD',
#                     'previous_prices': [28000],
#                     'price': 3600,
#                     'size': u'S'},
#            u'564': {'colour': u'Purple',
#                     'currency': 'USD',
#                     'previous_prices': [28000],
#                     'price': 3600,
#                     'size': u'M'},
#            u'566': {'colour': u'Purple',
#                     'currency': 'USD',
#                     'previous_prices': [28000],
#                     'price': 3600,
#                     'size': u'L'}},
#   'url': u'http://www.bluefly.com/hayden-purple-cashmere-turtleneck-sweater/p/351480403';,
#   'url_original': 'http://www.bluefly.com/hayden-purple-cashmere-turtleneck-sweater/p/351480403';}
