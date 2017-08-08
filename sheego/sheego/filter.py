import os

from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import request_fingerprint


class ColorFilter(RFPDupeFilter):
    def __getid(self, url):
        return url.split('?')[0]

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
