

class WoolrichItemloaderPipeline(object):
    def process_item(self, item, spider):

        if "skus" in item:
            item["skus"] = {raw_sku["sku"]: raw_sku for raw_sku in item["skus"]}

        return item
