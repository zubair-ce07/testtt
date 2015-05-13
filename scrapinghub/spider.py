from scrapy.contrib.spiders import CrawlSpider


class BaseSpider(CrawlSpider):

    list_of_days = [u'mon', u'tue', u'wed', u'thu', u'fri', u'sat', u'sun',
                    u'monday', u'tuesday', u'wednesday', u'thursday', u'friday', u'saturday', u'sunday']

    def parse_store_hours(self, days, hour_timings, hours):
        i, j = [self.list_of_days.index(s.strip()) for s in days.strip(':').lower().split('-')]
        for day in self.list_of_days[i:j + 1]:
            hours[day.title()] = hour_timings

    def __init__(self, *a, **kw):
        super(BaseSpider, self).__init__(*a, **kw)

    def get_text_from_node(self, node):
        text_array = node.extract()
        if text_array:
            return self.normalize(''.join(text_array))
        else:
            return ''

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
