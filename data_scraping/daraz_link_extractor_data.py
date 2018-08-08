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
         call the second method for further retrieval of details."""
        item_links = LinkExtractor(allow='\.html')
        links = item_links.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,
                                 callback=self.parse_of_individual_page)

        next_page=LinkExtractor(allow='page=',unique=True)
        links = next_page.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,
                                 callback=self.parse)

    def parse_of_individual_page(self, response):
        """This method crawls through individual pages and gathers all the
        details. Except the name and price, all details are in tables so
        a loop is functioned in the end which will iterate through each
        column and save the details in the dictionary"""
        self.arbi = {
            'Name' : response.css('h1.title::text')[0].extract(),
            'Price' : response.css('span::attr(data-price)')[0].extract()
        }
        table_column = len(response.css('div.osh-col::text').extract())
        for iteration in range(0, table_column-1, 2):
            self.arbi.update({

                response.css('div.osh-col::text')[iteration].extract():
                    response.css('div.osh-col::text')[iteration+1].extract()

                        })
        yield self.arbi
