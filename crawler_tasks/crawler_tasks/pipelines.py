# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from w3lib.url import url_query_parameter


class CrawlerTasksPipeline(object):
    def process_item(self, item, spider):
        return item


class PhiluItemPipeline(object):
    def process_item(self, item, spider):
        file_urls = []
        # for champ in item['course_champions'].values():
        #     file_urls += [champ['img']]
        # file_urls = [item['course_image']]
        # for did, disc in item['discussions'].items():
        #     file_urls += disc['image_urls']
        #
        # for exercise in item['exercises'].values():
        #     if 'submissions' not in exercise:
        #         continue
        #
        #     for subid, submission in  exercise['submissions'].items():
        #         url = submission['file_url']
        #         if url:
        #             file_urls += [url]
        #
        # for assignment in item['assignments']:
        #     for name, url in assignment['attachments'].items():
        #         file_urls += [url + '?name=' + name]
        #
        # for module in item['lectures']:
        #     module_image = module.get('module_image')
        #     if module_image:
        #         file_urls.append(module_image)
        #
        #     for unit in module['units']:
        #         for pdf in unit['unit_pdf']:
        #             name, url = list(pdf.items())[0]
        #             if 'adlercolvin' in url:
        #                 continue
        #
        #             if 'novoed.com' in url:
        #                 file_urls += [url + '?name=' + name]
        #             else:
        #                 file_urls += [url]
        # for project in item['project']:
        #     for unit in project['units']:
        #         for video in unit['unit_video']:
        #             file_urls += [
        #                 video['url'], video['transcript']
        #             ]
        #
        # item['file_urls'] = file_urls
        return item


class PhiluFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        # id_in_url = request.url.split('?')[0].split('/')[-1]
        id_in_url = url_query_parameter(request.url, 'name')
        id_in_url = id_in_url or request.url.split('?')[0].split('/')[-1]
        return 'full/{}'.format(id_in_url)
