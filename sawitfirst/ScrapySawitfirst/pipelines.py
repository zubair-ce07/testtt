import re

from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):

    def __init__(self):
        self.skus_seen = set()
        self.jl_numbers_seen = set()

    def process_item(self, item, spider):
        if item['retailer_sku'] in self.skus_seen or re.findall(r"-(jl\d+-?\d*)$", item['url'])[0] in self.jl_numbers_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.skus_seen.add(item['retailer_sku'])
            self.jl_numbers_seen.add(re.findall(r"-(jl\d+-?\d*)$", item['url'])[0])
            return item
