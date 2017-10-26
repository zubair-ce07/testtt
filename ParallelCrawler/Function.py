import requests
from bs4 import BeautifulSoup
import re


def get_urls(url):

    url_list = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    for link in soup.findAll('a'):

        url = link.get('href')
        if re.match('http', str(url)):
            url_list.append(url)
        else:
            continue

    return url_list