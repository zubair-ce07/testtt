from scrapy.contrib.spiders import CrawlSpider


class BaseSpider(CrawlSpider):

    full_names_of_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    abbreviation_of_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    def __init__(self, *a, **kw):
        super(BaseSpider, self).__init__(*a, **kw)

    def parse_store_hours(self, days, hour_timings, hours, abbreviation_flag=False):
        """
        To parse the given interval of days in to series of days
        e.g
        Mon-Sat (Mon, Tue, Wed, Thu, Fri, Sat)
        """
        start_index, end_index = [self.abbreviation_of_days.index(s.strip()[:3]) for s in days.lower().split('-')]
        if abbreviation_flag:
            for day in self.abbreviation_of_days[start_index:end_index + 1]:
                hours[day.title()] = hour_timings
        else:
            for day in self.full_names_of_days[start_index:end_index + 1]:
                hours[day.title()] = hour_timings

    def get_text_from_node(self, node):
        """
        To extract text from xpath node
        """
        text_array = node.extract()
        return self.normalize(''.join(text_array))

    def normalize(self, data):
        """

        To normalize (spaces) and clean str, list data
        """
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
