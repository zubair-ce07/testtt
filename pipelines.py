class KleineskarussellPipeline(object):
    def process_item(self, item, spider):
        skus = []

        for sku_id, sku in item['skus'].items():
            sku['key'] = sku_id
            skus.append(sku)
        item['skus'] = skus

        return item

