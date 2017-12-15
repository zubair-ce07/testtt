import requests
from bs4 import BeautifulSoup
import re


class GinaSpider:
    def __init__(self):
        self.links = set()
        self.url = "https://www.ginatricot.com"
        self.products_links = set()
        self.individual_products_links = set()
        self.crawled = set()
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

    def gina_spider(self):
        url = 'https://www.ginatricot.com/eu/en/start'
        soup = self.source_code(url)
        for div in soup.find_all('div', {'class': 'content-wrapper'}):
            children = div.findChildren()
            for child in children:
                if child.a:
                    href = child.a.get('href')
                    self.links.add(self.complete_url(href))
        self.product_spider()
        self.product_colour_spider()
        self.save_product()
        print(self.products)

    def product_spider(self):
        for link in self.links:
            soup = self.source_code(link)
            span = soup.find('span', {'class': 'pagingContainer'})
            if span:
                children = span.findChildren()
                for child in children:
                    href = child.get('href')
                    complete_url = self.complete_url(href)
                    self.individual_product(complete_url)
                    self.crawled.add(complete_url)
            else:
                self.individual_product(link)
                self.crawled.add(link)

    def individual_product(self, url):
        if url not in self.crawled:
            soup = self.source_code(url)
            for link in soup.find_all('a', {'class': 'product-link'}):
                href = link.get('href')
                self.products_links.add(self.complete_url(href))

    def product_colour_spider(self):
        for link in self.products_links:
            soup = self.source_code(link)
            for li in soup.find_all('li', {'class': 'color-mini-square'}):
                if li.a:
                    href = li.a.get('href')
                    complete_url = self.complete_url(href)
                    self.individual_products_links.add(complete_url)

    def save_product(self):
        for link in self.individual_products_links:
            soup = self.source_code(link)
            product = {}
            size = ""
            badchar = " \n\r"
            found = ""
            name = soup.find('div', {'class': 'prod-name'})
            price = soup.find('div', {'id': 'productPrice'})
            description = soup.find('div', {'class': 'product-description-box'})
            for li in soup.findAll('li', {'class': 'size-select'}):
                size += li.getText() + ','
            price_text = price.getText()
            for char in badchar:
                price_text = price_text.replace(char, "")
            text = description.getText()
            text = text.replace('\n', "")
            colour = re.search('Colour\:(.+?)\\r', text)
            if colour:
                found = colour.group(1)
                found = found.replace(" ", "")
                found = found.replace("\r", "")
            product['name'] = name.h1.getText()
            product['price'] = price_text
            product['size'] = size
            product['colour'] = found
            self.products.append(product)


def main():
    spider = GinaSpider()
    spider.gina_spider()


if __name__ == '__main__':
    main()
