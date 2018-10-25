import re


class LindexPipeline(object):
    def process_item(self, item, spider):
        prices = []
        skus = item["skus"]
        for sku in skus:
            prices.append(float(re.findall(r"\d+.\d+", sku["price"])[0]))

        item["price"] = min(price)
        return item
