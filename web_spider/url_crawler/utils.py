from bs4 import BeautifulSoup
import requests


def parse_html(response):
    """
    Parse the html string and extract meta data and returns

    Arguments:
        response (Response): string containing html
    Returns:
        size (int): total bytes in html string
        tags_count (int): total tags in html string
        meta_tags_count (int): Meta tags in html
        links (list): List of Link tags containing their href attribute
    """

    # using Beautiful Soup to parse html
    doc = BeautifulSoup(response.text, 'html.parser')
    size = response.headers.get('content-length')

    if size is None:
        size = len(response.text)

    links = [link['href'] for link in doc.find_all('a') if link.get('href') is not None]

    return {
        'size': size,
        'tags_count': len(doc.find_all()),
        'meta_tags': len(doc.find_all('meta')),
        'links': links
    }


class URLSpider:
    """
    This class crawl the given url and retrieve data about the page.
    """

    def __init__(self, url):
        """
        Initializing with url

        Arguments:
            url (str): url address to page to visit
        """
        self.url = url

    def crawl(self):
        """
        crawls the web page located at url.

        Returns:
            result (dict): returns meta data or None if error occurs

        Raises:
            TypeError: if response in not text or status is not OK
            ConnectionError: if connection to URL can not be made
        """
        try:
            response = requests.get(self.url)

            # get type from following string 'text/html; charset=UTF-8'
            content_type = response.headers['content-type'].split(';')[0]

            # check if response is text and charset is UTF-8
            if response.status_code == 200 and content_type == 'text/html':
                return parse_html(response)
            else:
                raise TypeError

        except requests.exceptions.ConnectionError:
            raise ConnectionError
