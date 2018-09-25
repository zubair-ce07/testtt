"""
This module checks data duplications.
"""
from scrapy.exceptions import DropItem


class LornajanePipeline(object):
    """This class checks data duplicates"""

    def __init__(self):
        self.url_seen = set()

    def process_item(self, item, spider):
        """This method check duplications in data"""
        if item['product_code'] in self.url_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.url_seen.add(item['product_code'])
            return item
