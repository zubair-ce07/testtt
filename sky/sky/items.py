# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SkyItem(scrapy.Item):
    product_id = scrapy.Field()
    inbound_departure_date = scrapy.Field()
    inbound_arrival_date = scrapy.Field()
    outbound_departure_date = scrapy.Field()
    outbound_arrival_date = scrapy.Field()
    outbound_Bundle = scrapy.Field()
    price_outbound = scrapy.Field()
    price_inbound = scrapy.Field()
    inbound_bundle = scrapy.Field()
    observation_date = scrapy.Field()
    observation_time = scrapy.Field()
    origin = scrapy.Field()
    destination = scrapy.Field()
    OD = scrapy.Field()
    OneWayIndicator = scrapy.Field(type=bool)
    carrier = scrapy.Field()
    OutboundFlightNumber = scrapy.Field()
    InboundFlightNumber = scrapy.Field()
    InboundFareBasis = scrapy.Field()
    OutboundFareBasis = scrapy.Field()
    outbound_booking_class = scrapy.Field()
    inbound_booking_class = scrapy.Field()
    price_exc = scrapy.Field()
    price_inc = scrapy.Field()
    Tax = scrapy.Field()
    currency = scrapy.Field()
    is_tax_inc_outin = scrapy.Field(type=bool)