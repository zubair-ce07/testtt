# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity

def _clean_in(self, values):
    return [value.strip("\n ") if type(value) == str else value for value in values]

# def _option(self, values):
#     for value in values:
#         if "yes" in value.lower():
#             return ["y"]
#         elif "no" in value.lower():
#             return ["n"]
        
class CompareItem(scrapy.Item):
    source = scrapy.Field()
    id = scrapy.Field()
    timestamp = scrapy.Field()
    effective_from = scrapy.Field()
    retailer = scrapy.Field()
    name = scrapy.Field()
    supply = scrapy.Field()
    peak_rate = scrapy.Field()
    shoulder = scrapy.Field()
    off_peak_rate = scrapy.Field()
    green = scrapy.Field()
    green_note = scrapy.Field()
    etf = scrapy.Field()
    contract_length = scrapy.Field()
    meter_type = scrapy.Field()
    solar = scrapy.Field()
    solar_meter_fee = scrapy.Field()##
    guaranteed_discount_off_usage = scrapy.Field() #Written in a paragraph and same location as guaranteed_discount_off_bill
    pot_discount_off_usage = scrapy.Field() #Written in a paragraph and same location as pot_discount_off_bill
    pot_discount_off_bill = scrapy.Field() #Written in a paragraph and same location as pot_discount_off_usage
    incentive_type = scrapy.Field()# same as other incentives as they come in same place
    approx_incentive_value = scrapy.Field()# complete paragraph as the $ value come inside of paragraph
    other_incentives = scrapy.Field()# same as incentive type as they come in same place
    restricted_eligibility = scrapy.Field()##
    guaranteed_discount_off_bill = scrapy.Field()#Written in a paragraph and same location as guaranteed_discount_off_usage
    fit = scrapy.Field()
    dd_discount_off_bill = scrapy.Field()#Written in a paragraph and same location as dd_discount_off_usage
    dd_discount_off_usage = scrapy.Field()#Written in a paragraph and same location as dd_discount_off_bill
    dual_fuel_discount_off_bill = scrapy.Field()#Written in a line and same location as dual_fuel_discount_off_usage
    dual_fuel_discount_off_usage = scrapy.Field()#Written in a line and same location as dual_fuel_discount_off_bill
    db = scrapy.Field()
    minimum_monthly_demand_charged = scrapy.Field()#

class CompareItemLoader(ItemLoader):
    default_item_class = CompareItem
    default_output_processor = TakeFirst()
    default_input_processor = _clean_in

    incentive_type_out = Identity()
    approx_incentive_value_out = Identity()
    other_incentives_out = Identity()
