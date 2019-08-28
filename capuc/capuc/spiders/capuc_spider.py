import scrapy

from capuc.items import Docket


class CPUCSpider(scrapy.Spider):
    name = "cpuc"

    root_url = "http://docs.cpuc.ca.gov/advancedsearchform.aspx"
    result_url = "http://docs.cpuc.ca.gov/SearchRes.aspx"
    result_page = 1
    dock_url = "https://apps.cpuc.ca.gov/apex/f?p=401:{}:6056676397617::NO:RP,57,RIR:P5_PROCEEDING_SELECT:{}"

    def start_requests(self):
        yield scrapy.Request(url=self.root_url, callback=self.parse)

    def parse(self, response):
        form_data = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": response.xpath("//input[@name='__VIEWSTATE']/@value").get(),
            "__VIEWSTATEGENERATOR": response.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value").get(),
            "__EVENTVALIDATION": response.xpath("//input[@name='__EVENTVALIDATION']/@value").get(),
            "DocTitle": "",
            "ddlCpuc01Types": "-1",
            "ddlEfileTypes": "-1",
            "IndustryID": "-1",
            "ProcNum": "",
            "MeetDate": "",
            "FilingDateFrom": "08/14/19",
            "FilingDateTo": "08/18/19",
            "PubDateFrom": "",
            "PubDateTo": "",
            "EfileConfirmNum": "",
            "SearchButton": "Search"
        }
        yield scrapy.FormRequest(url=self.root_url, callback=self.parse_results, formdata=form_data)

    def parse_results(self, response):
        proceedings = response.xpath('//td[@class="ResultTitleTD"]/text()[2]').getall()
        for proceeding in proceedings:
            pros = proceeding[12:]
            if ";" in pros:
                prc_list = pros.split(": ")
                for prc in prc_list:
                    yield scrapy.Request(url=self.dock_url.format(56, prc), callback=self.parse_docket)
            else:
                yield scrapy.Request(url=self.dock_url.format(56, pros), callback=self.parse_docket)
            break

        # next_id = "rptPages_btnPage_{}".format(self.result_page)
        # event_target_text = response.xpath("//a[@id='{}']/@href".format(next_id)).get()
        # if event_target_text is not None:
        #     event_target = event_target_text.split("'")[1]
        #     form_data = {
        #         "__EVENTTARGET": event_target,
        #         "__EVENTARGUMENT": "",
        #         "__VIEWSTATE": response.xpath("//input[@name='__VIEWSTATE']/@value").get(),
        #         "__VIEWSTATEGENERATOR": response.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value").get(),
        #         "__EVENTVALIDATION": response.xpath("//input[@name='__EVENTVALIDATION']/@value").get(),
        #     }
        #     self.result_page += 1
        #     yield scrapy.FormRequest(url=self.result_url, callback=self.parse_results, formdata=form_data)

    def parse_docket(self, response):
        proceeding = response.url.split(":")[-1]
        doc = {
            "major_parties": response.xpath("//span[@id='P56_FILED_BY']/text()").extract(),
            "assignees": response.xpath("//span[@id='P56_STAFF']/text()").extract(),
            "filed_on": response.xpath("//span[@id='P56_FILING_DATE']/text()").get(),
            "industries": response.xpath("//span[@id='P56_INDUSTRY']/text()").extract(),
            "proceeding_type": response.xpath("//span[@id='P56_CATEGORY']/text()").get(),
            "title": response.xpath("//span[@id='P56_DESCRIPTION']/text()").get(),
            "status": response.xpath("//span[@id='P56_STATUS']/text()").get(),
            "slug": "ca-{}".format(proceeding.lower()),
            "state": "ca",
            "state_id": proceeding,
            "filings": []
        }
        yield scrapy.Request(url=self.dock_url.format(57, proceeding), callback=self.parse_docs, meta={"data": doc})

    def parse_docs(self, response):
        doc = response.meta["data"]
        rows = response.xpath("//tr[@class='odd' or @class='even']")
        filings = []
        sub_docs_urls = []
        for row in rows:
            sub_docs_url = row.xpath("td[@headers='DOCUMENT_TYPE']/a/@href").get()
            file = {
                "filed_on": row.xpath("td[@headers='FILING_DATE']/text()").get(),
                "description": row.xpath("td[@headers='DESCRIPTION']/text()").get(),
                "filing_parties": row.xpath("td[@headers='FILED_BY']/text()").get().split("/"),
                "state_id": sub_docs_url.split("=")[-1],
                "types": row.xpath("td[@headers='DOCUMENT_TYPE']/a/span/u/text()").extract()
            }
            filings.append(file)
            sub_docs_urls.append(sub_docs_url)
            break
        doc["filings"] = filings
        print(sub_docs_urls)
        for url in sub_docs_urls:
            yield scrapy.Request(url=url, callback=self.parse_sub_docs, meta={"data": doc})
            break

    @staticmethod
    def parse_sub_docs(response):
        doc = response.meta["data"]
        doc_id = response.url.split("=")[-1]
        file = "doc-{}.json".format(doc_id)
        with open(file, 'wb') as f:
            f.write(response.body)
        rows = response.xpath("//table[@id='ResultTable']/tbody/tr[not(@style)]")
        print("/////////////////////////////////////////////////////////printing rows")
        print(rows)
        sub_docs = []
        for row in rows:
            print("///////////////////////////////row//////////////////////////////")
            print(row)
            sub_doc = {
                "blob_name": "CA-{}-{}".format(doc["state_id"], doc_id),
                "extension": row.xpath("td[@class='ResultLinkTD']/a/text()").get(),
                "name": row.xpath("td[@class='ResultLinkTD']/a/@href").get().split(".")[0].split("/")[-1],
                "title": row.xpath("td[@class='ResultTitleTD']/text()[1]").get()
            }
            print(sub_doc)
            sub_docs.append(sub_doc)
        filings = []
        all_filled = True
        for filing in doc["filings"]:
            if filing["state_id"] == doc_id:
                filing["documents"] = sub_docs
            if "documents" not in filing:
                all_filled = False
            filings.append(filing)
        doc["filings"] = filings
        if all_filled:
            yield doc
