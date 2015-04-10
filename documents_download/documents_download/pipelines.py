# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urlparse import urlparse

from scrapy.contrib.pipeline.files import FilesPipeline
from scrapy.http import Request


class DocumentsDownloadPipeline(FilesPipeline):
    # Overridden method
    def get_media_requests(self, item, info):
        yield Request(url=item["file_url"], meta={"item": item})

    # Overridden method
    def file_path(self, request, response=None, info=None):
        if response:
            item = request.meta['item']
            parsed_url = urlparse(request.url)
            if 'file_location' in item.keys():  # year wise storage
                path_to_file = '%s/%s/%s' % (parsed_url.netloc, item['file_location'], item["file_name"])
            else:
                path_to_file = '%s/%s' % (parsed_url.netloc, item["file_name"])
            if ';' in response.headers['Content-Type']:
                # first split on ';' then on '/'
                extension = response.headers['Content-Type'].split(';')[0].split('/')[1]
            else: # just split on '/'
                extension = response.headers['Content-Type'].split('/')[1]
            if extension == 'msword':
                extension = 'doc'
            return '%s.%s' % (path_to_file, extension)
