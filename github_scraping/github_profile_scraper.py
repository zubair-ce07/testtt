from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.spider import Spider
from scrapy.utils.response import open_in_browser
import scrapy


class GitSpider(Spider):
    name = "github"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/login"]

    def parse(self, response):
        """Username and password is given here and using form number,
        POST request is given"""
        formdata = {'login': 'ibraheem-nadeem',
                    'password': 'Batch@2015'}
        yield FormRequest.from_response(response,
                                        formnumber=0,
                                        formdata=formdata,
                                        clickdata={'name': 'commit'},
                                        callback=self.parse_profile)

    def parse_profile(self, response):
        """This will fetch all the teams and repos of the user"""
        open_in_browser(response)
        self.record = {
            'Teams': response.css('span.width-fit::text').extract(),
            'All repositories': response.css('a.d-flex::attr(href)').extract(),

        }
        yield self.record
        yield scrapy.Request(url='https://github.com/arbisoft/the-lab/pulls', callback=self.parse_arbisoft)

    def parse_arbisoft(self, response):
        """This will fetch all the pull requests in the-lab"""
        open_in_browser(response)
        number_of_elements = len(response.css('a.link-gray-dark::text').extract())
        for number in range(0, number_of_elements):
            pull_request= {
                'Pull name': response.css('a.link-gray-dark::text')[number].extract(),
                'Pull link': response.css('a.link-gray-dark::attr(href)')[number].extract()
            }
            yield pull_request
