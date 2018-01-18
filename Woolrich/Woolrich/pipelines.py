from scrapy.exceptions import DropItem


class WoolrichPipeline(object):
    def process_item(self, item, spider):
        prices = []
        previous_prices = []
        for key, value in item['skus'].items():
            prices.append(value['price'])
            previous_prices += [price for price in value['previous_price']]
        item['price'] = min(prices)
        item['previous_price'] = min(previous_prices)
        return item


class ValidationPipeline(object):
    def process_item(self, item, spider):
        if item['previous_price'] and item['price'] > item['previous_price']:
            raise DropItem("Sale price is greater than orignal price %s" % item)
        else:
            return item
