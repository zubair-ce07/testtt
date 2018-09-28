# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response


class OakwoodSpider(scrapy.Spider):
    name = 'oakwood'
    allowed_domains = ['gc.synxis.com']
    start_urls = ['https://gc.synxis.com/rez.aspx?Chain=7324&template=GCFOAK&SHELL=OakwoodShell']

    def parse(self, response):
        property_values = response.xpath("//*[@name='V110$C1$HotelDropDownList']//option/@value").extract()
        for value in property_values[1:]:
            yield scrapy.FormRequest.from_response(response, formname='XbeForm',
                                                   formdata={"V110$C1$HotelDropDownList": value}, callback=self.test
                                                   , meta={"value": value})

    def test(self, response):
        property_id = response.xpath("//script[contains(text(),"
                                     " 'Xbe.State.hotelId')]").re_first("Xbe\.State\.hotelId\D+(\d+)")
        print(property_id, response.meta["value"])
