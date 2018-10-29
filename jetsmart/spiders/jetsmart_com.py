# -*- coding: utf-8 -*-

from parsel import Selector
from datetime import datetime, timedelta
from jetsmart.items import JetsmartItem
import scrapy


class JetsmartComSpider(scrapy.Spider):
    name = 'jetsmart.com'
    # allowed_domains = ['jetsmart.com/cl/es']
    start_urls = ['http://jetsmart.com/cl/es/']

    def parse(self, response):
        trips = [
            ["ANF", "SCL"],
            ["SCL", "ANF"],
            ["CJC", "SCL"],
            ["SCL", "CJC"],
            ["PUQ", "SCL"],
            ["SCL", "PUQ"],
            ["SCL", "PMC"],
            ["PMC", "SCL"]
        ]
        for i, route in enumerate(trips):
            yield scrapy.Request("https://booking.jetsmart.com/V2/Flight", self.get_cookie, meta={'cookiejar': i, "route":route}, dont_filter=True)

    def get_cookie(self, response):
        yield scrapy.Request("https://booking.jetsmart.com/V2/Flight", self.parse_flights, meta={"cookiejar": response.meta['cookiejar'], "route":response.meta['route']}, dont_filter=True)

    def parse_flights(self, response):
        today = datetime.now()
        route = response.meta['route']
        date_iterator = today
        date_counter = 1
        while date_counter < 31:
            link = "/Flight/InternalSelect?s=True&o1={}&d1={}&ADT=1&dd1={}&mon=true&cur=CLP".format(route[0], route[1], date_iterator.date(),)
            yield scrapy.Request("https://booking.jetsmart.com/"+link, meta={"cookiejar": response.meta["cookiejar"], "datetime": date_iterator, "route":route, "link":link}, callback=self.parse_flight_data_ow, dont_filter=True)
            date_iterator = today + timedelta(days=date_counter)
            date_counter = date_counter + 1    

        today = datetime.now()
        dd1 = today
        today_counter = 1
        while today_counter < 31:
            date2 = today + timedelta(days=1)
            dd2 = date2
            date_counter = 1
            while date_counter < 31:
                link = "/Flight/InternalSelect?s=True&o1={}&d1={}&ADT=1&dd1={}&dd2={}&r=true&mon=true&cur=CLP".format(route[0], route[1], dd1, dd2)
                yield scrapy.Request("https://booking.jetsmart.com/"+link, meta={"cookiejar": response.meta["cookiejar"], "dd1": dd1, "dd2": dd2, "route":route, "link":link}, callback=self.parse_flight_data_tw, dont_filter=True)
                dd2 = date2 + timedelta(days=date_counter)
                date_counter += 1

            dd1 = today + timedelta(days=1)
            today_counter += 1            
        
    def parse_flight_data_ow(self, response):
        date_iterator = response.meta['datetime']
        route = response.meta['route']
        flight_list = response.xpath("//flight-fee-selector")
        if not(flight_list):
            link = response.meta["link"]
            yield scrapy.Request("https://booking.jetsmart.com/"+link, meta={"cookiejar": response.meta["cookiejar"], "datetime": date_iterator, "route":route, "link":link}, callback=self.parse_flight_data_ow, dont_filter=True)
        
        flight_list = flight_list.xpath("//flight-fee[@trip-index='0']").extract()
        if flight_list:
            for flight in flight_list:
                flight = Selector(flight)
                flightItem = JetsmartItem()
                flightItem["OD"] = route[0]+route[1]
                flightItem["POS"] = "PK"
                flightItem["carrier"] = "JA"
                flightItem["currency"] = "CLP"
                flightItem["destination"] = route[1]
                flightItem["observation_date"] = datetime.now().strftime("%Y-%m-%d")
                flightItem["observation_time"] = datetime.now().strftime("%H:%M")
                flightItem["oneway_indicator"] = 1
                flightItem["origin"] = route[0]
                flightItem["outbound_flight_number"] = flight.xpath("//@flight-number").extract_first()
                flightItem["outbound_travel_stopover"] = ""
                departure_hour_minute = flight.xpath("//@departure-time").extract_first().split(":")
                flightItem["outbound_departure_date"] = date_iterator.replace(hour=int(departure_hour_minute[0]), minute=int(departure_hour_minute[1])).strftime("%Y-%m-%d %H:%M")
                arrival_hour_minute = flight.xpath("//@arrival-time").extract_first().split(":")
                departure_datetime = date_iterator.replace(hour=int(departure_hour_minute[0]), minute=int(departure_hour_minute[1]))
                arrival_datetime = date_iterator.replace(hour=int(arrival_hour_minute[0]), minute=int(arrival_hour_minute[1]))
                if arrival_datetime < departure_datetime:
                    arrival_datetime += timedelta(days=1)
                    flightItem["outbound_arrival_date"] = arrival_datetime.strftime("%Y-%m-%d %H:%M")
                else:
                    flightItem["outbound_arrival_date"] = arrival_datetime.strftime("%Y-%m-%d %H:%M")
                flightItem["price_exc"] = flight.xpath("//@discounted-price").extract_first()
                flightItem["price_outbound"] = flightItem["price_exc"]
                flightItem["site_source"] = "JA"
                flightItem["source"] = "Jet Smart"
                sellkey =  flight.xpath("//input/@value").extract()[-1]
                if sellkey:
                    yield scrapy.Request("https://booking.jetsmart.com/V2XHR/PriceBreakdownFlightSelect?cur=CLP&SellKeys[]="+sellkey, self.get_tax_information, meta={"cookiejar": response.meta['cookiejar'], "flight":flightItem, "tries": 1}, dont_filter=True)

    def get_tax_information(self, response):
        flightItem = response.meta['flight']
        final_total = response.xpath("//div[contains(@class, 'total-row')]//div[2]/span/text()").extract_first()
        if final_total is not None:
            flightItem["price_inc"] = final_total
            final_total = float(final_total.strip("$").strip())
            total = float(flightItem["price_exc"].strip("$").strip())
            tax = final_total - total
            flightItem["tax"] = "$ "+str(tax)
            yield flightItem
        elif response.xpath("//div[@class='prices-wrapper']").extract():
            tries = response.meta['tries']
            if tries < 5:
                tries += 1
                yield scrapy.Request(response.url, self.get_tax_information, meta={"cookiejar": response.meta['cookiejar'], "flight":flightItem, "tries": tries}, dont_filter=True)
            else:
                yield flightItem
        
    def parse_flight_data_tw(self, response):
        dd1 = response.meta["dd1"]
        dd2 = response.meta["dd2"]
        route = response.meta['route']
        flight_list = response.xpath("//flight-fee-selector")
        if not(flight_list):
            link = response.meta['link']
            yield scrapy.Request("https://booking.jetsmart.com/"+link, meta={"cookiejar": response.meta["cookiejar"], "dd1": dd1, "dd2": dd2, "route":route, "link":link}, callback=self.parse_flight_data_tw, dont_filter=True)

        flight_list_ow = flight_list.xpath("//flight-fee[@trip-index='0']").extract()
        flight_list_tw = flight_list.xpath("//flight-fee[@trip-index='1']").extract()
        if flight_list_ow:
            for flight in flight_list_ow:
                flight = Selector(flight)
                flightItem = JetsmartItem()
                flightItem["OD"] = route[0]+route[1]
                flightItem["POS"] = "PK"
                flightItem["carrier"] = "JA"
                flightItem["currency"] = "CLP"
                flightItem["destination"] = route[1]
                flightItem["observation_date"] = datetime.now().strftime("%Y-%m-%d")
                flightItem["observation_time"] = datetime.now().strftime("%H:%M")
                flightItem["oneway_indicator"] = 0
                flightItem["origin"] = route[0]
                flightItem["outbound_flight_number"] = flight.xpath("//@flight-number").extract_first()
                flightItem["outbound_travel_stopover"] = ""
                departure_hour_minute = flight.xpath("//@departure-time").extract_first().split(":")
                flightItem["outbound_departure_date"] = dd1.replace(hour=int(departure_hour_minute[0]), minute=int(departure_hour_minute[1])).strftime("%Y-%m-%d %H:%M")
                arrival_hour_minute = flight.xpath("//@arrival-time").extract_first().split(":")
                departure_datetime = dd1.replace(hour=int(departure_hour_minute[0]), minute=int(departure_hour_minute[1]))
                arrival_datetime = dd1.replace(hour=int(arrival_hour_minute[0]), minute=int(arrival_hour_minute[1]))
                if arrival_datetime < departure_datetime:
                    arrival_datetime += timedelta(days=1)
                    flightItem["outbound_arrival_date"] = arrival_datetime.strftime("%Y-%m-%d %H:%M")
                else:
                    flightItem["outbound_arrival_date"] = arrival_datetime.strftime("%Y-%m-%d %H:%M")
                flightItem["price_exc"] = flight.xpath("//@discounted-price").extract_first()
                flightItem["price_outbound"] = flightItem["price_exc"]
                flightItem["site_source"] = "JA"
                flightItem["source"] = "Jet Smart"
                sellkey1 =  flight.xpath("//input/@value").extract()[-1]
                if flight_list_tw:   
                    for out_flight in flight_list_tw:
                        out_flight = Selector(out_flight)
                        flightItem["inbound_flight_number"] = out_flight.xpath("//@flight-number").extract_first()
                        flightItem["inbound_travel_stopover"] = ""
                        departure_hour_minute = out_flight.xpath("//@departure-time").extract_first().split(":")
                        flightItem["inbound_departure_date"] = dd2.replace(hour=int(departure_hour_minute[0]), minute=int(departure_hour_minute[1])).strftime("%Y-%m-%d %H:%M")
                        arrival_hour_minute = out_flight.xpath("//@arrival-time").extract_first().split(":")
                        departure_datetime = dd2.replace(hour=int(departure_hour_minute[0]), minute=int(departure_hour_minute[1]))
                        arrival_datetime = dd2.replace(hour=int(arrival_hour_minute[0]), minute=int(arrival_hour_minute[1]))
                        if arrival_datetime < departure_datetime:
                            arrival_datetime += timedelta(days=1)
                            flightItem["inbound_arrival_date"] = arrival_datetime.strftime("%Y-%m-%d %H:%M")
                        else:
                            flightItem["inbound_arrival_date"] = arrival_datetime.strftime("%Y-%m-%d %H:%M")
                        flightItem["price_inbound"] = out_flight.xpath("//@discounted-price").extract_first()
                        price_exc = float(flightItem["price_outbound"].strip("$").strip()) + float(flightItem["price_inbound"].strip("$").strip())
                        flightItem["price_exc"] = "$ "+ str(price_exc)
                        sellkey2 = out_flight.xpath("//input/@value").extract()[-1]
                        yield scrapy.Request("https://booking.jetsmart.com/V2XHR/PriceBreakdownFlightSelect?cur=CLP&SellKeys[]="+sellkey1+",&SellKeys[]="+sellkey2, self.get_tax_information, meta={"cookiejar": response.meta['cookiejar'], "flight":flightItem, "tries": 1}, dont_filter=True)
                else:
                    if sellkey1:
                        yield scrapy.Request("https://booking.jetsmart.com/V2XHR/PriceBreakdownFlightSelect?cur=CLP&SellKeys[]="+sellkey1, self.get_tax_information, meta={"cookiejar": response.meta['cookiejar'], "flight":flightItem, "tries": 1}, dont_filter=True)
        elif flight_list_tw:
            for flight in flight_list_tw:
                flight = Selector(flight)
                flightItem = JetsmartItem()
                flightItem["OD"] = route[0]+route[1]
                flightItem["POS"] = "PK"
                flightItem["carrier"] = "JA"
                flightItem["currency"] = "CLP"
                flightItem["destination"] = route[1]
                flightItem["observation_date"] = datetime.now().strftime("%Y-%m-%d")
                flightItem["observation_time"] = datetime.now().strftime("%H:%M")
                flightItem["oneway_indicator"] = 0
                flightItem["origin"] = route[0]
                flightItem["inbound_flight_number"] = flight.xpath("//@flight-number").extract_first()
                flightItem["inbound_travel_stopover"] = ""
                departure_hour_minute = flight.xpath("//@departure-time").extract_first().split(":")
                flightItem["inbound_departure_date"] = dd2.replace(hour=int(departure_hour_minute[0]), minute=int(departure_hour_minute[1])).strftime("%Y-%m-%d %H:%M")
                arrival_hour_minute = flight.xpath("//@arrival-time").extract_first().split(":")
                departure_datetime = dd2.replace(hour=int(departure_hour_minute[0]), minute=int(departure_hour_minute[1]))
                arrival_datetime = dd2.replace(hour=int(arrival_hour_minute[0]), minute=int(arrival_hour_minute[1]))
                if arrival_datetime < departure_datetime:
                    arrival_datetime += timedelta(days=1)
                    flightItem["inbound_arrival_date"] = arrival_datetime.strftime("%Y-%m-%d %H:%M")
                else:
                    flightItem["inbound_arrival_date"] = arrival_datetime.strftime("%Y-%m-%d %H:%M")
                flightItem["price_exc"] = flight.xpath("//@discounted-price").extract_first()
                flightItem["price_inbound"] = flightItem["price_exc"]
                flightItem["site_source"] = "JA"
                flightItem["source"] = "Jet Smart"
                sellkey =  flight.xpath("//input/@value").extract()[-1]
                if sellkey:
                    yield scrapy.Request("https://booking.jetsmart.com/V2XHR/PriceBreakdownFlightSelect?cur=CLP&SellKeys[]="+sellkey, self.get_tax_information, meta={"cookiejar": response.meta['cookiejar'], "flight":flightItem, "tries": 1}, dont_filter=True)