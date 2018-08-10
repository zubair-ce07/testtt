import json
import scrapy
from scrapy.selector import Selector


class QuotesSpider(scrapy.Spider):
    name = "brainy_quotes_spider"
    parameters = {
        "typ": "topic",
        "v": "8.2.1:2893987",
        "pg": 1,
        "id": "t:132622",
        "vid": "7b363d749b4c7c684ace871c8a75f8e6"
    }

    def start_requests(self):
        yield scrapy.Request(url='https://www.brainyquote.com/api/inf',
                             method='POST', callback=self.parse,
                             body=json.dumps(self.parameters),
                             headers={'Content-Type': 'application/json'})

    def parse(self, response):
        response_data = json.loads(response.text)

        for selection in Selector(text=response_data['content']).css('div.clearfix'):
            yield {
                'text': selection.css('a.oncl_q::text').extract(),
                'author': selection.css('a.oncl_a::text').extract(),
                'img-url': selection.css('::attr(data-img-url)').extract(),
                'shareable url': selection.css('::attr(href)').extract_first()
            }

        self.parameters['pg'] += 1

        yield scrapy.Request(url='https://www.brainyquote.com/api/inf',
                             method='POST', callback=self.parse,
                             body=json.dumps(self.parameters),
                             headers={'Content-Type': 'application/json'})
