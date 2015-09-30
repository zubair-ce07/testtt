from HTMLParser import HTMLParser
from urlparse import urlparse
from urlparse import urljoin


class MyParser(HTMLParser):

    def __init__(self, base_url, allowed_domain):
        HTMLParser.__init__(self)
        self.data = []
        self.base_url = base_url
        self.allowed_domain = allowed_domain

    #: Handles both absolute and relative urls
    def handle_starttag(self, tag, attrs):

        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    #: checking special cases  etc "  https://www.quanat.com" and "www.lums.edu.pk"
                    #: check for spaces in the url and remove them
                    url = attr[1]
                    url = url.strip()

                    if url[0] != '/' and url[0:4] != 'http':  #: Append 'http://' if missing else the below
                        url = 'http://' + url                 #: logic will not work

                    #: Check domain of the url whether it is in the allowed domain or not
                    domain = urlparse(url).netloc
                    if domain == '' or domain == self.allowed_domain:
                        parsed_url = urlparse(url).path
                        full_url = urljoin(self.base_url, parsed_url)
                        #: Append '/' at last of the url else 'arbisoft.com' and 'arbisoft.com/'
                        #  will be considered different
                        if full_url[-1] != '/':
                            full_url += '/'
                        self.data.append(full_url)

    def get_data(self):
        return self.data
