from scrapy.exceptions import DropItem


class OrsayPipeline(object):
    """Pipeline for removing duplicates"""

    def __init__(self):
        self.ids = set()

    def process_item(self, item, spider):
        if item['_id'] in self.ids:
            print("Duplicate Found: ", item["_id"])
            raise DropItem("Duplicate item found: %s" % item)

        self.ids.add(item['_id'])
        return item
