import json
import re

import scrapy
from scrapy.selector import Selector


class QuotesSpider(scrapy.Spider):
    name = 'brainy_quotes_spider'
    start_urls = [
        'https://www.brainyquote.com/topics/motivational'
    ]

    def parse(self, response):
        quotes = response.xpath('//*[@id="quotesList"]')
        for quote in quotes:
            img_url = quote.css('::attr(data-img-url)').extract_first()
            if not img_url:
                img_url = 'No image URL'

            yield {
                'text': quote.css('a.oncl_q::text').extract_first(),
                'author': quote.css('a.oncl_a::text').extract_first(),
                'img-url': img_url,
                'shareable url': quote.css('::attr(href)').extract_first()
            }

        parameters = {}
        required_variables_script = response.xpath('//script[2]').extract_first()
        parameters['vid'] = re.search('VID=\'(.+?)\'', required_variables_script).group(1)
        required_variables_script = response.xpath('//script[11]').extract_first()
        parameters['id'] = re.search('PG_DM_ID=\"(.+?)\"', required_variables_script).group(1)
        parameters['typ'] = re.search('GA_PG_TYPE=\"(.+?)\"', required_variables_script).group(1)
        parameters['v'] = response.xpath('/html/head/meta[5]/@content').extract_first()
        parameters['pg'] = 2

        yield scrapy.Request(url='https://www.brainyquote.com/api/inf',
                             method='POST', callback=self.parse_inf_api_pages,
                             body=json.dumps(parameters),
                             headers={'Content-Type': 'application/json'},
                             meta=parameters)

    def parse_inf_api_pages(self, response):
        response_data = json.loads(response.text)

        for selection in Selector(text=response_data['content']).css('div.clearfix'):
            img_url = selection.css('::attr(data-img-url)').extract_first()
            if not img_url:
                img_url = 'No image URL'
            yield {
                'text': selection.css('a.oncl_q::text').extract(),
                'author': selection.css('a.oncl_a::text').extract(),
                'img-url': img_url,
                'shareable url': selection.css('::attr(href)').extract_first()
            }

        response.meta['pg'] += 1
        yield scrapy.Request(url='https://www.brainyquote.com/api/inf',
                             method='POST', callback=self.parse_inf_api_pages,
                             body=json.dumps(response.meta),
                             headers={'Content-Type': 'application/json'},
                             meta=response.meta)
