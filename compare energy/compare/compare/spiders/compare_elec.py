# -*- coding: utf-8 -*-
import json
import csv
import datetime

import scrapy
from scrapy.shell import inspect_response

from ..items import CompareItemLoader

class CompareElecSpider(scrapy.Spider):

    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,
        "FEED_EXPORT_ENCODING": "utf-8"
    }

    filename = "electricity.csv"
    name = 'compare_elec_electricity'
    allowed_domains = ['compare.energy.vic.gov.au']
    start_urls = ['http://compare.energy.vic.gov.au/']

    electricity_distributor_map = {
        "United Energy": "18",
        "AusNet": "17",
        "CitiPower": "7",
        "Jemena": "14",
        "Powercor": "16"
    }
    gas_distributor_map = {
        "Ausnet": "20",
        "Australian Gas Networks": "19",
        "Multinet Gas": "21",
        "Enwave": "22"
    }
    distributor_zone = {
        "Bairnsdale": "8",
        "North": "9",
        "Mildura": "10",
        "Murry": "11",
        "Central": "12",
        "Adjoining Central": "13",
        "Adjoining West": "14",
        "Central": "15",
        "West": "16",
        "Yarra Valley Extension": "17",
        "South Gippsland Extension": "18",
        "Melbourne Metropolitan Area": "19",
    }

    def start_requests(self):
        requests = []
        url = "http://compare.energy.vic.gov.au/"
        with open(self.filename, 'r') as f:
            locations = list(csv.DictReader(f))
        
        for jar_index, location in enumerate(locations):
            if location["type"] == "electricity":
                if self.electricity_distributor_map.get(location["distributor"]):
                    requests.append(scrapy.Request(url=url, meta={
                        "type": location["type"],
                        "distributor": self.electricity_distributor_map[location["distributor"]],
                        "postcode": location["postal_code"],
                        "cookiejar": jar_index
                    },
                    callback=self.parse, dont_filter=True))
            elif location["type"] == "gas":
                if self.gas_distributor_map.get(location["distributor"]) and self.distributor_zone.get(location["zone"]):
                    requests.append(scrapy.Request(url=url, meta={
                        "type": location["type"],
                        "distributor": self.gas_distributor_map[location["distributor"]],
                        "zone": self.distributor_zone[location["zone"]],
                        "postcode": location["postal_code"],
                        "cookiejar": jar_index
                    },
                    callback=self.parse, dont_filter=True))
        
        return requests

    def parse(self, response):
        form_data = {
            "energy_category": response.meta["type"],
            "location": "home",
            "location-home": "shift",
            "postcode": response.meta["postcode"],
            "distributor": response.meta["distributor"],
            "energy_concession": "0",
            "solar": "0",
            "disclaimer_chkbox": "disclaimer_selected"
        }
        if response.meta["type"] == "gas":
            form_data["zone"] = response.meta["zone"]
        
            
        yield scrapy.FormRequest.from_response(response=response, formid="welcome_form", 
        formdata=form_data, callback=self.parse_questions, meta=response.meta, dont_filter=True)

    def parse_questions(self, response):
        form_data={
            "person-count": "1",
            "room-count": "1",
            "spaceheating[]": "none",
            "cloth-dryer": "0",
            "waterheating[]": "other"
        }
        form_id = "gas_ques_form"
        if response.meta["type"] == "electricity":
            form_data.update({
                "refrigerator-count": "0",
                "gas-type": "4",
                "pool-heating": "0",
                "poolheatingtype[]": "none",
                "spacecooling[]": "none",
                "cloth-dryer-freq-weekday": "",
                "cloth-dryer-freq-weekend": "",
                "control-load": "0"
            })
            form_id = "electric_ques_form"
            
        yield scrapy.FormRequest.from_response(response=response, formid=form_id, 
        formdata=form_data, callback=self.parse_result_page, meta=response.meta, dont_filter=True)

    def parse_result_page(self, response):
        yield scrapy.Request(url="https://compare.energy.vic.gov.au/service/offers",
         callback=self.parse_results, meta=response.meta, dont_filter=True)
    
    def parse_results(self, response):
        all_results = json.loads(response.text)["offersList"]
        for result in all_results:
            key = result["offerDetails"][0]["offerKey"]
            response.meta["offer_json"] = json.dumps(result["offerDetails"][0])
            yield scrapy.Request(url="https://compare.energy.vic.gov.au/modal/offers/{}".format(key),
            callback=self.parse_result, meta=response.meta, dont_filter=True)
    

    def parse_result(self, response):
        offer_data = json.loads(response.meta["offer_json"])
        common_xpath = "//*[contains(text(),'{}')]/../td[2]/text()"
        il = CompareItemLoader(response=response)
        
        il.add_value("energy_plan", response.meta["type"])
        il.add_value("source", response.url)
        il.add_xpath("id", common_xpath.format("Offer ID:"))
        il.add_value("timestamp", str(datetime.datetime.utcnow()))
        il.add_xpath("effective_from", common_xpath.format("Release date:"))
        il.add_css("retailer", "h1::text")
        il.add_css("name", "h1 + p > span::text")
        il.add_css("supply", ".supply-charge .value::text")
        il.add_value("green", "y" if offer_data["greenPower"] else "n")
        il.add_value("green_note", offer_data["greenPower"])
        
        il.add_xpath("contract_length", "//*[contains(@class, 'contract-table')]//"
                                        "td[contains(text(), 'Contract term')]/../td[2]/text()")
        il.add_xpath("meter_type", common_xpath.format("Rate type:"))
        il.add_xpath("solar", common_xpath.format("Avail. to solar customers"))
        il.add_xpath("incentive_type", "//*[contains(text(), 'Incentives')]/../td[2]//i/text()")
        il.add_xpath("other_incentives", "//*[contains(text(), 'Incentives')]/../td[2]//i/text()")
        il.add_xpath("approx_incentive_value", "//*[contains(text(), 'Incentives')]/../td[2]/p/text()")
        il.add_value("etf", "y" if response.xpath("//*[contains(text(), 'Early termination fee')]") else "n")
        il.add_xpath("shoulder", "//*[contains(@class, 'tariff-details')]//p[contains(text(),"
                                 " 'Shoulder')]/../div[contains(@class, 'tariff-separator')]//div[2]/p/strong/text()")
        il.add_xpath("peak_rate", "//*[contains(@class, 'tariff-details')]//p[contains(text(), 'Peak')]"
                                  "/../div[contains(@class, 'tariff-separator')]//div[2]/p/strong/text()")
        
        il.add_xpath("off_peak_rate", "//*[contains(@class, 'tariff-details')]//p[contains(text(), 'Off-peak')]/../div[contains(@class, 'tariff-separator')]//div[2]/p/strong/text()")
        il.add_xpath("fit", "//*[text()='Feed in Tariff']/../../following::div[contains(@class, 'value')]/p/*/text()")
        il.add_xpath("db", common_xpath.format("Distributor:"))
        il.add_xpath("vec_discount_summary", "//*[text()='Discounts:']/../p/strong/text()")
        il.add_xpath("vec_discount_description", "//*[text()='Discounts:']/../p[not(strong)]/text()")
        
        raw_rates = response.xpath("//*[@class='row offer-rate-header']")
        for rate in raw_rates[1:]:
            raw_summary = rate.xpath("descendant-or-self::*[@class]/text()").extract()
            raw_summary = " ".join([text for text in raw_summary if text.strip(" \n")])
            il.add_value("vec_tariff_summary", raw_summary)
        
        raw_rate_details = response.xpath("//*[@class='row tariff-details']")
        for detail in raw_rate_details:
            values = detail.css(".row ::text").extract()
            values = " ".join([text for text in values if text.strip(" \n")])
            il.add_value("vec_tariff_description", values)

        yield il.load_item()

class CompareElecSpiderSecond(CompareElecSpider):

    filename = "gas.csv"
    name = 'compare_elec_gas'
