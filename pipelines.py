class OrsayPipeline(object):

    def process_item(self, item, orsay):
        item["price"] = min([sku["price"] for sku in item["skus"].values()])
        del item["meta"]
        return item
