
from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['retailer_sku'] in self.ids_seen:
            raise DropItem("{}Duplicate item found: {}{}".format("\033[1;31m", item, "\033[1;m"))
        else:
            self.ids_seen.add(item['retailer_sku'])
            return item
