class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        item.setdefault('assignees', [])
        item.setdefault('industries', [])
        item.setdefault('filings', [])
        item.setdefault('status', 'unknown')
        if not item['status']:
            item['status'] = 'unknown'

        return item