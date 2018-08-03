import scrapy


class YayvoMobile(scrapy.Spider):
    """This class contains two methods. parse(this will
     call the second method and iterate through all the home pages) and
    parse_of_individual_pages (this will extract all the individual details
    of the mobile phone)."""

    name= "Yayvo_Spider"
    start_urls = ['http://yayvo.com/mobiles-tablets/smartphones.html']

    def parse(self, response):
        """In this method, the program will obtain the number of links
        present for each specific page and call the individual parser
        for each one of them. After all items have been iterated from the
        home page, crawler will go to the next page."""

        number_of_elements = len(response.css('a.product-image::attr(href)').extract())
        for mobile in range (0, number_of_elements):
            individual_page = response.css('a.product-image::attr(href)')[mobile].extract()
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
        self.record = {
            'Name' : response.css('div.product-name > h1::text')[0].extract(),
            'Price' : response.css('span.price::text')[1].extract()
        }
        table_column = len(response.css('td.label::text').extract())
        for iteration in range(0, table_column-1, 2):
            self.record.update({

                response.css('td.label::text')[iteration].extract():
                    response.css('td.data::text')[iteration].extract()

                        })
        yield self.record
