from scrapy.exceptions import DropItem


class DuplicatesPipeline:

    def __init__(self):
        self.skus_seen = set()

    def process_item(self, item, spider):
        if item['retailer_sku'] in self.skus_seen:
            raise DropItem("Duplicate item found: %s" % item)
        self.skus_seen.add(item['retailer_sku'])
        return item
