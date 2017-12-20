from urllib import parse


class LinkFinder:
    def __init__(self):
        self.url = "https://www.ginatricot.com"
        self.links = set()
        self.products = []

    def findlinks(self, source):
        links = source.xpath(
            "//div[contains(@class, 'content-wrapper')]//ul//li//a/@href")
        for link in links:
            href = parse.urljoin(self.url, link)
            self.links.add(href)

    def add_links(self, links):
        for link in links:
            href = parse.urljoin(self.url, link)
            self.links.add(href)

    def find_links_category(self, source):
        product_links = source.xpath(
            "//a[contains(@class, 'product-link')]/@href")
        self.add_links(product_links)
        page_links = source.xpath(
            "//span[contains(@class, 'pagingContainer')]//a/@href")
        self.add_links(page_links)
        self.save_product(source)
        individual_colors = source.xpath(
            "//li[contains(@class, 'color-mini-square')]//a/@href"
        )
        self.add_links(individual_colors)

    def save_product(self, source):
        product = {'name': ''}
        name = source.xpath(
            "//div[contains(@class, 'prod-name')]//h1/text()")
        price = source.xpath(
            "//div[contains(@id, 'productPrice')]/text()"
        )
        description = source.xpath(
            "//div[contains(@class, 'product-description-box')]/text()"
        )
        sizes = source.xpath(
            "//li[contains(@class, 'size-select')]//a/text()"
        )
        product['name'] = self.find_name(name)
        product['price'] = self.find_price(price)
        product['size'] = self.find_size(sizes)
        product['colour'] = self.find_color(description)
        if product['name'] != '':
            print(product)

    @staticmethod
    def find_color(description):
        if len(description) > 0:
            for color in description:
                if 'Colour' in color:
                    return "".join(e for e in color if e.isalnum())
        return ""

    @staticmethod
    def find_name(name):
        if len(name) > 0:
            return name[0]
        return ""

    @staticmethod
    def find_price(price):
        if len(price) > 0:
            return "".join(e for e in price[0] if e.isalnum())
        return ""

    @staticmethod
    def find_size(sizes):
        if len(sizes) > 0:
            size = ""
            for text in sizes:
                size += text + ','
            return size
        return ""
