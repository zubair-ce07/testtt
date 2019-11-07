import urllib.parse

from scrapy import Spider
from string import Template

from ..items import Docket


class ParseSpider():
    BASE_URL = 'http://www.floridapsc.com'
    
    OPEN = 'Open'
    CLOSED = 'Closed'
    STATE = 'FL'

    status_open = ['OPEN', 'Opened', 'Open']
    status_closed = ['CLOSED', 'Closed', 'CLOSE']

    industries = {
        'EI': 'Electric Utility - Investor Owned', 
        'EM': 'Electric Utility - Municipally Operated',
        'EC': 'Electric Utility - Rural Cooperative',
        'EU': 'Electric Utility - Generally',
        'EG': 'Energy Conservation',
        'EQ': 'Electric Utility - Qualifying Cogenerating Facility',
        'GU': 'Gas Utility',
        'GP': 'Gas Pipeline',
        'GS': 'Gas Safety',
        'TI': 'Telephone Utility - Interexchange',
        'TL': 'Telephone Utility - Local Exchange',
        'TC': 'Telephone Utility - Coin Telephone Service',
        'TA': 'Telephone Utility - Alternative Access Vendor',
        'TS': 'Telephone Utility - Shared Tenant Service',
        'TP': 'Telephone Utility - Generally',
        'TX': 'Telephone Utility- Alternative Local Exchange',
        'SU': 'Wastewater (Sewer) Utility',
        'WU': 'Water Utility',
        'WS': 'Water & Wastewater (Sewer) Utility',
        'PU': 'Public Utility',
        'OT': 'Other'   
    }

    def parse_docket(self, response):
        docket = Docket()
        
        docket['filed_on'] = self.get_filed_on(response)
        docket['industries'] = self.get_industries(response)
        docket['title'] = self.get_title(response)
        docket['state'] = self.STATE        
        docket['status'] = self.get_status(response)
        docket['filings'] = []
        docket['source_url'] = self.get_source_url(response)
        docket['source_title'] = self.get_title(response)
        docket['assignees'] = self.get_assignees(response)
        docket['major_parties'] = self.get_major_parties(response)

        filings_request = self.filings_request(response)

        return self.request_or_docket(docket, filings_request)    

    def parse_filings(self, response):
        filings = []

        docket = response.meta['docket']

        if 'page' not in response.url:
            requests = response.meta['requests'] + self.pagination_requests(response)
        else:
            requests = response.meta['requests']

        filing_rows = response.css('#dvDocketFile tbody tr')

        for row in filing_rows:
            filing_attributes = {}
            filing_attributes['documents'] = []

            document_attributes = {
                'name': self.get_name(row),
                'source_url': self.get_filing_url(row)
            }

            filing_attributes['documents'].append(document_attributes)

            filing_attributes['description'] = self.get_description(row)
            filing_attributes['filed_on'] = self.get_filing_date(row)

            filings.append(filing_attributes)
            docket['filings'].append(filings)

        return self.request_or_docket(docket, requests)

    def get_filed_on(self, response):
        return response.meta['filed_on']

    def get_industries(self, response):
        return self.map_industries(response.meta['docket_type'])

    def get_title(self, response):
        return response.css('table td strong::text').getall()[1]

    def get_source_url(self, response):
        return response.url  

    def get_status(self, response):
        status = response.css('table td span::text').re_first(r'\((.*)\)')
        return self.map_status(status)

    def get_assignees(self, response):
        return response.css('#dvPscStaff tbody td::text').getall()

    def get_major_parties(self, response):
        return response.css('#dvParties tbody td > b:first-child::text').getall()

    def get_name(self, row):
        name = row.css('.docTitle + td a::text').get()
        return name.replace('*', '') if name else name

    def get_filing_url(self, row):
        return urllib.parse.urljoin(self.BASE_URL, row.css('.docTitle + td a::attr(href)').get())

    def get_description(self, row):
        return row.css('.docTitle::text').get().strip()

    def get_filing_date(self, row):
        return row.css('td::text').re_first(r'\d+/\d+/\d+')

    def map_industries(self, docket_type):
        industries = self.industries
        return [industries[docket_type]] if docket_type in industries else industries['OT']

    def map_status(self, status):
        if status in self.status_open:
            return self.OPEN
        elif status in self.status_closed:
            return self.CLOSED 

    def filings_request(self, response):
        filings_url = response.css('table tr td a[href*="DocketFiling"]::attr(href)').get()        
        return [response.follow(filings_url, callback=self.parse_filings)]

    def pagination_requests(self, response):
        pagination_urls = response.css('.gridFooter a::attr(href)').getall()
        return [response.follow(url, callback=self.parse_filings) for url in pagination_urls]
        
    def request_or_docket(self, docket, requests):           
        if requests:            
            request = requests.pop(0)
            request.meta['docket'] = docket
            request.meta['requests'] = requests

            return request                                

        return docket


class FloridapscSpider(Spider):
    name = 'floridapsc_spider'
    allowed_domains = ['floridapsc.com']
    start_urls = ['http://floridapsc.com/ClerkOffice/Docket/']

    listings_url = Template(
            'http://www.floridapsc.com/ClerkOffice/DocketList?casestatus=0&' 
            'preHearingDate=01%2F01%2F0001%2000%3A00%3A00&document_id=0&radioValue=Date&' 
            'isCompleted=False&fromDate=$fromDate%2000%3A00%3A00&' 
            'toDate=$toDate%2000%3A00%3A00&docutype=0&EventType=All' 
    )

    docket_parser = ParseSpider()

    def parse(self, response):
        if self.fromDate:
            from_date = urllib.parse.quote(self.fromDate, safe='')    
        if self.toDate:
            to_date = urllib.parse.quote(self.toDate, safe='')

        url = self.listings_url.substitute(fromDate=from_date, toDate=to_date)

        return response.follow(url, callback=self.parse_pagination)

    def parse_pagination(self, response):        
        pagination_urls = response.css('.gridFooter a::attr(href)').getall()

        if pagination_urls:
            for url in pagination_urls:
                yield response.follow(url, callback=self.parse_listings)
        
        yield response.follow(response.url, callback=self.parse_listings, dont_filter=True)        

    def parse_listings(self, response):            
        for row in response.css('.webGrid tbody tr'):
            docket_record = {}

            docket_url = row.css('td a::attr(href)').get()
            docket_type = row.css('td a::text').get().split('-')[1]
            filed_date = row.css('td::text').re_first(r'\d+/\d+/\d+')

            docket_record['filed_on'] = filed_date
            docket_record['docket_type'] = docket_type
            
            yield response.follow(docket_url, callback=self.parse_item, meta=docket_record)

    def parse_item(self, response):
        return self.docket_parser.parse_docket(response)
