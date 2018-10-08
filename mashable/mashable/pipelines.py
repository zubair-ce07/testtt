from scrapy.exceptions import DropItem


class MashablePipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['story_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)

        self.ids_seen.add(item['story_id'])
        return item
