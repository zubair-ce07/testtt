class DuplicatesRemovalPipeline(object):

    def __init__(self):
        self.seen_ids = set()

    def process_item(self, item, spider):
        if 'retailer_sku' in item.keys():
            if item['retailer_sku'] in self.seen_ids:
                raise DropItem(f"A duplicate item found: {item['retailer_sku']}")
            self.seen_ids.add(item['retailer_sku'])

        return item
