from linkedin.items import LinkedinProfilesItem
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LinkedinProfilesPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, LinkedinProfilesItem):
            return LinkedinProfilesItem((key, value) for key, value in item.items() if value)
        return item
