class DuplicatesRemovalPipeline(object):

    def __init__(self):
        self.processed_product_items = set()

    def process_item(self, item, spider):
        if 'retailer_sku' in item.keys():
            if item['retailer_sku'] in self.processed_product_items:
                raise DropItem(f"A duplicate item found: {item['retailer_sku']}")
            self.processed_product_items.add(item['retailer_sku'])

        return item
