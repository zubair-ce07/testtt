"""
This module checks data dublications.
"""
from scrapy.exceptions import DropItem


class SheegoPipeline(object):
    """This class checks data dublicates"""

    def __init__(self):
        self.url_seen = set()

    def process_item(self, item, spider):
        """This method check dublications in data"""
        if item['item_detail_url'] in self.url_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.url_seen.add(item['item_detail_url'])
            return item
