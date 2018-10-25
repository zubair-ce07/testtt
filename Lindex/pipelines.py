import re


class LindexPipeline(object):
    def process_item(self, item, spider):
        prices = []
        skus = item["skus"]
        for sku in skus:
            prices.append(sku["price"])

        item["price"] = min(prices)
        item["currency"] = skus[0]["currency"]
        return item
