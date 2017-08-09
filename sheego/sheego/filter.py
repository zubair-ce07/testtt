import os

from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import request_fingerprint


class ColorFilter(RFPDupeFilter):
    def __getid(self, url):
        print('*************************')
        print(url)
        url.split('color=')[1]
        print('*************************')
        return url.split('?')[0]

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if fp in self.fingerprints:
            return True
        if 'index' not in fp:
            self.fingerprints.add(fp)
