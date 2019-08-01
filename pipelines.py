class OrsayPipeline(object):

    def process_item(self, item, orsay):
        item["price"] = min([item["skus"][sku]["price"] for sku in item["skus"]])
        del item["meta"]
        return item
