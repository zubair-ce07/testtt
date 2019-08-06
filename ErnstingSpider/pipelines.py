from scrapy.exceptions import DropItem


class ErnstingSpiderPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item["product_id"] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.ids_seen.add(item["product_id"])
            return item

