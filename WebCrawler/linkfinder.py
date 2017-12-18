import requests
from bs4 import BeautifulSoup
import re


class LinkFinder:
    def __init__(self):
        self.url = "https://www.ginatricot.com"
        self.start_url = "https://www.ginatricot.com/eu/en/start"
        self.links = set()
        self.products = []

    @staticmethod
    def source_code(url):
        source_code = requests.get(url)
        clean_text = source_code.text
        soup = BeautifulSoup(clean_text, 'lxml')
        return soup

    def complete_url(self, href):
        if 'https' not in href:
            href = self.url + href
        return href

    def findlinks(self, url):
        soup = self.source_code(url)
        for div in soup.find_all('div', {'class': 'content-wrapper'}):
            children = div.findChildren()
            for child in children:
                if child.a:
                    href = child.a.get('href')
                    self.links.add(self.complete_url(href))

    def find_links_category(self, url, queue):
        soup = self.source_code(url)
        span = soup.find('span', {'class': 'pagingContainer'})
        if span:
            children = span.findChildren()
            for child in children:
                href = child.get('href')
                complete_url = self.complete_url(href)
                if complete_url not in queue:
                    self.links.add(complete_url)
                else:
                    self.individual_product(url, queue)
        else:
            self.individual_product(url, queue)

    def individual_product(self, url, queue):
        soup = self.source_code(url)
        product_links = soup.find_all('a', {'class': 'product-link'})
        individual_product = soup.find_all('li', {'class': 'color-mini-square'})
        if product_links:
            for link in product_links:
                href = link.get('href')
                self.links.add(self.complete_url(href))
        elif individual_product:
            for li in individual_product:
                if li.a:
                    href = li.a.get('href')
                    complete_url = self.complete_url(href)
                    if complete_url not in queue:
                        self.links.add(complete_url)
                    else:
                        self.save_product(url)
        else:
            self.save_product(url)

    def page_links(self):
        return self.links

    def save_product(self, link):
        soup = self.source_code(link)
        product = {'name': ''}
        size = ""
        badchar = " \n\r"
        found = ""
        name = soup.find('div', {'class': 'prod-name'})
        price = soup.find('div', {'id': 'productPrice'})
        description = soup.find('div', {'class': 'product-description-box'})
        lis = soup.findAll('li', {'class': 'size-select'})
        if name:
            product['name'] = name.h1.getText()
        if lis:
            for li in lis:
                size += li.getText() + ','
            product['size'] = size
        if price:
            price_text = price.getText()
            for char in badchar:
                price_text = price_text.replace(char, "")
            product['price'] = price_text
        if description:
            text = description.getText()
            text = text.replace('\n', "")
            colour = re.search('Colour\:(.+?)\\r', text)
            if colour:
                found = colour.group(1)
                found = found.replace(" ", "")
                found = found.replace("\r", "")
            product['colour'] = found
        if product['name'] != '':
            self.products.append(product)
