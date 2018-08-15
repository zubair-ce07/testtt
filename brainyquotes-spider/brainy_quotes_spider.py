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
            parameters = response.meta
            parameters['pg'] += 1
            response = Selector(text=json.loads(response.text)['content'])
        else:
            parameters = self.get_parameters(response)

        for quote_html in response.css('.m-brick.grid-item'):
            quote = {
                'quote': quote_html.xpath('.//a[contains(@class, "oncl_q")]/text()').extract_first(),
                'author': quote_html.xpath('.//a[contains(@class, "oncl_a")]/text()').extract_first(),
                'img_url': quote_html.xpath('.//a[contains(@class, "oncl_q")]/img/@data-img-url').extract_first()
            }
            tags = Selector(text=quote_html.xpath('.//div[@class="kw-box"]').extract_first())
            quote['tags'] = tags.xpath('//a/text()').extract()
            shareable_urls = Selector(text=quote_html.xpath('.//div[@class="sh-box"]').extract_first())
            quote['shareable_urls'] = {
                'facebook': shareable_urls.xpath('//a[1]/@href').extract_first(),
                'twitter': shareable_urls.xpath('//a[2]/@href').extract_first(),
                'pinterest': shareable_urls.xpath('//a[3]/@href').extract_first()
            }
            yield quote

        if response.xpath('//link[@rel="next"]/@href').extract():
            print('going to next page')

        yield scrapy.Request(url='https://www.brainyquote.com/api/inf',
                             method='POST', callback=self.parse,
                             body=json.dumps(parameters),
                             headers={'Content-Type': 'application/json'},
                             meta=parameters)

    def get_parameters(self, response):
        parameters = {}
        required_variables_script = response.xpath('//script[2]').extract_first()
        parameters['vid'] = re.search('VID=\'(.+?)\'', required_variables_script).group(1)
        required_variables_script = response.xpath('//script[11]').extract_first()
        parameters['id'] = re.search('PG_DM_ID=\"(.+?)\"', required_variables_script).group(1)
        parameters['typ'] = re.search('GA_PG_TYPE=\"(.+?)\"', required_variables_script).group(1)
        parameters['v'] = response.xpath('/html/head/meta[5]/@content').extract_first()
        parameters['pg'] = 2

        return parameters
