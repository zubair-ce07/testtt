from items import JobLoader
from urlparse import urljoin
import json
import datetime
import scrapy
import time


def concatenate_strings(a, b):
    if b == None:
        return None
    else:
        return '{}{}'.format(a, b)


class BloombergSpider(scrapy.Spider):
    name = 'bloomberg_spider'

    def start_requests(self):
        yield scrapy.Request(
            url='https://careers.bloomberg.com/job_search/search_query?'
                'jobStartIndex=0&jobBatchSize=20',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        yield scrapy.Request(
            url = concatenate_strings('https://careers.bloomberg.com/job_search'
                                   '/search_query?jobStartIndex=0&jobBatchSize'
                                   '=', data['totalJobCount']),
            headers={'X-Requested-With': 'XMLHttpRequest'},
            callback=self.all_jobs)

    def all_jobs(self, response):
        date_format = "%Y-%m-%d"
        date_today = datetime.datetime.strptime(str(datetime.datetime.now()
                                                    .date()), date_format)
        data = json.loads(response.body)
        for job in data['jobData']:
            job_date = job['PostedDate'][:10]
            date_posted = datetime.datetime.strptime(job_date, date_format)
            days_since_posted = date_today-date_posted
            if days_since_posted <= datetime.timedelta(days = int(self.n)):
                url = urljoin('https://careers.bloomberg.com/job/'
                                       'detail/', job['JobReqNbr'])
                yield scrapy.Request(
                    url = url,
                    meta = {
                        'business_area' : job['Function']['Value'],
                        'experience_level' : job['ExperienceLevel'],
                        'job_date': job_date,
                        'job_function' : job['Specialty']['Value'],
                        'location' : job['Office']['City'],
                        'requisition_no' : job['JobReqNbr'],
                        'title' : job['JobTitle'],
                        'url' : url,
                    },
                    callback = self.parse_job
                )

    def parse_job(self, response):
        job = JobLoader(selector=response)
        job.add_value('business_area', response.meta['business_area'])
        time_now = datetime.datetime.now().fromtimestamp(time.time()) \
            .strftime('%Y-%m-%d %H:%M:%S.%f')
        job.add_value('crawled_at', time_now)
        job.add_xpath('description', '//div[@class="col-xs-12"]/div[@class='
                                     '"row"]/div[@class="col-xs-12"]//text()')
        job.add_value('experience_level', response.meta['experience_level'])
        job.add_value('job_date', response.meta['job_date'])
        job.add_value('job_function', response.meta['job_function'])
        job.add_value('location', response.meta['location'])
        job.add_value('provider', 'bloomberg')
        job.add_value('provider_url', 'https://careers.bloomberg.com/')
        job.add_value('requisition_no', response.meta['requisition_no'])
        job.add_value('title', response.meta['title'])
        job.add_value('url', response.meta['url'])
        return job.load_item()
