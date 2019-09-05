import datetime
import scrapy
import urllib.parse as urlparse


class CPUCSpider(scrapy.Spider):
    name = "capuc"
    proceeding_page = 1
    root_url = "http://docs.cpuc.ca.gov/advancedsearchform.aspx"
    result_url = "http://docs.cpuc.ca.gov/SearchRes.aspx"
    filing_pagination_url = "https://apps.cpuc.ca.gov/apex/wwv_flow.show"
    dock_url = "https://apps.cpuc.ca.gov/apex/f?p=401:{}:6056676397617::NO:RP,57,RIR:P5_PROCEEDING_SELECT:{}"

    def start_requests(self):
        # `start` and `end` being command line arguments here
        self.validate_date(self.start)
        self.validate_date(self.end)
        yield scrapy.Request(url=self.root_url, callback=self.parse)

    def parse(self, response):
        # filling the search form and requesting
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
            "FilingDateFrom": self.start,
            "FilingDateTo": self.end,
            "PubDateFrom": "",
            "PubDateTo": "",
            "EfileConfirmNum": "",
            "SearchButton": "Search"
        }
        yield scrapy.FormRequest(url=self.root_url, callback=self.parse_results, formdata=form_data)

    @staticmethod
    def validate_date(date):
        try:
            datetime.datetime.strptime(date, '%m/%d/%y')
        except ValueError:
            raise ValueError("Incorrect date format, should be MM/DD/YY")

    def parse_results(self, response):
        proceedings = response.xpath('//td[@class="ResultTitleTD"]/text()[2]').getall()
        for proceeding in proceedings:
            proceeding = proceeding[12:]
            if ";" in proceeding:
                proc_list = proceeding.split("; ")
                for prc in proc_list:
                    yield scrapy.Request(url=self.dock_url.format(56, prc), callback=self.parse_docket)
            else:
                yield scrapy.Request(url=self.dock_url.format(56, proceeding), callback=self.parse_docket)

        # running pagination on proceedings result pages
        yield from self.paginate_proceedings(response)

    def paginate_proceedings(self, response):
        next_id = "rptPages_btnPage_{}".format(self.proceeding_page)
        event_target_text = response.xpath("//a[@id='{}']/@href".format(next_id)).get()
        if event_target_text is not None:
            event_target = event_target_text.split("'")[1]
            form_data = {
                "__EVENTTARGET": event_target,
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": response.xpath("//input[@name='__VIEWSTATE']/@value").get(),
                "__VIEWSTATEGENERATOR": response.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value").get(),
                "__EVENTVALIDATION": response.xpath("//input[@name='__EVENTVALIDATION']/@value").get(),
            }
            self.proceeding_page += 1
            yield scrapy.FormRequest(url=self.result_url, callback=self.parse_results,
                                     formdata=form_data)

    def parse_docket(self, response):
        # extracting docket data against one proceeding and requesting for its filings
        proceeding = response.url.split(":")[-1]
        doc = {
            "state_id": proceeding,
            "major_parties": response.xpath("//span[@id='P56_FILED_BY']/text()").extract(),
            "assignees": response.xpath("//span[@id='P56_STAFF']/text()").extract(),
            "filed_on": response.xpath("//span[@id='P56_FILING_DATE']/text()").get(),
            "industries": response.xpath("//span[@id='P56_INDUSTRY']/text()").extract(),
            "proceeding_type": response.xpath("//span[@id='P56_CATEGORY']/text()").get(),
            "title": response.xpath("//span[@id='P56_DESCRIPTION']/text()").get(),
            "status": response.xpath("//span[@id='P56_STATUS']/text()").get(),
            "slug": "ca-{}".format(proceeding.lower()),
            "state": "ca",
            "filings": []
        }
        yield scrapy.Request(url=self.dock_url.format(57, proceeding), callback=self.parse_docs, meta={"data": doc})

    def parse_docs(self, response):
        # parsing the filings against one proceeding
        doc = response.meta["data"]
        sub_docs_urls = []
        if "urls" in response.meta:
            sub_docs_urls = response.meta["urls"]
        rows = response.xpath("//tr[@class='odd' or @class='even']")
        for row in rows:
            sub_docs_url = row.xpath("td[@headers='DOCUMENT_TYPE']/a/@href").get()
            parsed = urlparse.urlparse(sub_docs_url)
            query_dict = urlparse.parse_qs(parsed.query)
            state_id = None
            if "DocID" in query_dict:
                state_id = query_dict["DocID"][0]
                sub_docs_urls.append(sub_docs_url)
            file = {
                "filed_on": row.xpath("td[@headers='FILING_DATE']/text()").get(),
                "description": row.xpath("td[@headers='DESCRIPTION']/text()").get(),
                "filing_parties": row.xpath("td[@headers='FILED_BY']/text()").get().split("/"),
                "state_id": state_id,
                "types": row.xpath("td[@headers='DOCUMENT_TYPE']/a/span/u/text()").extract()
            }
            doc["filings"].append(file)

        # running pagination on filings
        yield from self.paginate_filings(response, doc, sub_docs_urls)

        # requesting for sub documents against one filing
        if sub_docs_urls:
            url = sub_docs_urls.pop()
            yield scrapy.Request(url=url, headers={"Referer": response.url},
                                 callback=self.parse_sub_docs,
                                 meta={"data": doc, "urls": sub_docs_urls, "dont_merge_cookies": True})

    def paginate_filings(self, response, doc, sub_docs_urls):
        next_link = response.xpath("//span[@class='fielddata']/a")
        if next_link:
            p_instance = response.xpath("//input[@name='p_instance']/@value").get() or response.meta["p_instance"]
            form_data = {
                "p_request": "APXWGT",
                "p_instance": p_instance,
                "p_flow_id": "401",
                "p_flow_step_id": "57",
                "p_widget_num_return": "100",
                "p_widget_name": "worksheet",
                "p_widget_mod": "ACTION",
                "p_widget_action": "PAGE",
                "p_widget_action_mod": response.xpath("//span[@class='fielddata']/a/@href")[0].get().split("'")[1],
                "x01": response.xpath("//input[@id='apexir_WORKSHEET_ID']/@value").get(),
                "x02": response.xpath("//input[@id='apexir_REPORT_ID']/@value").get(),
            }
            yield scrapy.FormRequest(url=self.filing_pagination_url, callback=self.parse_docs,
                                     meta={"data": doc, "urls": sub_docs_urls, "p_instance": p_instance},
                                     formdata=form_data)

    def parse_sub_docs(self, response):
        doc = response.meta["data"]
        sub_docs_urls = response.meta["urls"]
        next_url = None
        if sub_docs_urls:
            next_url = sub_docs_urls.pop()
        doc_id = response.url.split("=")[-1]
        rows = response.xpath("//table[@id='ResultTable']/tbody/tr[not(@style)]")
        sub_docs = []
        for row in rows:
            sub_doc = {
                "blob_name": "CA-{}-{}".format(doc["state_id"], doc_id),
                "extension": row.xpath("td[@class='ResultLinkTD']/a/text()").get(),
                "name": row.xpath("td[@class='ResultLinkTD']/a/@href").get().split(".")[0].split("/")[-1],
                "title": row.xpath("td[@class='ResultTitleTD']/text()[1]").get()
            }
            sub_docs.append(sub_doc)
        all_filled = True
        for i, _ in enumerate(doc["filings"]):
            if doc["filings"][i]["state_id"] is None:
                continue
            if doc["filings"][i]["state_id"] == doc_id:
                doc["filings"][i]["documents"] = sub_docs
            if "documents" not in doc["filings"][i]:
                all_filled = False
        if all_filled:
            yield doc
        else:
            yield scrapy.Request(url=next_url, headers={"Referer": response.url},
                                 callback=self.parse_sub_docs,
                                 meta={"data": doc, "urls": sub_docs_urls, "dont_merge_cookies": True})
