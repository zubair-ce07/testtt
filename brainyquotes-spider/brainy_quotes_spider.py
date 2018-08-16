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
        if response.request.method == 'POST':
            pagination_request_parameters = response.meta
            pagination_request_parameters['pg'] += 1
            response = Selector(text=json.loads(response.text)['content'])
        else:
            pagination_request_parameters = self.get_pagination_request_parameters(response)

        for quote_html in response.css('.m-brick.grid-item'):
            quote = {
                'quote': quote_html.css('.oncl_q::text').extract_first(),
                'author': quote_html.css('.oncl_a::text').extract_first(),
                'img_url': quote_html.css('.bqpht::attr(data-img-url)').extract_first(),
                'tags': quote_html.css('.oncl_k::text').extract(),
                'shareable_urls': {
                    'facebook': quote_html.css('.sh-fb::attr(href)').extract_first(),
                    'twitter': quote_html.css('.sh-tw::attr(href)').extract_first(),
                    'pinterest': quote_html.css('.sh-pi::attr(href)').extract_first()
                }
            }
            yield quote

        if pagination_request_parameters['pg'] <= pagination_request_parameters['last_page']:
            yield scrapy.Request(url='https://www.brainyquote.com/api/inf',
                                 method='POST', callback=self.parse,
                                 body=json.dumps(pagination_request_parameters),
                                 meta=pagination_request_parameters)

    def get_pagination_request_parameters(self, response):
        required_variables_script = response.xpath('//script[11]').extract_first()
        parameters = {
            'id': re.search('PG_DM_ID=\"(.+?)\"', required_variables_script).group(1),
            'typ': re.search('GA_PG_TYPE=\"(.+?)\"', required_variables_script).group(1),
            'v': response.xpath('//meta[5]/@content').extract_first(),
        }
        required_variables_script = response.xpath('//script[2]').extract_first()
        parameters.update({
            'vid': re.search('VID=\'(.+?)\'', required_variables_script).group(1),
            'last_page': int(re.search('LPAGE = (.+?);', required_variables_script).group(1)),
            'pg': int(re.search('CPAGE = (.+?);', required_variables_script).group(1)) + 1
        })
        return parameters
