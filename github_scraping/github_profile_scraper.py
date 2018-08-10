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
                    'password': '*******'}
        yield FormRequest.from_response(
                           response,
                           formnumber=0,
                           formdata=formdata,
                           clickdata={'name': 'commit'},
                           callback=self.parse_profile)

    def get_teams(self, response):
        """This is a helper function for returning teams of a user"""
        teams = {
            'Teams': response.css('span.width-fit::text').extract()
        }
        return teams

    def get_repositories(self, response):
        """This is a helper function for returning repos of a user"""
        repos = {
            'All repositories': response.css('a.d-flex::attr(href)').extract()
        }
        return repos

    def get_pull_name(self, response, index_number):
        """This is a helper function for returning pull name of a PR"""
        pull_name = response.css('a.link-gray-dark::text')[index_number].extract()
        return pull_name

    def get_pull_link(self,response, index_number):
        """This is a helper function for returning pull link of a PR"""
        pull_link = response.css('a.link-gray-dark::attr(href)')[index_number].extract()
        return pull_link

    def parse_profile(self, response):
        """This will fetch all the teams and repos of the user"""
        open_in_browser(response)
        final_dict = {**self.get_teams(response), **self.get_repositories(response)}
        yield final_dict
        yield scrapy.Request(url='https://github.com/arbisoft/the-lab/pulls', callback=self.parse_the_lab)

    def parse_the_lab(self, response):
        """This will fetch all the pull requests in the-lab"""
        open_in_browser(response)
        number_of_elements = len(response.css('a.link-gray-dark::text').extract())
        for number in range(0, number_of_elements):
            pull_request= {
                'Pull name': self.get_pull_name(response, number),
                'Pull Link': self.get_pull_link(response, number)
            }
            yield pull_request
