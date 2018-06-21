# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class PropertyscraperItem(Item):
    property_name = Field()
    street_address_1 = Field()
    street_address_2 = Field()
    city = Field()
    postcode = Field()
    area = Field()
    area_info = Field()
    website = Field()
    furnished = Field()
    bills_included = Field()
    property_type = Field()
    move_in_date = Field()
    move_out_date = Field()
    deposit_amount = Field()
    property_amenities = Field()
    property_images = Field()
    property_description = Field()
    room_images = Field()
    room_name = Field()
    room_availability = Field()
    property_contact_name = Field()
    property_contact_email = Field()
    property_contact_number = Field()
    discounts = Field()
    room_price = Field()
    floor_plans = Field()
    deposit_name = Field()
    deposit_type = Field()
    room_amenities = Field()
    property_ad_link = Field()
    agent_fees = Field()
    agent_fees_amount = Field()


