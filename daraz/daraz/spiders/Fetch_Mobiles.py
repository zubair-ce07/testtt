import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from daraz.items import DarazItem

class rules(CrawlSpider):
    name = 'rules'
    start_urls = [
                    'https://www.daraz.pk/phones-tablets/samsung/'
                 ]

    def parse_details(self, response):
        title = response.css('h1.title::text').extract_first()
        rating =  response.css('.stars::attr(style)').extract_first()
        if rating:
            rating = rating.split()[-1]
        else:
            rating = None
        price = response.css('.price span::text').extract()[1]
        specs_heading = response.css('.osh-row .-head::text').extract()
        specs = response.css('#product-details .osh-row .osh-col+div::text').extract()
        specs_dic = { 'Title': title,
                      'Ratings': rating,
                      'Price' : price
                    }
        for heading,spec in zip(specs_heading, specs):
            specs_dic[heading] = spec
        yield specs_dic
        return


    rules = [

            Rule(LinkExtractor(restrict_css=('.link')), callback='parse_details'),
            Rule(LinkExtractor(restrict_css=('.item')), callback='parse'),
            Rule(LinkExtractor(restrict_css=('.-gallery','.pagination .-selected + li')), follow=True)

    ]
