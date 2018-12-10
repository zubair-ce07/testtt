# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JetsmartItem(scrapy.Item):
    # define the fields for your item here like:
    OD = scrapy.Field()                     #origin+destination
    POS = scrapy.Field()                    #point of sale. Should be Pakistan/PK
    carrier = scrapy.Field()            
    currency = scrapy.Field()
    destination = scrapy.Field()
    inbound_arrival_date = scrapy.Field()
    inbound_departure_date = scrapy.Field()
    inbound_fare_basis = scrapy.Field()
    inbound_flight_number = scrapy.Field()
    inbound_travel_stopover = scrapy.Field()#mid flights stops
    is_tax_inc_outin = scrapy.Field()       #boolean check if tax includes.
    observation_date = scrapy.Field()       #should be in UTC
    observation_time = scrapy.Field()
    oneway_indicator = scrapy.Field()
    origin = scrapy.Field()
    outbound_arrival_date = scrapy.Field()
    outbound_booking_class = scrapy.Field()
    outbound_bundle = scrapy.Field()
    outbound_departure_date = scrapy.Field()
    outbound_fare_basis = scrapy.Field()
    outbound_flight_number = scrapy.Field()
    outbound_travel_stopover = scrapy.Field()
    outbound_travel_duration = scrapy.Field()
    price_exc = scrapy.Field()              #exclude tax
    price_inc = scrapy.Field()              #include tax
    price_inbound = scrapy.Field()
    price_outbound = scrapy.Field()
    site_source = scrapy.Field()
    source = scrapy.Field()
    tax = scrapy.Field()