from scrapy.contrib.spiders import CrawlSpider

class BaseSpider(CrawlSpider):

    def __init__(self, *a, **kw):
        super(BaseSpider, self).__init__(*a, **kw)

    @staticmethod
    def get_text_from_node(node):
        text_array = node.extract()
        if text_array:
            return BaseSpider.normalize(''.join(text_array))
        else:
            return ''

    @staticmethod
    def normalize(data):
        if type(data) is str or type(data) is unicode:
            return BaseSpider.clean(data)
        elif type(data) is list:
            lines = [BaseSpider.clean(x) for x in data]
            return [line for line in lines if line]
        else:
            return data

    @staticmethod
    def clean(data):
        return data.replace("\n", "") \
            .replace("\r", "") \
            .replace("\t", "").strip()
