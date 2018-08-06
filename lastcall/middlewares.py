from scrapy import signals


class CustomHeaderMiddleware(object):
    header = {'Accept-Language': 'en',
              'Accept-Encoding': 'gzip,deflate',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)' +
                            ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
              'Content- Type': 'application/x-www-form-urlencoded;charset = UTF-8',
              'Accept': '*/*',
              'X-Requested-With': 'XMLHttpRequest'
              }

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for request in start_requests:
            if 'request' in str(type(request)):
                request.headers.update(self.header)
            yield request

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for item in result:
            if 'request' in str(type(item)):
                item.headers.update(self.header)
            yield item
