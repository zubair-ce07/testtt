import re

from scrapy.dupefilters import RFPDupeFilter

data_url = 'https://www.lindex.com/WebServices/ProductService.asmx/GetProductData'


class Filter(RFPDupeFilter):
    def __getid(self, url):
        return url

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if fp != data_url:
            regex = re.search(r'\d+/(?P<name>.+)/', fp)
            if regex:
                fp = regex.group('name')
            if fp in self.fingerprints:
                return True
            self.fingerprints.add(fp)
