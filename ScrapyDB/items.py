
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class StackItem(Item):
    product_url = Field()  #   str: URL of the currency product
    store_keeping_unit = Field()  #   str: unique ID that might be used in database of the website
    title = Field()  #   str: Title of the product
    brand = Field()  #   str: Brand of the product (site name if brand not given explicitly)
    description = Field()  #   list: List of strings in normalized form
    locale = Field()  #   str: language and country e.g; en_GB, en_US, en_PK
    currency = Field()  #   str: currency code of the selected locale. e.g; USD, PKR etc.
    variations = Field()  #   dict: { <slugified_color_name>: <List of Variation Items> ... }


class VariationItem(Item):
    display_color_name = Field() # str: Color name/code if available on the site, Blank otherwise
    image_urls = Field()			# list: List of image URL's of this color
    sizes = Field()			# list: <List of Size Items>

class SizeItem(Item):
    size_name = Field()			# str:	Size name displayed on the website
    is_available = Field()	# bool:	True if product is available for sale, False otherwise
    price = Field() # str:	Price of the product for this size (Without Discount)
    is_discounted = Field()		# bool:	True if product is on sale, False otherwise
    discounted_price = Field() 	# str:	Discounted Price of the product for this size, Blank if not discounted

