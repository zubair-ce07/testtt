# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline


class CrawlerTasksPipeline(object):
    def process_item(self, item, spider):
        return item


class PhiluItemPipeline(object):
    def process_item(self, item, spider):
        file_urls = [item['course_image']]
        for module in item['lectures']:
            module_image = module.get('module_image')
            if module_image:
                file_urls.append(module_image)

            for unit in module['units']:
                for video in unit['unit_video']:
                    file_urls += [
                        video['url'], video['transcript']
                    ]

        item['file_urls'] = file_urls
        return item


class PhiluFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        id_in_url = request.url.split('?')[0].split('/')[-1]
        return 'full/{}'.format(id_in_url)
