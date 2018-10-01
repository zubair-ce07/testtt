# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.shell import inspect_response


class OakwoodSpider(scrapy.Spider):
    name = 'oakwood'

    custom_settings = {
        "USER_AGENT": "'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    allowed_domains = ['gc.synxis.com']
    start_urls = ['https://gc.synxis.com/rez.aspx?Chain=7324&template=GCFOAK&SHELL=OakwoodShell']

    def parse(self, response):
        property_values = response.xpath("//*[@name='V110$C1$HotelDropDownList']//option/@value").extract()
        for value in property_values[1:]:
            yield scrapy.FormRequest.from_response(response, formname='XbeForm',
                                                   formdata={"V110$C1$HotelDropDownList": value},
                                                   callback=self.property_id
                                                   , meta={"value": value})

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

        body = {"criteria": {"year": 2018, "month": 10, "adults": 1, "children": 0, "childrenAges": "",
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
                                 callback=self.test,
                                 dont_filter=True)

    def test(self, response):
        inspect_response(response, self)



