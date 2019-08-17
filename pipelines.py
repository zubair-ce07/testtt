class OnlyPipeline(object):
    def process_item(self, item, onlyspider):
        del item["meta"]
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.images = []

    def process_item(self, item, onlyspider):
        for image in item['image_urls']:
            if image in self.images:
                pass
            else:
                self.images.append(image)
        item['image_urls'] = self.images
        self.images = []
        return item
