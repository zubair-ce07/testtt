import base64
import random


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        proxies = ['https://212.191.32.83:8080', 'https://94.20.21.38:8888', 'https://125.16.240.197:8080']
        request.meta['proxy'] = random.choice(proxies)

class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        # Set the location of the proxy
        user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:49.0) Gecko/20100101 Firefox/49.0',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36']
        request.headers.setdefault('User-Agent', random.choice(user_agents))