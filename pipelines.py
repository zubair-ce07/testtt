class UllaPopKenPipeline(object):
    def process_item(self, item, spider):
        item['care'] = [item['care'][0]]
        item['description'] = [item['description'][0]]

        return item
