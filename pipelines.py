class KleineskarussellPipeline(object):
    def process_item(self, item, spider):
        flat_sku = []

        for key, sku in item['skus'].items():
            sku['key'] = key
            flat_sku.append(sku)
        item['skus'] = flat_sku

        return item
