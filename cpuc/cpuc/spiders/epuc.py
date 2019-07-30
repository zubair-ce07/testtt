import re
from datetime import datetime, timedelta

import scrapy
from scrapy import FormRequest
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

        return scrapy.FormRequest(
            url='https://epuc.vermont.gov/?q=User',
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

        search_start_date = self.get_start_date()
        search_end_date = self.get_end_date()
        formdata = {
            'data(181445)': search_end_date,
            'data(181445_right)': search_start_date,
        }

        return FormRequest.from_response(
            response=response,
            formdata=formdata,
            callback=self.parse_proceeding_numbers,
            meta={
                'proceeding_urls': [],
                'proceeding_type': []
            },
            dont_filter=True
        )

    def parse_proceeding_numbers(self, response):
        """In this method, all docket numbers are turned into a list and send for getting infromation. """

        proceeding_urls = response.meta['proceeding_urls']
        proceeding_type = response.meta['proceeding_type']

        for row in response.xpath("//tr[starts-with(@id,'form_search_')]"):
            url = response.urljoin(row.xpath("td[1]/span/a/@href").get())

            if "q=node/104/" in url:
                url = url.replace("q=node/104/", "q=node/64/")
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

        docket_loader = ItemLoader(item=ProceedingDetail(), response=response, selector=response)

        docket_loader.add_value("source_url", response.url)
        content = response.xpath("//div[@class='content']/div[@style][1]/table")

        title = response.xpath("//div[@id='formBody_1065']/table//tr/td//span[last()]/text()").getall()

        if title:
            title = title[2].strip()

        docket_loader.add_value('title', title)
        docket_loader.add_value('proceeding_type', response.meta['proceeding_type'])
        filled_on = content.xpath("//tr[3]/td[2]/text()").get()

        if filled_on and len(filled_on) == 2:
            docket_loader.add_value('filled_on', filled_on.split(':')[1].strip())

        status = content.xpath("//tr[3]/td[1]/text()").get()

        if status and len(status) == 2:
            docket_loader.add_value('status', status.split(':')[1].strip())

        industries = content.xpath("//tr[5]/td[3]/text()").get()

        if industries:
            industries = industries.strip()

        docket_loader.add_value('industries', industries)
        url = response.url + '/FV-People-Portal'

        yield response.follow(
            url=url,
            meta={
                'docket_loader': docket_loader
            },
            callback=self.parse_filing_parties,

        )

    def parse_filing_parties(self, response):
        """In this method, all people who are involving in each docket are parse"""

        docket_loader = response.meta['docket_loader']
        filing_parties = response.xpath("//table[starts-with(@id, 'form.')]/tr[starts-with(@id, 'tree.branch.')]"
                                        "[not(starts-with(@class, 'tt'))]")
        parties = []

        for party in filing_parties:
            party = party.xpath("td[2]/span[last()]/text()").get()

            if party:
                parties.append(party.strip())

        docket_loader.add_value('filing_parties', parties)

        url = response.url.replace('/FV-People-Portal', '') + '/FV-BDIssued-PTL'

        yield response.follow(
            url=url,
            meta={
                'docket_loader': docket_loader,
                'filing': []
            },
            callback=self.parse_comission_issue_document
        )

    def parse_comission_issue_document(self, response):
        """In this method, all comission issue documents parse"""

        docket_loader = response.meta['docket_loader']
        filings = response.meta['filing']

        self.parse_filings(filings, response)

        url = response.url.replace('/FV-BDIssued-PTL', '') + '/FV-ALLOTDOX-PTL'

        yield response.follow(
            url=url,
            meta={
                'docket_loader': docket_loader,
                'filing': filings
            },
            callback=self.parse_other_document
        )

    def parse_other_document(self, response):
        """In this method, all other issue parse"""

        docket_loader = response.meta['docket_loader']
        filings = response.meta['filing']

        self.parse_filings(filings, response)

        docket_loader.add_value('filings', filings)

        return docket_loader.load_item()

    def parse_filings(self, filings, response):
        """In this method, here data of filing loads in filing list"""

        filings_data = response.xpath("//table[starts-with(@id, 'form.treeTable')]/tr[starts-with(@id, 'tree.branch')]")
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
                document = [filing.xpath("td[7]/a/@href").get().strip()]
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
                documents = filing.xpath("td[8]/a/@href").get()
                filing_loader.add_value('documents', documents)
                filings.append(filing_loader.load_item())
                del filing_loader
                filing_loader = ItemLoader(item=Filing(), response=response)

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
        count = 0
        for td in filing.xpath("td").getall():
            count += 1
        return count

    @staticmethod
    def get_start_date():
        search_start_date = datetime.now().date()
        search_start_date = search_start_date.strftime("%m/%d/%Y")
        return search_start_date

    def get_end_date(self):
        search_end_date = (datetime.now() - timedelta(days=int(self.days))).date()
        search_end_date = search_end_date.strftime("%m/%d/%Y")
        return search_end_date

    @staticmethod
    def removed_garbage_from_data(data_list):
        return [data.strip() for data in data_list if data.strip()]
