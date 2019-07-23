import re

import scrapy
from scrapy import FormRequest
from datetime import datetime, timedelta

from scrapy.loader import ItemLoader

from cpuc.items import ProceedingDetail, Filing


class CpucSpider(scrapy.Spider):
    name = "epuc"
    allowed_domains = ['epuc.vermont.gov']
    start_urls = ['https://epuc.vermont.gov/?q=User']

    def __init__(self, days=2, *args, **kwargs):
        super(CpucSpider, self).__init__(*args, **kwargs)
        self.days = days

    def parse(self, response):
        """ This function will do login ."""

        form_build_id = response.xpath("//*[@name='form_build_id']/@value").get()
        formdata = {
            'name': 'shahrukh.ijaz@arbisoft.com',
            'pass': 'shahrukh31',
            'form_id': 'user_login',
            'form_build_id': form_build_id,
            'op': 'Log in'
        }
        cookiejar = form_build_id
        return scrapy.FormRequest(
            url='https://epuc.vermont.gov/?q=User',
            formdata=formdata,
            meta={
                'cookiejar': cookiejar
            },
            method='POST',
            callback=self.redirect_to_search
            )

    def redirect_to_search(self, response):
        """ This function will redirect to the search case page."""

        return response.follow(
            url='https://epuc.vermont.gov/?q=node/101',
            callback=self.search_case,
            meta={'cookiejar': response.meta['cookiejar']}
        )

    @staticmethod
    def get_start_date():
        search_start_date = datetime.now().date()
        search_start_date = search_start_date.strftime("%m/%d/%Y")
        return search_start_date

    def get_end_date(self):
        search_end_date = (datetime.now() - timedelta(days=int(self.days))).date()
        search_end_date = search_end_date.strftime("%m/%d/%Y")
        return search_end_date

    def search_case(self, response):
        """This function make search for last two days dockets"""

        search_start_date = self.get_start_date()
        search_end_date = self.get_end_date()

        ecp_form_id = response.xpath("//input[@name='ecpFormId']/@value").get()

        formdata = {
            'formId': response.xpath("//*[@name='formId']/@value").get(),
            'data(181445)': search_end_date,
            'data(181445_right)': search_start_date,
            'eCourtFormCode': 'S-Document-Orders-Portal',
            'ecpFormId': ecp_form_id,
            'op': 'Search',
            'form_build_id': response.xpath("//input[@name='form_build_id']/@value").get(),
            'form_id': 'ecp_searchform_form'
        }

        return FormRequest.from_response(
            response=response,
            formdata=formdata,
            callback=self.parse_proceeding_numbers,
            meta={
                'cookiejar': response.meta['cookiejar'],
                'proceeding_urls': [],
                'proceeding_type': []
            },
            dont_filter=True
        )

    def parse_proceeding_numbers(self, response):
        """In this method, all docket numbers are turned into a list and send for getting infromation. """

        proceeding_urls = response.meta['proceeding_urls']
        proceeding_type = response.meta['proceeding_type']

        for row in response.xpath("//table[contains(@class, 'searchResultsPage')]/tr[starts-with(@id,'form_search_')]"):
            proceeding_urls.append(response.urljoin(row.xpath("td[1]/span/a/@href").get()))
            proceeding_type.append(row.xpath("td[3]/text()").get().strip())

        next_page = response.xpath("//ul[@class='pagination']/li[@class=' active ']/following-sibling::li/a/@href").get()

        if next_page:

            yield response.follow(
                next_page,
                callback=self.parse_proceeding_numbers,
                meta={
                    'cookiejar': response.meta['cookiejar'],
                    'proceeding_urls': proceeding_urls,
                    'proceeding_type': proceeding_type
                    }
             )

        else:

            for index, url in enumerate(proceeding_urls):

                yield response.follow(
                    url,
                    callback=self.parse_proceeding_details,
                    meta={
                        'cookiejar': response.meta['cookiejar'],
                        'proceeding_type': proceeding_type[index]
                    }
                )

    def parse_proceeding_details(self, response):
        """In this method, all proceeding docket detail will scrap"""

        if response.url != 'https://epuc.vermont.gov/?q=node/104/16216':

            docket_loader = ItemLoader(item=ProceedingDetail(), response=response, selector=response)

            docket_loader.add_value("source_url", response.url)
            content = response.xpath("//div[@class='content']/div[@style][1]/table")
            title = response.xpath("//div[@id='formBody_1065']/table//tr/td//span[last()]/text()").getall()[2].strip()
            docket_loader.add_value('title', title)
            docket_loader.add_value('proceeding_type', response.meta['proceeding_type'])
            docket_loader.add_value('filled_on', content.xpath("//tr[3]/td[2]/text()").get().split(':')[1].strip())
            docket_loader.add_value('status', content.xpath("//tr[3]/td[1]/text()").get().split(':')[1].strip())
            docket_loader.add_value('industries', content.xpath("//tr[5]/td[3]/text()").get().strip())

            yield response.follow(
                url='https://epuc.vermont.gov/?q=node/64/143572/FV-People-Portal',
                meta={
                    'cookiejar': response.meta['cookiejar'],
                    'docket_loader': docket_loader
                },
                callback=self.parse_filing_parties,
                dont_filter=True

            )

    def parse_filing_parties(self, response):
        """In this method, all people who are involving in each docket are parse"""

        docket_loader = response.meta['docket_loader']

        filing_parties = response.xpath("//table[starts-with(@id, 'form.')]/tr[starts-with(@id, 'tree.branch.')]")
        parties = []
        for party in filing_parties:
            party = party.xpath("td[2]/span[last()]/text()").get()
            if party:
                parties.append(party.strip())

        docket_loader.add_value('filing_parties', parties)

        yield response.follow(
            url='https://epuc.vermont.gov/?q=node/64/143572/FV-BDIssued-PTL',
            meta={
                'cookiejar': response.meta['cookiejar'],
                'docket_loader': docket_loader,
                'filing': []
            },
            dont_filter=True,
            callback=self.parse_comission_issue_document
        )

    def parse_comission_issue_document(self, response):
        """In this method, all comission issue documents parse"""

        docket_loader = response.meta['docket_loader']
        filings = response.meta['filing']

        self.parse_filings(filings, response)

        yield response.follow(
            url='https://epuc.vermont.gov/?q=node/64/143572/FV-ALLOTDOX-PTL',
            meta={
                'cookiejar': response.meta['cookiejar'],
                'docket_loader': docket_loader,
                'filing': filings
            },
            dont_filter=True,
            callback=self.parse_other_document
        )

    def parse_other_document(self, response):
        """In this method, all other issue parse"""

        docket_loader = response.meta['docket_loader']
        filings = response.meta['filing']

        self.parse_filings(filings, response)

        docket_loader.add_value('filings', filings)

        return docket_loader.load_item()

    @staticmethod
    def parse_filings(filings, response):
        """In this method, here data of filing loads in filing list"""

        filings_data = response.xpath("//table[starts-with(@id, 'form.')]/tr[starts-with(@class, 'tt')]")
        for filing in filings_data:
            filing_loader = ItemLoader(item=Filing(), response=response, selector=filing)
            filled_on = filing.xpath("td[2]/text()").getall()[3].strip()
            filing_loader.add_value('filled_on', filled_on)
            filing_loader.add_xpath('description', "td[3]/text()")
            filing_loader.add_xpath('types', "td[6]/text()")
            filings.append(filing_loader.load_item())
