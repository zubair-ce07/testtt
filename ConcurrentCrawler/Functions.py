import requests
import re

from bs4 import BeautifulSoup


def get_urls(url):

    url_list = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        for link in soup.findAll('a') or soup.find_all('link'):
            url = link.get('href')
            if re.match('http', str(url)):
                url_list.append(url)
            else:
                continue

        return url_list

    except Exception:
        print('Wrong Url Entered! Please Enter A valid Website Address')
        exit()
