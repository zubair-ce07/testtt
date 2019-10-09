from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):

    def __init__(self):
        self.retailer_sku_seen = set()

    def process_item(self, item, spider):
        if item['retailer_sku'] in self.retailer_sku_seen:
            raise DropItem(f'Duplicate item found: {item}')
        else:
            self.retailer_sku_seen.add(item['retailer_sku'])

            return item
