class OnlyPipeline(object):
    def process_item(self, item, onlyspider):
        del item["meta"]
        return item


class DuplicatesPipeline(object):
    def process_item(self, item, onlyspider):
        images = []
        for image in item['image_urls']:
            if image in images:
                pass
            else:
                images.append(image)
        item['image_urls'] = images
        images.clear()
        return item
