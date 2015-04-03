from scrapy.spider import Spider
from scrapy.selector import Selector
from zip_code.items import ZipCodeItem
from scrapy.http import Request

class ZipSpider(Spider):
    name = 'zipSpider'
    allowed_domains = ['zip-codes.com']
    start_urls = ['http://www.zip-codes.com/']
    all_urls = []                                      # List of all urls from where data will scrap
    total_population = 0                               # To compare population between multiple county
    detail_requests = []                               # List of Request for parse_population
    zip_details = []                                   # List for results


    # To update all_urls by reading zip from input file
    def __init__(self,file_name=None,
            *args, **kwargs):
        super(ZipSpider, self).__init__(*args, **kwargs)
        file = open(file_name, 'r')
        for line in file:
            code = line.split('\r')
            code = code[0]
            self.all_urls.append(
                'http://www.zip-codes.com/zip-code/'+code+'/zip-code-'+code+'.asp')


    # Run spider to get next Request to parse the page
    def parse(self,response):
        return self.make_next_request()


    # Get Next Request to Scrap from Queue
    def make_next_request(self):
        if self.detail_requests:
            return self.detail_requests.pop(0)              # Request of checking greater population method in Queue

        if self.all_urls:
            zip_url = self.all_urls.pop(0)
            return Request(
                url = zip_url,
                callback=self.parse_page
            )                                               # Request for new Zip Code page from all_urls


    # Scrap data from given zip code url
    def parse_page(self,response):
        zip_detail = ZipCodeItem()
        sel = Selector(response)
        zip_detail['city'] = sel.xpath(
            '//td[a[contains(text(),"City:")]]/following-sibling::td//text()'
            ).extract()[0]
        zip_detail['state'] = sel.xpath(
            '//td[a[contains(text(),"State:")]]/following-sibling::td//text()'
            ).extract()[0]
        multi_county = sel.xpath(
            '//td[a[contains(text(),"Multi County:")]]/following-sibling::td//text()'
            ).extract()[0]
        if multi_county == 'Yes':
            county_urls = sel.xpath(
                '//td[a[contains(text(),"Counties")]]/following-sibling::td//a/@href'
                ).extract()
            i = 0
            for c_url in county_urls:
                c_url = 'http://www.zip-codes.com%s' %c_url
                county_name = sel.xpath(
                    '//td[a[contains(text(),"Counties")]]/following-sibling::td//text()'
                    ).extract()[i]
                i = i + 1
                req = Request(url=c_url,
                    meta= {'zip_detail' :zip_detail,'county_name' : county_name },
                    callback = self.parse_population)                                      # Request for parse_population
                self.detail_requests.append(req)
        elif multi_county == 'No':
            zip_detail['county'] = sel.xpath(
                '//td[a[contains(text(),"Counties")]]/following-sibling::td//text()'
                ).extract()[0]
        self.total_population = 0
        self.zip_details.append(zip_detail)
        print self.zip_details
        return self.make_next_request()                                                    # Add Next page parse request


    # Compare population and set greater population county
    def parse_population(self, response):
        sel = Selector(response)
        population = sel.xpath(
            '//td[contains(text(),"Total population of")]/following-sibling::td//text()'
            ).extract()[0]
        zip_detail = response.meta['zip_detail']
        if population > self.total_population:
            zip_detail['county'] = response.meta['county_name']
            self.total_population = population
        yield zip_detail
        yield self.make_next_request()                                       #Add request for Next county population



