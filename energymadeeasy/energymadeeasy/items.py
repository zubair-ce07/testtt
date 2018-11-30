# -*- coding: utf-8 -*-

# Define here the models for your scraped items


import scrapy


class EnergymadeeasyItem(scrapy.Item):
    source = scrapy.Field()
    id = scrapy.Field()
    energy_plan = scrapy.Field()
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
    solar_meter_fee = scrapy.Field()
    guaranteed_discount_off_usage = scrapy.Field()
    pot_discount_off_usage = scrapy.Field()
    pot_discount_off_bill = scrapy.Field()
    incentive_type = scrapy.Field()
    approx_incentive_value = scrapy.Field()
    other_incentives = scrapy.Field()
    restricted_eligibility = scrapy.Field()
    guaranteed_discount_off_bill = scrapy.Field()
    fit = scrapy.Field()
    dd_discount_off_bill = scrapy.Field()
    dd_discount_off_usage = scrapy.Field()
    dual_fuel_discount_off_bill = scrapy.Field()
    dual_fuel_discount_off_usage = scrapy.Field()
    db = scrapy.Field()
    minimum_monthly_demand_charged = scrapy.Field()
    raw_usage_rates = scrapy.Field()
    raw_discount_and_incentives = scrapy.Field()
    raw_restrictions = scrapy.Field()
    block_type = scrapy.Field()
    controlled_loads = scrapy.Field()
