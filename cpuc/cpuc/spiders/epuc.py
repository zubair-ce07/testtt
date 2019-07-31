import re
from datetime import datetime, timedelta

import scrapy
from scrapy import FormRequest
from scrapy.loader import ItemLoader

from cpuc.items import ProceedingDetail, Filing, Document


class VermontSpider(scrapy.Spider):
    name = "vermont"
    allowed_domains = ['epuc.vermont.gov']
    start_urls = ['https://epuc.vermont.gov/?q=User']

    def __init__(self, days=2, *args, **kwargs):
        super(VermontSpider, self).__init__(*args, **kwargs)
        self.days = days

    def parse(self, response):
        """ This function will do login ."""

        formdata = {
            'name': 'shahrukh.ijaz@arbisoft.com',
            'pass': 'shahrukh31'
        }

        return scrapy.FormRequest.from_response(
            response=response,
            formdata=formdata,
            method='POST',
            callback=self.redirect_to_search
        )

    def redirect_to_search(self, response):
        """ This function will redirect to the search case page."""

        return response.follow(
            url='https://epuc.vermont.gov/?q=node/101',
            callback=self.search_case,
        )

    def search_case(self, response):
        """This function make search for last two days dockets"""

        search_start_date = self.get_end_date()
        search_end_date = self.get_start_date()
        formdata = {
            'data(181445)': search_end_date,
            'data(181445_right)': search_start_date,
        }

        return FormRequest.from_response(
            response=response,
            formdata=formdata,
            callback=self.parse_proceeding_numbers,
            dont_filter=True
        )

    def parse_proceeding_numbers(self, response):
        """In this method, all docket numbers are turned into a list and send for getting infromation. """

        proceeding_urls = response.meta.get('proceeding_urls', [])
        proceeding_type = response.meta.get('proceeding_type', [])

        for row in response.xpath("//tr[starts-with(@id,'form_search_')]"):

            url = response.urljoin(row.xpath("td[1]/span/a/@href").get())
            proceeding_urls.append(url)
            proceeding_type.append(row.xpath("td[3]/text()").get().strip())

        next_page = response.xpath("//li[@class=' active ']/following-sibling::li/a/@href").get()

        if next_page:

            yield response.follow(
                next_page,
                callback=self.parse_proceeding_numbers,
                meta={
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
                        'proceeding_type': proceeding_type[index]
                    }
                )

    def parse_proceeding_details(self, response):
        """In this method, all proceeding docket detail will scrap"""

        if "q=node/104/" in response.url:

            return self.handle_legacy_request(response)

        docket_loader = ItemLoader(item=ProceedingDetail(), response=response, selector=response)

        content = response.xpath("//div[@class='content']/div[@style][1]/table")

        docket_loader.add_value('proceeding_type', response.meta['proceeding_type'])
        filed_on = response.meta.get('filed_on', None)
        filed_on = self.parse_filed_on_date(filed_on, content)
        docket_loader.add_value('filled_on', filed_on)

        docket_loader.add_value("source_url", response.url)
        docket_loader.add_value('state_id', response.url.rsplit('/', 1)[-1])

        docket_loader.add_value('title', self.removed_garbage_from_data(
            response.xpath("//div[@id='formBody_1065']/table//tr/td//"
                           "span[last()]/text()").getall()))

        docket_loader.add_value('proceeding_type', response.meta['proceeding_type'])

        docket_loader.add_value('industries', self.removed_garbage_from_data(
            content.xpath("//tr[5]/td[3]/text()").getall()))

        docket_loader.add_value('status', self.remove_garbage_from_string(
            content.xpath("//tr[1]/td[last()-1]/text()").get()))

        docket_loader.add_value('spider_name', self.name)
        docket_loader.add_value('state', "VT")

        yield response.follow(
            url=response.url + '/FV-People-Portal',
            callback=self.parse_filing_parties,
            meta={
                'docket_loader': docket_loader
            }
        )

    def parse_filing_parties(self, response):
        """In this method, all people who are involving in each docket are parse"""

        docket_loader = response.meta['docket_loader']
        filing_parties = response.xpath("//tr[starts-with(@id, 'tree.branch.')][not(starts-with(@class, 'tt'))]")
        parties = []

        for party in filing_parties:

            party = party.xpath("td[2]/span[last()]/text()").get()

            if party:

                parties.append(party.strip())

        docket_loader.add_value('filing_parties', parties)

        url = response.url.replace('/FV-People-Portal', '/FV-BDIssued-PTL')

        yield response.follow(
            url=url,
            callback=self.parse_comission_issue_document,
            meta={
                'docket_loader': docket_loader,
            }
        )

    def parse_comission_issue_document(self, response):
        """In this method, all comission issue documents parse"""

        docket_loader = response.meta['docket_loader']
        filings = response.meta.get('filing', [])

        self.parse_filings(filings, response)

        url = response.url.replace('/FV-BDIssued-PTL', '/FV-ALLOTDOX-PTL')

        yield response.follow(
            url=url,
            callback=self.parse_other_document,
            meta={
                'docket_loader': docket_loader,
                'filing': filings
            }
        )

    def parse_other_document(self, response):
        """In this method, all other issue parse"""

        docket_loader = response.meta['docket_loader']
        filings = response.meta['filing']

        self.parse_filings(filings, response)

        docket_loader.add_value('filings', filings)

        url = response.url.replace('/FV-ALLOTDOX-PTL', '/FV-PFEXAFF-PTL')

        yield response.follow(
            url=url,
            callback=self.parse_prefiled_testimony_exhibits_documents,
            meta={
                'docket_loader': docket_loader,
                'filing': filings
            }
        )

    def parse_prefiled_testimony_exhibits_documents(self, response):
        docket_loader = response.meta['docket_loader']
        filings = response.meta['filing']

        self.parse_filings(filings, response)

        docket_loader.add_value('filings', filings)

        return docket_loader.load_item()

    def parse_filings(self, filings, response):
        """In this method, here data of filing loads in filing list"""

        filings_data = response.xpath("//tr[starts-with(@id, 'tree.branch')]")
        doc_type = ""
        filing_loader = ItemLoader(item=Filing(), response=response)

        for filing in filings_data:

            if self.get_column_count(filing) == 2:

                doc_type = filing.xpath("td[2]/text()").getall()
                doc_type = self.removed_garbage_from_data(doc_type)
                match = re.search(r'(\d+/\d+/\d+)', doc_type[0])

                if match:
                    filing_loader.add_value('filled_on', match.group(1))
                else:
                    filing_loader.add_value('types', doc_type[0])

            elif self.get_column_count(filing) == 7:

                if len(filing_loader.get_output_value('types')) == 0:

                    filing_loader.add_value('types', doc_type)

                if filing_loader.get_output_value('filled_on') is None:

                    filled_on = filing.xpath("td[2]/text()").getall()
                    filled_on = self.removed_garbage_from_data(filled_on)
                    filing_loader.add_value('filled_on', filled_on)

                filing_loader.replace_value('description', filing.xpath("td[3]/text()").get().strip())

                document = self.parse_document_details(self.remove_garbage_from_string(
                    filing.xpath("td[7]/a/@href").get()), response.meta['docket_loader'])

                filing_loader.replace_value('documents', document)
                del document

                filing_parties = self.get_filing_if_exist(response, filing)

                if filing_parties:

                    filing_loader.replace_value('filing_parties', filing_parties)

                filings.append(filing_loader.load_item())
                del filing_loader
                filing_loader = ItemLoader(item=Filing(), response=response)

            elif self.get_column_count(filing) == 8:

                filled_on = self.removed_garbage_from_data(filing.xpath("td[2]/text()").getall())
                filing_loader.add_value('filled_on', filled_on)
                description = filing.xpath("td[3]/text()").get().strip()
                filing_loader.add_value('description', description)
                filing_parties = self.removed_garbage_from_data(filing.xpath("td[5]/text()").getall())
                filing_loader.add_value('filing_parties', filing_parties)

                document = self.parse_document_details(self.remove_garbage_from_string(
                    filing.xpath("td[8]/a/@href").get()), response.meta['docket_loader'])
                filing_loader.add_value('documents', document)

                filings.append(filing_loader.load_item())
                del filing_loader
                filing_loader = ItemLoader(item=Filing(), response=response)

    @staticmethod
    def parse_document_details(document_url, docket_loader):
        document_loader = ItemLoader(item=Document())
        title = document_url.rsplit('/', 1)[-1]
        document_loader.add_value('title', title)
        document_loader.add_value('extension', ".PDF")
        document_loader.add_value('source_url', "https://epuc.vermont.gov/{}".format(document_url))
        document_loader.add_value('blob_name', "{}_{}_{}".format(
                                  docket_loader.get_output_value('state'),
                                  docket_loader.get_output_value('state_id'),
                                  document_loader.get_output_value('title')))

        return document_loader.load_item()

    @staticmethod
    def get_filing_if_exist(response, filing):
        filings_data = response.xpath("//table[starts-with(@id, 'form.treeTable')]/thead/tr[2]/th[5]/text()")\
            .get().strip()

        if filings_data == 'Filed By':

            filing_parties = filing.xpath("td[4]/text()").get().strip()

            return filing_parties

        return False

    @staticmethod
    def get_column_count(filing):
        return len(filing.xpath("td").getall())

    @staticmethod
    def get_end_date():
        search_start_date = datetime.now().date()
        search_start_date = search_start_date.strftime("%m/%d/%Y")

        return search_start_date

    def get_start_date(self):
        search_end_date = (datetime.now() - timedelta(days=int(self.days))).date()
        search_end_date = search_end_date.strftime("%m/%d/%Y")

        return search_end_date

    @staticmethod
    def removed_garbage_from_data(data_list):
        return [data.strip() for data in data_list if data.strip() and len(data.strip()) > 1]

    def handle_legacy_request(self, response):
        filed_on = response.xpath("//table//tr[1]/td[2]/text()").get()

        if 'Date Filed' in filed_on:

            match = re.search(r'(\d+/\d+/\d+)', filed_on)
            filed_on = match.group(1)
            url = response.url.replace('q=node/104/', 'q=node/64/')

            return response.follow(
                url=url,
                callback=self.parse_proceeding_details,
                meta={
                    'filed_on': filed_on
                }
            )

    @staticmethod
    def parse_filed_on_date(filed_on, content):
        if filed_on:

            return filed_on
        else:

            filed_on = content.xpath("//tr[3]/td[2]/text()").get()

            if filed_on:

                return filed_on.split(':')[1].strip()

    @staticmethod
    def remove_garbage_from_string(data):
        if data.strip():

            return data.strip()

        return None
