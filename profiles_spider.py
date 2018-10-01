import scrapy


class ProfileSpider(scrapy.Spider):

    name = "ProfileSpider"
    base_url = 'https://www.nwh.org/find-a-doctor/find-a-doctor-home'
    start_urls = [base_url]
    allowed_domains = ['www.nwh.org']

    def get_parameters(self, response):
        data = {}
        specialty = response.css('#ctl00_cphContent_ctl01_ddlResultsSpecialties > option::attr(value)').extract_first()
        generator = response.css('input[name="__VIEWSTATEGENERATOR"]::attr(value)').extract_first()
        state = response.css('input[name="__VIEWSTATE"]::attr(value)').extract_first()
        data.update({
            'ctl00$cphContent$ctl01$ddlResultsSpecialties': specialty,
            'ctl00$cphContent$ctl01$ddlPublished': "False",
            '__VIEWSTATE': state,
            '__VIEWSTATEGENERATOR': generator,
            '__EVENTTARGET': "ctl00$cphContent$ctl01$lnkSeachResults",
            'ctl00$cphContent$ctl01$ddlResultsPerPage': "99999",
            'ctl00$header$searchRdoBtn': "0",
            'ctl00$header$hdnHoverLocationId': "1",
            'ctl00$header$rptLocation$ctl00$hdnLocationId': "1",
            'ctl00$header$rptLocation$ctl01$hdnLocationId': "2",
            'ctl00$header$rptLocation$ctl02$hdnLocationId': "3",
            'ctl00$header$rptLocation$ctl03$hdnLocationId': "4",
            'ctl00$header$rptLocation$ctl04$hdnLocationId': "5",
            'ctl00$header$rptLocation$ctl05$hdnLocationId': "6",
            'ctl00$header$rptLocation$ctl06$hdnLocationId': "7",
            'ctl00$header$rptLocation$ctl07$hdnLocationId': "8",
            'ctl00$cphContent$ctl01$ddlPhysicianRefferalRequired': "-1",
            'ctl00$cphContent$ctl01$ddlAcceptNewPatients': "-1",
            'ctl00$cphContent$ctl01$ddlConcierge': "-1",
        })

        return data


    def parse(self, response):
        _params = self.get_parameters(response)
        yield scrapy.FormRequest(url=u"https://www.nwh.org/find-a-doctor/ContentPage.aspx?nd=847",
                                 formdata=_params, method='POST', callback=self.parse_doctors)

    def parse_doctors(self, response):
        doc_params = self.get_parameters(response)
        for doctors in response.css('a.link-name-profile'):
            target = doctors.css('a.link-name-profile::attr(href)').extract()
            targets = target[0][25:-5]
            doc_params.update({
                '__EVENTTARGET': targets,
            })
            yield scrapy.FormRequest(url=u"https://www.nwh.org/find-a-doctor/ContentPage.aspx?nd=847",
                                     formdata=doc_params, method='POST', callback=self.parse_profile)
    def parse_profile(self, response):
        for inf in response.css('div.light'):
            item = {
                'Full name':  inf.xpath('//h1[@class="header-doctor-name"]/text()').extract_first(),
                'Specialty': inf.xpath('//div[@class="pnl-doctor-specialty"]//h2/text()').extract()[0][50:-30],
                'Med school':  inf.xpath('//div[@id="ctl00_cphContent_ctl01_pnlMedicalSchool"]//ul//li/text()').extract(),
                'Affiliation': inf.xpath('//div[@id="ctl00_cphContent_ctl01_pnlBoardOfCertifications"]//ul//li/text()').extract(),
                'Grad education': inf.xpath('//div[@id="ctl00_cphContent_ctl01_pnlInternship"]//ul//li/text()').extract(),
                'Address': inf.css('.doctor-contact-location-address>a::text').extract(),
                'img_url': response.urljoin(response.css('div.pnl-doctor-image>img::attr(src)').extract_first()),
                'source url': response.request.url


            }
            yield item
