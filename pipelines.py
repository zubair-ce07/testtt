class KleineskarussellPipeline(object):
    def process_item(self, item, spider):
        skus = []

        for sku_key, sku in item['skus'].items():
            sku['key'] = sku_key
            skus.append(sku)
        item['skus'] = skus

        return item

