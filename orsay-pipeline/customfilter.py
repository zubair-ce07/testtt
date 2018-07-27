import urllib.parse as urlparse

from scrapy.dupefilters import RFPDupeFilter


class SeenURLFilter(RFPDupeFilter):
    def __init__(self, *args, **kwargs):
        self.urls_seen = list()
        super(SeenURLFilter, self).__init__(*args, **kwargs)

    def request_seen(self, request):
        url_parts = urlparse.urlparse(request.url)
        query = dict(urlparse.parse_qsl(url_parts.query))
        if not query:
            return
        data = list(query.values())
        if data in self.urls_seen:
            print('duplicate handled')
            return True
        self.urls_seen.append(data)

    def log(self, request, spider):
        if self.debug:
            msg = 'Custom Filtered duplicate request: %(request)s'
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ('Custom Filtered duplicate request: %(request)s'
                   ' - no more duplicates will be shown'
                   ' (see DUPEFILTER_DEBUG to show all duplicates)')
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)

