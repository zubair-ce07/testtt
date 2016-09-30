import base64
import random


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        proxies = ['https://212.191.32.83:8080', 'https://94.20.21.38:8888', 'https://125.16.240.197:8080']
        n =random.randrange(0,3)
        request.meta['proxy'] = proxies[n]
        # Use the following lines if your proxy requires authentication
        #proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        #encoded_user_pass = base64.encodestring(proxy_user_pass)
        #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass