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

        # The line below only fetches items because all item have "gb" in them
        item_links = LinkExtractor(allow='\gb')
        links = item_links.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,
                                 callback=self.parse_of_individual_page)

        # This line will fetch the next page and remove duplicates
        next_page=LinkExtractor(allow='p=', unique=True)
        links = next_page.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,
                                 callback=self.parse)

    def parse_of_individual_page(self, response):
        """This method crawls through individual pages and gathers all the
        details. Except the name and price, all details are in tables so
        a loop is functioned in the end which will iterate through each
        column and save the details in the dictionary"""
        self.record = {
            'Name': response.css('div.product-name > h1::text')[0].extract(),
            'Price': response.css('span.price::text')[1].extract()
        }
        table_column = len(response.css('td.label::text').extract())
        for iteration in range(0, table_column - 1, 2):
            self.record.update({

                response.css('td.label::text')[iteration].extract():
                    response.css('td.data::text')[iteration].extract()

            })
        yield self.record
