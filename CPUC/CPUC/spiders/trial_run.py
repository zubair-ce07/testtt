# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import re
import json
import requests



class CpucSpider(scrapy.Spider):
    name = 'cpuc'
    #allowed_domains = ['https://apps.cpuc.ca.gov/apex/f?p=401:1:0::NO:RP']
    start_urls = ['https://apps.cpuc.ca.gov/apex/f?p=401:1:0::NO:RP']
    PAGNITION_URL = "https://apps.cpuc.ca.gov/apex/wwv_flow.show"
    URL_PART = 'https://apps.cpuc.ca.gov/apex/'
    P_WIDGET_NUM_RETURN = '100'
    P_WIDGET_Name = 'worksheet'
    P_WIDGET_MOD = 'ACTION'
    P_WIDGET_ACTION = 'PAGE'
    P_INSTANCE = ''
    P_FLOW_ID = ''
    P_FLOW_STEP_ID = ''
    P_WIDGET_ACTION_MOD = ''
    proceeding_items = dict()
    document_items = dict()
    document_data_item = dict()
    


    def __init__(self, low_date_range=None, high_date_range=None,**kwargs):
        
        super(CpucSpider, self).__init__(**kwargs)
        if low_date_range is None or high_date_range is None:
            self.low_date_range = ''
            self.high_date_range = ''
        else:
            self.low_date_range = low_date_range
            self.high_date_range = high_date_range

    @staticmethod
    def validate_date(date):
        """Date validation for data ranges."""
        try:
            datetime.strptime(date, '%m/%d/%Y')
            return True
        except ValueError:
            print("Date format is not correct.")
            exit()

    def parse(self, response):
        if self.low_date_range and self.high_date_range:
            if self.validate_date(self.low_date_range) and \
                    self.validate_date(self.high_date_range):
                form_data = {'p_t05': self.low_date_range,
                             'p_t06': self.high_date_range}
           
        else:
            form_data = {'p_t05': '10/01/2019',
                         'p_t06': '10/09/2019'}

        yield scrapy.FormRequest.from_response(
            response,
            formdata=form_data,
            callback=self.parse_proceedings
        )
    
    def parse_proceedings(self, response):
        
        proceeding_urls = response.css("table.apexir_WORKSHEET_DATA tr a::attr(href)").getall()
        for url in proceeding_urls:
            proceeding_url = self.URL_PART + url
            yield scrapy.Request(url=proceeding_url, callback=self.parse_proceeding_data)
            # yield {
            #     'proceeding': proceeding_url
            # }
                
            

        self.P_WIDGET_ACTION_MOD = response.css('.fielddata > a:nth-child(2)::attr(href)').get()

        if self.P_WIDGET_ACTION_MOD is not None:
            self.P_WIDGET_ACTION_MOD = self.P_WIDGET_ACTION_MOD.split("'")[1]
        if not self.P_WIDGET_ACTION_MOD:
            self.P_WIDGET_ACTION_MOD = response.css('.fielddata > a::attr(href)').get()
        if self.P_WIDGET_ACTION_MOD is not None:
            self.P_WIDGET_ACTION_MOD = self.P_WIDGET_ACTION_MOD.split("'")[1]
        if not self.P_INSTANCE:
            self.P_INSTANCE = response.css('#pInstance::attr(value)').get()
        if not self.P_FLOW_ID:
            self.P_FLOW_ID = response.css('#pFlowId::attr(value)').get()
        if not self.P_FLOW_STEP_ID:
            self.P_FLOW_STEP_ID = response.css('#pFlowStepId::attr(value)').get()


        if response.css('.fielddata > a') and response.css(".fielddata > a > img[title*='Next']"):
            form_data = {'p_request': 'APXWGT',
                         'p_instance': self.P_INSTANCE,
                         'p_flow_id': self.P_FLOW_ID,
                         'p_flow_step_id': self.P_FLOW_STEP_ID,
                         'p_widget_num_return': self.P_WIDGET_NUM_RETURN,
                         'p_widget_name': self.P_WIDGET_Name,
                         'p_widget_mod': self.P_WIDGET_MOD,
                         'p_widget_action': self.P_WIDGET_ACTION,
                         'p_widget_action_mod': self.P_WIDGET_ACTION_MOD,
                         'x01': response.css('#apexir_WORKSHEET_ID::attr(value)').get(),
                         'x02': response.css('#apexir_REPORT_ID::attr(value)').get(),
                         }
            req = scrapy.FormRequest(
                self.PAGNITION_URL,
                formdata=form_data,
                callback=self.parse_proceedings
                )
            yield req

    def parse_proceeding_data(self, response):
        documents_url = str(response.url).replace(':56:', ':57:')

        proceeding_detail_item = {
            'proceeding_number': response.css('div.rc-content-main >h1::text').get().split(' ')[0],
            'filed_by': response.css('#P56_FILED_BY::text').get(),
            'service_lists': response.css('#P56_SERVICE_LISTS > span > a::attr(href)').getall(),
            'industry': response.css('#P56_INDUSTRY::text').get(),
            'filing_date': response.css('#P56_FILING_DATE::text').get(),
            'category': response.css('#P56_CATEGORY::text').get(),
            'current_status': response.css('#P56_STATUS::text').get(),
            'description' : response.css('#P56_DESCRIPTION::text').get(),
            'staff' : response.css('#P56_STAFF::text').getall(),
        }
        self.proceeding_items = proceeding_detail_item
        yield scrapy.Request(url=documents_url, callback=self.parse_proceeding_documents)

    def parse_proceeding_documents(self, response):
        filing_date = re.findall(r"headers=\"FILING_DATE\">(.*?)</td>", response.text)
        document_url = re.findall(r"headers=\"DOCUMENT_TYPE\"><a href=\"(.*?)\">", response.text)
        document_type = re.findall(r'blue"><u>(.*?)</u>', response.text)
        filed_by = re.findall(r"headers=\"FILED_BY\">(.*?)</td>", response.text)
        description = re.findall(r"headers=\"DESCRIPTION\">(.*?)</td>", response.text)
        
        for data in range(len(filing_date)):
            document_data_item = {
                'document_filing_date ': filing_date[data],
                'document_type': document_type[data],
                'document_url': document_url[data],
                'document_filed_by': filed_by[data],
                'document_description': description[data],     
            }
        self.document_items = document_data_item
        yield self.proceeding_items
        yield document_data_item

        #for data in document_url:
            #yield scrapy.Request(url=data, callback=self.parse_documents)

    #def parse_documents(self, response):



        
        

