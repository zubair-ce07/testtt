from scrapy.contrib.spiders import CrawlSpider


class BaseSpider(CrawlSpider):
    def __init__(self, *a, **kw):
        super(BaseSpider, self).__init__(*a, **kw)

    def get_text_from_node(self, node):
        text_array = node.extract()
        if text_array:
            return self.normalize(''.join(text_array))
        else:
            return ''

    def get_directory(self, product_id):
        directory_path = 0
        for letter in product_id:
            char_ascii = ord(letter)
            char_ascii = char_ascii * abs(255 - char_ascii)
            directory_path += char_ascii
        directory_path = directory_path % 1023
        directory_path = "{:0>4}".format(directory_path)
        directory_path = "%s/%s" % (directory_path[:2], directory_path[2:])
        return directory_path

    def normalize(self, data):
        if type(data) is str or type(data) is unicode:
            return self.clean(data)
        elif type(data) is list:
            lines = [self.clean(x) for x in data]
            return [line for line in lines if line]
        else:
            return data

    def clean(self, data):
        return data.replace("\n", "") \
            .replace("\r", "") \
            .replace("\t", "").strip()
