import json

import scrapy
from WWE.items import Item
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from w3lib.html import remove_tags, replace_escape_chars


class WWESpider(CrawlSpider):
    name = 'wwe-crawler'

    base_url = 'https://wwecorp.wd5.myworkdayjobs.com/wwecorp?clientRequestID=d4a6cc91769d43b5b9a6f0821100ad91'
    job_posting_url = 'https://wwecorp.wd5.myworkdayjobs.com{}'

    headers = {
        'Accept': 'application/json,application/xml',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'wwecorp.wd5.myworkdayjobs.com',
        'User-Agent': 'Mozilla/5.0(X11;Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko)'
                      ' Chrome / 71.0.3578.98 Safari / 537.36',
        'X-Workday-Client': '2018.51.1488'
    }

    def start_requests(self):

        yield Request(self.base_url,
                      headers=self.headers, callback=self.parse_jobs)

    def parse_jobs(self, response):

        jobs = json.loads(response.text)
        job_posting = jobs['body']['children'][0]['children'][0]['listItems']
        for job in job_posting:
            yield Request(self.job_posting_url.format(job['title']['commandLink']),
                          headers=self.headers, callback=self.parse_job_details)

    def parse_job_details(self, response):
        job_details = json.loads(response.text)
        l = ItemLoader(item=Item(), response=response)
        l.add_value('categories', self.extract_categories(job_details))
        l.add_value('title', self.extract_title(job_details))
        l.add_value('description', self.extract_description(job_details))
        l.add_value('job_types', self.extract_job_type(job_details))
        l.add_value('job_date', self.extract_job_date(job_details))
        l.add_value('provider', 'WWE careers')
        l.add_value('url', response.url)

        if len(job_details['body']['children'][1]['children'][0]['children']) > 4:
            for location in job_details['body']['children'][1]['children'][0]['children']:
                if 'LOCATION' in location.values():
                    l.replace_value('location', location['imageLabel'])
                    l.replace_value('external_id', '{}_{}'.format(
                        job_details['body']['children'][1]['children'][1]['children'][2]['imageLabel'],
                        location['imageLabel']))
                    yield l.load_item()
        else:
            l.add_value('external_id', job_details['body']['children'][1]['children'][1]['children'][2]['imageLabel'])
            l.add_value('location', job_details['body']['children'][1]['children'][0]['children'][0]['imageLabel'])
            yield l.load_item()

    def extract_categories(self, job_details):
        return remove_tags(job_details['body']['children'][0]['text'])

    def extract_title(self, job_details):
        return remove_tags(job_details['body']['children'][0]['text'])

    def extract_description(self, job_details):
        return remove_tags(job_details['openGraphAttributes']['description'])

    def extract_job_type(self, job_details):
        return job_details['body']['children'][1]['children'][1]['children'][1]['imageLabel']

    def extract_job_date(self, job_details):
        return job_details['body']['children'][1]['children'][1]['children'][0]['imageLabel']
