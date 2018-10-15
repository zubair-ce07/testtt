# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FlatenPipeline(object):

    def process_item(self, item, spider):
        return convert([dict(item)])


def to_string(s):
    try:
        return str(s)
    except:
        return s.encode('utf-8')


def reduce_item(key, value, reduced_item):
    if type(value) is list:
        i = 0
        for sub_item in value:
            reduce_item(key + '_' + to_string(i), sub_item, reduced_item)
            i = i + 1
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key + '_' + to_string(sub_key), value[sub_key], reduced_item)
    else:
        reduced_item[to_string(key)] = to_string(value)


def convert(raw_data):
        node = "data"

        try:
            data_to_be_processed = raw_data[node]
        except:
            data_to_be_processed = raw_data

        processed_data = []
        header = []
        for item in data_to_be_processed:
            reduced_item = {}
            reduce_item(node, item, reduced_item)

            header += reduced_item.keys()

            processed_data.append(reduced_item)

        header = list(set(header))
        header.sort()
        final_data = {}
        for data in processed_data[0]:
            final_data[data.replace("data_", "")] = processed_data[0][data]

        return final_data
