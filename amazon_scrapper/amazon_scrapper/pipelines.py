import json
from scrapy.exceptions import DropItem


class JsonWriterPipeline(object):

    def open_spider(self, __):
        self.file = open('products.jl', 'w')

    def close_spider(self, __):
        self.file.close()

    def process_item(self, item, __):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.asin_seen = set()

    def process_item(self, item, __):
        asin = item['ASIN']

        if asin in self.asin_seen:
            raise DropItem("Duplicate item found: %s" % item)

        self.asin_seen.add(asin)
        return item
