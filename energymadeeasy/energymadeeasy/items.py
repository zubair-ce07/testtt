# -*- coding: utf-8 -*-

# Define here the models for your scraped items


import scrapy


class EnergymadeeasyItem(scrapy.Item):
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
    demand_usage_rate = scrapy.Field()

    # SELF INSERTED

    raw_controlled_loads = scrapy.Field()
    energy_plan = scrapy.Field()
    raw_usage_rates = scrapy.Field()
    raw_restrictions = scrapy.Field()
    raw_discount_and_incentives = scrapy.Field()
