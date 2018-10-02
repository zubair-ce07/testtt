# -*- coding: utf-8 -*-
import json
import datetime

import scrapy
from scrapy.item import Item, Field
from scrapy.shell import inspect_response


class PropertyItem(Item):
    selected_property = Field()
    arrival_date = Field()
    departure_date = Field()
    calender_data = Field()


class CalenderDataItem(Item):
    available = Field()
    no_available = Field()
    min_stay = Field()
    max_stay = Field()
    no_arrival = Field()
    no_departure = Field()
    raw_dump = Field()


class OakwoodSpider(scrapy.Spider):
    name = 'oakwood'

    custom_settings = {
        "USER_AGENT": "'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "DOWNLOAD_DELAY": 1.25
    }
    allowed_domains = ['gc.synxis.com']
    start_urls = ['https://gc.synxis.com/rez.aspx?Chain=7324&template=GCFOAK&SHELL=OakwoodShell']

    def parse(self, response):
        property_titles = response.xpath("//*[@name='V110$C1$HotelDropDownList']//option/text()").extract()
        property_values = response.xpath("//*[@name='V110$C1$HotelDropDownList']//option/@value").extract()
        for value, title in zip(property_values[1:], property_titles[1:]):
            yield scrapy.FormRequest.from_response(response, formname='XbeForm',
                                                   formdata={"V110$C1$HotelDropDownList": value},
                                                   callback=self.property_id
                                                   , meta={"value": value,
                                                           "title": title})

    def property_id(self, response):
        property_id = response.xpath("//script[contains(text(),"
                                     " 'Xbe.State.hotelId')]").re_first("Xbe\.State\.hotelId\D+(\d+)")
        headers = {
            'Origin': 'https://gc.synxis.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.99 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://gc.synxis.com/rez.aspx?Chain=7324&template=GCFOAK&SHELL=OakwoodShell',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
        current_date = datetime.datetime.now()
        last_date = datetime.datetime(current_date.year + 2, current_date.month, current_date.day)

        while current_date <= last_date:

            body = {"criteria": {"year": current_date.year, "month": current_date.month, "adults": 1,
                                 "children": 0, "childrenAges": "",
                                 "rooms": 1, "corporatePromotionCode": "", "travelIndustryCode": "",
                                 "numberOfMonths": 3, "nights": 1, "hotelId": property_id, "hotelGroupId": 7324,
                                 "hotelGuid": response.meta["value"],
                                 "hotelGroupGuid": "b40433f8-b314-4925-a585-2db369943968", "primaryChannelId": 1,
                                 "secondaryChannelId": 5,
                                 "customerUniqueId": "00000000-0000-0000-0000-000000000000",
                                 "BookerUniqueId": "00000000-0000-0000-0000-000000000000",
                                 "templateInstanceUniqueId": "5b061de2-79b9-4e0e-bc85-79fac2e12fda",
                                 "roomTypeFilterCodes": "", "rateFilterCodes": "",
                                 "isRequireFilter": False, "includeUnassignedRatesInRateFilters": False,
                                 "hideAssignedRatesOnEmptyFilter": False,
                                 "requestedNewRates": "", "userLocationCode": "",
                                 "arrivalTicks": 0, "departureTicks": 0,
                                 "calculatePricing": 2,
                                 "includeTaxesInPricingCalculation": False,
                                 "showPriceAmount": 1,
                                 "calendarRate": "", "currencyDisplayId": 1,
                                 "restrictions": "MINLOS|OPEN|NOARRIVE|OPEN" ,
                                 "losUsedByCalendar": 2,
                                 "membershipLevel": "",
                                 "certificates": "", "confirmNumber": "", "isSoaEnabled": "",
                                 "dayCellStyleSuffix": "", "highlightWeekendsAndHolidays": False,
                                 "weekendDefinition": 0,
                                 "forceDisplayPricing": False,
                                 "localCalId": 6714}}

            yield scrapy.Request(url="https://gc.synxis.com/services/XbeService.asmx/GetCalendarAvailability",
                                     body=json.dumps(body),
                                     headers=headers,
                                     method="POST",
                                     callback=self.parse_calender,
                                     dont_filter=True,
                                 meta={"title": response.meta["title"],
                                       "day": current_date.day,
                                       "year": current_date.year,
                                       "month": current_date.month})

            current_date = current_date + datetime.timedelta(days=1)

    def parse_calender(self, response):
        arrival_date = datetime.datetime(response.meta["year"], response.meta["month"], response.meta["day"])
        departure_date = arrival_date + datetime.timedelta(days=30)

        property_item = PropertyItem()
        property_item["selected_property"] = response.meta["title"]
        property_item["arrival_date"] = arrival_date.strftime("%d %B %Y")
        property_item["departure_date"] = departure_date.strftime("%d %B %Y")

        calender_data = json.loads(response.text)["d"]
        calender_item = CalenderDataItem()
        calender_item["available"] = self.load_dates(calender_data[1], arrival_date, departure_date)
        calender_item["min_stay"] = self.load_dates(calender_data[2], arrival_date, departure_date)
        calender_item["max_stay"] = self.load_dates(calender_data[3], arrival_date, departure_date)
        calender_item["no_arrival"] = self.load_dates(calender_data[4], arrival_date, departure_date)
        calender_item["no_departure"] = self.load_dates(calender_data[5], arrival_date, departure_date)
        calender_item["no_available"] = self.load_dates(calender_data[6], arrival_date, departure_date)
        calender_item["raw_dump"] = response.text

        property_item["calender_data"] = calender_item

        yield property_item

    def load_dates(self, raw_legend_data, arrival_date, departure_date):
        raw_legend_data = raw_legend_data.replace("'", '"')
        raw_legend_data = json.loads(raw_legend_data)

        legend_data = []

        for raw_data in raw_legend_data:
            if raw_data[0] < arrival_date.month:
                year = arrival_date.year+1
            else:
                year = arrival_date.year

            raw_data_date = datetime.datetime(year, raw_data[0], raw_data[1])
            if arrival_date <= raw_data_date <= departure_date:
                legend_data.append({
                    "month": raw_data[0],
                    "date": raw_data[1],
                    "year": year,
                    "type": raw_data[2]
                })

        return legend_data
