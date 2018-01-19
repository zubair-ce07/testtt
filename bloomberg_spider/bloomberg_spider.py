from items import JobLoader
from urlparse import urljoin
import json
import datetime
import scrapy
import time



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
            url='{}{}'.format('https://careers.bloomberg.com/job_search/search'
                              '_query?jobStartIndex=0&jobBatchSize=',
                              data['totalJobCount']),
            headers={'X-Requested-With': 'XMLHttpRequest'},
            callback=self.get_all_jobs)

    def get_all_jobs(self, response):
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

                job_loader = JobLoader(selector=response)
                job_loader.add_value('business_area', job['Function']['Value'])
                job_loader.add_value('experience_level', job['ExperienceLevel'])
                job_loader.add_value('job_date', job_date)
                job_loader.add_value('job_function', job['Specialty']['Value'])
                job_loader.add_value('location', job['Office']['City'])
                job_loader.add_value('requisition_no', job['JobReqNbr'])
                job_loader.add_value('title', job['JobTitle'])
                job_loader.add_value('url', url)
                yield scrapy.Request(
                    url=url, meta={'item_loader':job_loader},
                    callback=self.parse_job
                )

    def parse_job(self, response):
        job = response.meta['item_loader']
        time_now = datetime.datetime.now().fromtimestamp(time.time()) \
            .strftime('%Y-%m-%d %H:%M:%S.%f')
        job.add_value('crawled_at', time_now)
        job.add_xpath('description', '//div[@class="col-xs-12"]/div[@class='
                                     '"row"]/div[@class="col-xs-12"]//text()')
        job.add_value('provider', 'bloomberg')
        job.add_value('provider_url', 'https://careers.bloomberg.com/')
        return job.load_item()
