import scrapy


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
            "FilingDateTo": "08/22/19",
            "PubDateFrom": "",
            "PubDateTo": "",
            "EfileConfirmNum": "",
            "SearchButton": "Search"
        }
        yield scrapy.FormRequest(url=self.root_url, callback=self.parse_results, formdata=form_data)

    def parse_results(self, response):
        proceedings = response.xpath('//td[@class="ResultTitleTD"]/text()[2]').getall()
        for proceeding in proceedings:
            prc = proceeding[12:]
            # todo - break the list
            if ";" not in prc:
                yield scrapy.Request(url=self.dock_url.format(56, prc), callback=self.parse_docket)

        next_id = "rptPages_btnPage_{}".format(self.result_page)
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
            self.result_page += 1
            yield scrapy.FormRequest(url=self.result_url, callback=self.parse_results, formdata=form_data)

    def parse_docket(self, response):
        proceeding = response.url.split(":")[-1]
        data = {
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
        print("=========================================")
        print(data)
        print("=========================================")
        yield scrapy.Request(url=self.dock_url.format(57, proceeding), callback=self.parse_docs)

    @staticmethod
    def parse_docs(response):
        proceeding = response.url.split(":")[-1]
        rows = response.xpath("//tr[@class='odd' or @class='even']").extract()
        for row in rows:
            filed_on = row.xpath("td[@headers='FILING_DATE']/text()").get()
            description = row.xpath("td[@headers='DESCRIPTION']/text()").get()
            sub_docs_url = row.xpath("td[@headers='DOCUMENT_TYPE']/a/@href").get()
            state_id = sub_docs_url.split("=")[-1]
            types = row.xpath("td[@headers='DOCUMENT_TYPE']/a/span/u/text()").get()
            filing_parties = row.xpath("td[@headers='FILED_BY']/text()").get()
