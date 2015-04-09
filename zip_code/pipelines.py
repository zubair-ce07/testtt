class ZipCodePipeline(object):

    def process_item(self, item, spider):
        if item.get('cities'):
            item['city'] = max(item['cities'])[1]
            del item['cities']
        if item.get('counties'):
            item['county'] = max(item['counties'])[1]
            del item['counties']
        return item