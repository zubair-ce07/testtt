import scrapy


class specs(scrapy.Spider):
    name = "specs"

    start_urls = [
                    'https://www.daraz.pk/samsung-galaxy-grand-prime-plus-5.0-8gb-1.5gb-ram-8mp-black-6667089.html',
                    'https://www.daraz.pk/samsung-s8-5.8-4gb-ram-64gb-rom-12mp-maple-gold-6666307.html',
                 ]

    def parse(self, response):
        title = response.css('h1.title::text').extract_first()
        rating =  response.css('div.stars::attr(style)').extract_first().split(' ')[-1]
        price = response.css('span.price span::text').extract()[1]
        specs_heading = response.css('div.osh-row div.-head::text').extract()
        specs = response.css('div.osh-row div.osh-col+div::text').extract()
        dict = { 'Title': title,
                 'Ratings': rating,
                 'Price' : price
        }
        for heading,spec in zip(specs_heading, specs):
            dict[heading] = spec
        yield dict
