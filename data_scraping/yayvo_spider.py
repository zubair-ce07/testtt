import scrapy
from scrapy.linkextractors import LinkExtractor


class YayvoMobile(scrapy.Spider):
    """This class contains two methods. parse_of_home_pages(this will
     call the second method and iterate through all the home pages) and
    parse_of_individual_pages (this will extract all the individual details
    of the mobile phone)."""

    name= "Yayvo_Spider"
    allowed_domains = ['yayvo.com']
    start_urls = ['http://yayvo.com/mobiles-tablets/smartphones.html']

    def parse(self, response):
        """In this method, the program will iterate through the links and then
         call the second method for further retrieval of details."""

        # The line below only fetches individual smartphones
        #  because all item have "gb" in them

        item_links = LinkExtractor(allow='\gb')
        links = item_links.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,
                                 callback=self.parse_of_mobile)

        # This line will fetch the next page
        next_page=LinkExtractor(allow='p=')
        links = next_page.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,
                                 callback=self.parse)

    def parse_of_mobile(self, response):
        """This method crawls through individual pages and gathers all the
        details. Except the name and price, all details are in tables so
        a loop is functioned in the end which will iterate through each
        column and save the details in the dictionary"""
        name_of_mobile = {
            'Name': response.css('div.product-name > h1::text')[0].extract()
        }

        # Obtaining price of mobile
        price_of_mobile = {
            'Price': response.css('span.price::text')[1].extract()
        }

        # Obtaining features from table
        column_number = len(response.css('td.label::text').extract())

        features_of_mobile = {}

        # The code below uses selectors to fetch data and loop is driven
        # to populate as separate entries in dictionary
        for number_of_columns in range(0, column_number - 1, 2):
            features_of_mobile.update({

                response.css('td.label::text')[number_of_columns].extract():
                    response.css('td.data::text')[number_of_columns].extract()

            })
        # Appending all dictionaries into final dictionary

        final_dict = {**name_of_mobile, **price_of_mobile, **features_of_mobile}
        yield final_dict
