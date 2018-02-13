from items import JobLoader
from scrapy.http import FormRequest
from urlparse import urljoin
import datetime
import json
import scrapy
import time


class InmarSpider(scrapy.Spider):
    name = "inmar_spider"

    def start_requests(self):
        yield scrapy.Request(
            url='https://inmar.wd1.myworkdayjobs.com/inmarcareers',
            headers={'Accept':'application/json,application/xml'},
            callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        facet_values = data['body']['children'][0]['facetContainer']['facets'][0]['facetValues']
        url = urljoin('https://inmar.wd1.myworkdayjobs.com', data['body']['children'][0]['endPoints'][4]['uri'])
        for value in facet_values:
            yield FormRequest(
                url= url,
                formdata= {
                    'facets':'jobFamilyGroup',
                    'jobFamilyGroup': value['iid'],
                },
                headers={'Accept': 'application/json,application/xml'},
                callback=self.filter_by_category,
                meta={'category':value['label']}
            )

    def filter_by_category(self, response):
        data = json.loads(response.body)
        list_items = data['body']['children'][0]['children'][0]['listItems']
        for item in list_items:
            yield scrapy.Request(
                url=urljoin('https://inmar.wd1.myworkdayjobs.com',
                                     item['title']['commandLink']),
                headers={'Accept': 'application/json,application/xml'},
                callback=self.parse_job,
                meta={'category': response.meta['category']}
            )

    def parse_job(self, response):
        job = JobLoader(selector=response)
        data = json.loads(response.body)
        job_attributes = data['body']['children'][1]['children']
        job.add_value('category', response.meta['category'])
        time_now = datetime.datetime.now().fromtimestamp(time.time()) \
            .strftime('%Y-%m-%d %H:%M:%S.%f')
        job.add_value('crawled_at', time_now)
        description = data['openGraphAttributes']['description']
        job.add_value('description', description)
        job_id = job_attributes[1]['children'][2]['imageLabel']
        job.add_value('job_id', job_id)
        job_date = job_attributes[1]['children'][0]['imageLabel']
        job.add_value('job_date', job_date)
        job_url = data['openGraphAttributes']['url']
        job.add_value('job_url', job_url)
        job_type = job_attributes[1]['children'][1]['imageLabel']
        job.add_value('job_type', job_type)
        locations = job_attributes[0]['children'][0]['imageLabel']
        job.add_value('locations', locations)
        job.add_value('provider', 'inmar')
        title = data['body']['children'][0]['text']
        job.add_value('title', title)
        return job.load_item()
