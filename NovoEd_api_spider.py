# -*- coding: utf-8 -*-
import json
import os
import re
from copy import deepcopy

import scrapy
from  scrapy.http import Request


class NovoEdSpider(scrapy.Spider):
    name = 'NovoEd'
    api_key = 'TMQthsAI2JTwD0IiXqVU3wtt'
    custom_settings = {
        'DOWNLOAD_DELAY': 6,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
    }
    api_secret = 'w9wzIszIKGGGSk4IxjBIEQtt'

    already_visited_links = []
    error_files = []
    error_count = 0

    urls = ['https://api.novoed.com/{0}/learner_info_in_course.json?api_key={1}&api_secret={2}',
            'https://api.novoed.com/{0}/learners_in_course.json?api_key={1}&api_secret={2}',
            'https://api.novoed.com/{0}/learner_participation_details_in_course.json?api_key={1}&api_secret={2}',
            'https://api.novoed.com/{0}/learner_participation_in_course.json?api_key={1}&api_secret={2}'
            ]

    course_catalogs = [
        ("Philanthropy U program space", ["philanthropy-initiative"]),

        ("Fall 2015", ["philanthropy-university-strategy",
                       "philanthropy-university-capacity",
                       "philanthropy-university-fundraising",
                       "philanthropy-university-leadership",
                       "philanthropy-university-scale",
                       "philanthropy-university-entrepreneurship",
                       "philanthropy-university-financial-modeling"]),

        ("2016 Session 1", ["strategy-2016-1",
                            "capacity-2016-1",
                            "fundraising-2016-1",
                            "leadership-2016-1",
                            "scale-2016-1",
                            "entrepreneurship-2016-1",
                            "financial-modeling-2016-1"]),

        ("2016 Session 2", ["strategy-2016-2",
                            "capacity-2016-2",
                            "fundraising-2016-2",
                            "leadership-2016-2",
                            "scale-2016-2",
                            "entrepreneurship-2016-2",
                            "financial-modeling-2016-2"]),

        ("2016 Session 3", ["strategy-2016-3",
                            "capacity-2016-3",
                            "fundraising-2016-3",
                            "leadership-2016-3",
                            "scale-2016-3",
                            "entrepreneurship-2016-3",
                            "financial-modeling-2016-3"]),

        ("2016 Session 4", ["strategy-2016-4",
                            "capacity-2016-4",
                            "fundraising-2016-4",
                            "leadership-2016-4",
                            "scale-2016-4",
                            "entrepreneurship-2016-4",
                            "financial-modeling-2016-4"]),

        ("2017 Session 1", ["strategy-2017-1",
                            "fundraising-2017-1",
                            "leadership-2017-1",
                            "scale-2017-1",
                            "entrepreneurship-2017-1",
                            "financial-modeling-2017-1"]),

        ("2017 Session 2", ["strategy-2017-2",
                            "fundraising-2017-2",
                            "leadership-2017-2",
                            "scale-2017-2",
                            "entrepreneurship-2017-2",
                            "financial-modeling-2017-2",
                            "capacity-2017-2"])
    ]

    def check_file(self, url, session, course_id, page_no):
        end_point_data = re.findall('.com\/.*\/(.*)?.json', url)[0]
        directory_path = 'output_test/NovoEdData/{end_point}/{session}/{course_id}'.format(
            end_point=end_point_data,
            session=session,
            course_id=course_id
        )
        self.create_directory(directory_path)

        filename = '{dir}/{page}.json'.format(dir=directory_path, page=page_no)
        return os.path.exists(filename)

    def start_requests(self):

        for url in self.urls:
            for session, courses in self.course_catalogs:

                for course_id in courses:
                    link = url.format(course_id, self.api_key, self.api_secret)
                    meta = {'session': session, 'course_id': course_id}
                    req = Request(link, meta=deepcopy(meta), callback=self.parse_page)
                    yield req

    def parse_page(self, response):
        response_json = json.loads(response.body)
        total_pages = response_json['result']['meta_data']['page_count']
        for page_num in range(1, total_pages + 1):
            url = '{0}&page={1}'.format(response.url, page_num)
            if self.check_file(url, response.meta["session"], response.meta["course_id"], page_num):
                print("skipping: ", url)
            else:
                self.already_visited_links.append(url)
                yield Request(url, meta=response.meta, callback=self.parse_page_results)

    def parse_page_results(self, response):
        response_json = json.loads(response.body)
        current_page_no = response_json['result']['meta_data']['page_num']
        total_pages = response_json['result']['meta_data']['page_count']

        yield self.save_data(response, current_page_no, total_pages)

    def save_data(self, response, current_page_no, total_pages):
        end_point_data = re.findall('.com\/.*\/(.*)?.json', response.url)[0]
        directory_path = 'output/NovoEdData/{end_point}/{session}/{course_id}'.format(
            end_point=end_point_data,
            session=response.meta['session'],
            course_id=response.meta['course_id']
        )
        self.create_directory(directory_path)

        filename = '{dir}/{page}.json'.format(dir=directory_path, page=current_page_no)
        outfile = open(filename, 'w')
        item = {
            'url': response.url,
            # 'body':response.body,
            'endpoint': end_point_data,
            'session': response.meta['session'],
            'course_id': response.meta['course_id']
        }
        outfile.write(response.body)
        outfile.close()

        self.logger.info("File Saved: {end_point} > {session} > {course_id} > Page {page} / {total_pages}".format(
            end_point=end_point_data,
            session=response.meta['session'],
            course_id=response.meta['course_id'],
            page=current_page_no,
            total_pages=total_pages
        ))
        return item

    def create_directory(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

