import scrapy
from scrapy.linkextractors import LinkExtractor


class DarazMobile(scrapy.Spider):
    """This class contains two methods. parse_of_home_pages(this will
     call the second method and iterate through all the home pages) and
    parse_of_individual_pages (this will extract all the individual details
    of the mobile phone)."""

    name= "Daraz_Spider"
    allowed_domains = ['daraz.pk']
    start_urls = ['https://www.daraz.pk/smartphones/']


    def parse(self, response):
        """In this method, the program will iterate through the links and then
         call the second method for further retrieval of details.
         In the first LinkExtractor, we are eliminating urdu version
         of website and only allowing mobile sites which all start with
         .html. The pagination has page= from where link is followed"""

        item_links = LinkExtractor(allow='\.html', deny='ur')
        links = item_links.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,
                                 callback=self.parse_of_mobile)

        next_page=LinkExtractor(allow='page=')
        links = next_page.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,
                                 callback=self.parse)

    def parse_of_mobile(self, response):
        """This method crawls through individual pages and gathers all the
        details. Except the name and price, all details are in tables so
        a loop is functioned in the end which will iterate through each
        column and save the details in the dictionary"""

        # Splitting name so we don't get additional specs in name
        whole_name = str(response.css('h1.title::text')[0].extract())
        splitted_name=whole_name.split("-")

        name_of_mobile = {
            'Name' : splitted_name[0]
        }

        # Obtaining price of mobile
        price_of_mobile = {
            'Price' : response.css('span::attr(data-price)')[0].extract()
        }

        # Obtaining features from table
        column_number = len(response.css('div.osh-col::text').extract())

        features_of_mobile = {}

        # The code below uses selectors to fetch data and loop is driven
        # to populate as separate entries in dictionary
        for number_of_columns in range(0, column_number-1, 2):

            features_of_mobile.update({

                response.css('div.osh-col::text')[number_of_columns].extract():
                    response.css('div.osh-col::text')[number_of_columns+1].extract()

                        })
        # Appending all dictionaries into final dictionary

        final_dict = {**name_of_mobile, **price_of_mobile, **features_of_mobile}
        yield final_dict
