import scrapy


class FetchAll(scrapy.Spider):

    name = 'mobiles_specs'
    start_urls = [
                    'https://www.daraz.pk/phones-tablets/samsung/'
                 ]

    def parse_details(self, response):
        title = response.css('h1.title::text').extract_first()
        rating =  response.css('div.stars::attr(style)').extract_first()
        if rating:
            rating = rating.split(' ')[-1]
        price = response.css('span.price span::text').extract()[1]
        specs_heading = response.css('div.osh-row div.-head::text').extract()
        specs = response.css('div#product-details div.osh-row div.osh-col+div::text').extract()
        dict = { 'Title': title,
                 'Ratings': rating,
                 'Price' : price
        }
        for heading,spec in zip(specs_heading, specs):
            dict[heading] = spec
        yield dict
        return


    def parse(self, response):
        links = response.css('div.-gallery a.link::attr(href)').extract()
        for link in links:
            yield response.follow(link, callback=self.parse_details)

        next_page = response.css('section.pagination li.-selected + li a::attr(href)').extract_first()
        print "Next Page", next_page
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
