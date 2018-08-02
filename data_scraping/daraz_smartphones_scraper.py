import scrapy


class DarazMobile(scrapy.Spider):
    """This class contains two methods. parse_of_home_pages(this will
     call the second method and iterate through all the home pages) and
    parse_of_individual_pages (this will extract all the individual details
    of the mobile phone)."""

    name= "Daraz_Spider"
    start_urls = ['https://www.daraz.pk/smartphones/']

    def parse(self, response):
        """In this method, the program will first specifically select the
        'div.sku' space to gather and iterate through the links and then
         call the second method for further retrieval of details."""

        for mobile in response.css('div.sku'):
            individual_page = mobile.css('a.link::attr(href)')[0].extract()
            yield scrapy.Request(url=individual_page,
                                 callback=self.parse_of_individual_page)

        next_page = response.css('a[title="Next"]::attr(href)').extract_first()
        """The above line is retrieving the link for individual product"""

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

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
