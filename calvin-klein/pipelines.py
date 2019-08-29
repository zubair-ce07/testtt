class CalvinPipeline(object):
    def process_item(self, item, spider):
        skus = []

        for key, sku in item['skus'].items():
            sku['key'] = key
            skus.append(sku)

        item['skus'] = skus

        return item
