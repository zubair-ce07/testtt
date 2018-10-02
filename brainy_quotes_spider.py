import json
from copy import deepcopy

import scrapy


class BrainyQuotesSpider(scrapy.Spider):
    name = "BrainyQuotes"
    start_urls = [
        'https://www.brainyquote.com/topics'
    ]
    request_url = 'https://www.brainyquote.com/api/inf'

    def parse(self, response):
        topics = response.css('div.bqLn')
        for each_topic in topics:
            topic_url = response.urljoin(each_topic.css('a.topicIndexChicklet::attr(href)').extract_first())
            yield scrapy.Request(topic_url, callback=self.parse_topics)

    def parse_topics(self, response):
        request_params = {
            'ab': 'a',
            'fdd': 'd',
            'langc': 'en',
            'm': 0,
            'typ': 'topic',
        }
        v = response.xpath("//meta[@property='ver']/@content").extract_first()
        vid = response.xpath('//script[@type="text/javascript"]').re_first("VID='(.*?)';")
        _id = response.xpath('//script[@type="text/javascript"]').re_first('PG_DM_ID="(.+)";')
        last_page = response.xpath('//script[@type="text/javascript"]').re_first('LPAGE =(.+);')
        request_params = deepcopy(request_params)
        request_params.update({
            'v': v,
            'vid': vid,
            'id': _id,
        })
        for quotes in response.css('div.m-brick'):
            yield {
                    'Quote': quotes.css('a.b-qt::text').extract_first(),
                    'Author': quotes.css('div.clearfix a.oncl_a::text').extract_first(),
                    'Tags': quotes.css('div.kw-box a.oncl_list_kc::text').extract(),
                    'Shareable links': quotes.css('div.sh-box a.fa-stack::attr(href)').extract(),
                    'img_url': response.urljoin(quotes.css('img.zoomc::attr(data-img-url)').extract_first()),
            }
        for page_no in range(2, int(last_page)):
            request_params['pg'] = page_no
            yield scrapy.Request(self.request_url, callback=self.parse_scrolled_pages, method='POST', body=json.dumps(request_params),
                                 headers={'Content-Type': 'application/json'})

    def parse_scrolled_pages(self, response):
        json_response = json.loads(response.body_as_unicode())
        data_store = json_response['content'].encode('ascii', 'ignore')
        data = scrapy.Selector(text=data_store)
        for quotes in data.css('div.m-brick'):
            yield {
                    'Quote': quotes.css('a.b-qt::text').extract_first(),
                    'Author': quotes.css('div.clearfix a.oncl_a::text').extract_first(),
                    'Tags': quotes.css('div.kw-box a.oncl_list_kc::text').extract(),
                    'Shareable links': quotes.css('div.sh-box a.fa-stack::attr(href)').extract(),
                    'img_url': response.urljoin(quotes.css('img.zoomc::attr(data-img-url)').extract_first()),
            }
