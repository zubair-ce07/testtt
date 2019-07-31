from scrapy.exceptions import DropItem


class AsicsSpiderPipeline(object):
    @staticmethod
    def process_item(item, spider):
        price = float(item.get("price"))
        if price > 160:
            return item

        raise DropItem(f"{item['name']} priced too low")
