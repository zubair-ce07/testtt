# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity



def _clean_in(self, values):
    return [re.sub(r'[ \t]+', ' ', val).strip(' \n') for val in values if type(val)==str]

# def _option(self, values):
#     for value in values:
#         if "yes" in value.lower():
#             return ["y"]
#         elif "no" in value.lower():
#             return ["n"]
        
class CompareItem(scrapy.Item):
    id = scrapy.Field()
    timestamp = scrapy.Field()
    db = scrapy.Field()
    meter_type = scrapy.Field()
    effective_from = scrapy.Field()
    solar = scrapy.Field()
    restricted_eligibility = scrapy.Field()
    solar_meter_fee = scrapy.Field()
    retailer = scrapy.Field()
    name = scrapy.Field()
    supply = scrapy.Field()
    peak_rate = scrapy.Field()
    block_type = scrapy.Field()
    peak_step_1 = scrapy.Field()
    peak_rate_2 = scrapy.Field()
    peak_step_2 = scrapy.Field()
    peak_rate_3 = scrapy.Field()
    peak_step_3 = scrapy.Field()
    peak_rate_4 = scrapy.Field()
    off_peak_rate = scrapy.Field()
    shoulder = scrapy.Field()
    minimum_monthly_demand_charged = scrapy.Field()
    fit = scrapy.Field()
    green = scrapy.Field()
    green_note = scrapy.Field()

    guaranteed_discount_off_usage = scrapy.Field()
    guaranteed_discount_off_bill = scrapy.Field()
    pot_discount_off_usage = scrapy.Field()
    pot_discount_off_bill = scrapy.Field()
    dd_discount_off_bill = scrapy.Field()
    dd_discount_off_usage = scrapy.Field()
    e_bill_discount_off_bill = scrapy.Field()
    e_bill_discount_off_usage = scrapy.Field()
    online_signup_discount_off_bill = scrapy.Field()
    online_signup_discount_off_usage = scrapy.Field()
    dual_fuel_discount_off_bill = scrapy.Field()
    dual_fuel_discount_off_usage = scrapy.Field()

    contract_length = scrapy.Field()
    etf = scrapy.Field()
    other_incentives = scrapy.Field()
    incentive_type = scrapy.Field()
    approx_incentive_value = scrapy.Field()
    source = scrapy.Field()

    # ADDED LATER

    single_rate = scrapy.Field()
    controlled_load_1 = scrapy.Field()
    controlled_load_2 = scrapy.Field()
    vec_discount_summary = scrapy.Field()
    vec_discount_description = scrapy.Field()

    # SELF INSERTED

    controlled_loads = scrapy.Field()
    energy_plan = scrapy.Field()
    raw_usage_rates = scrapy.Field()
    raw_restrictions = scrapy.Field()
    raw_discount_and_incentives = scrapy.Field()
    vec_tariff_summary = scrapy.Field()
    vec_tariff_description = scrapy.Field()
    
class CompareItemLoader(ItemLoader):
    default_item_class = CompareItem
    default_output_processor = TakeFirst()
    default_input_processor = _clean_in

    incentive_type_out = Identity()
    approx_incentive_value_out = Identity()
    other_incentives_out = Identity()
    vec_discount_summary_out = Identity()
    vec_discount_description_out = Identity()
    vec_tariff_summary_out = Identity()
    vec_tariff_description_out = Identity()