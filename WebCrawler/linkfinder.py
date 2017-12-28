from urllib.parse import urljoin


class LinkFinder:
    def __init__(self):
        self.url = "https://www.ginatricot.com"
        self.links = set()
        self.products = []

    def add_links(self, source, xpath):
        self.links.update(urljoin(self.url, u) for u in source.xpath(xpath))

    def findlinks(self, source):
        xpath = "//div[contains(@class, 'content-wrapper')]//ul//li//a/@href"
        self.add_links(source, xpath)

    def find_links_category(self, source):
        product_xpath = "//a[contains(@class, 'product-link')]/@href"
        self.add_links(source, product_xpath)
        page_xpath = "//span[contains(@class, 'pagingContainer')]//a/@href"
        self.add_links(source, page_xpath)
        self.parse_product(source)
        colors_xpath = "//li[contains(@class, 'color-mini-square')]//a/@href"
        self.add_links(source, colors_xpath)

    def parse_product(self, source):
        product = dict()
        product['name'] = self.name(source)
        product['price'] = self.price(source)
        product['size'] = self.sizes(source)
        product['colour'] = self.color(source)
        if product['name'] != '':
            print(product)

    @staticmethod
    def color(source):
        xpath = "//div[contains(@class, 'product-description-box')]/text()"
        description = source.xpath(xpath) or []
        for color in description:
            if 'Colour' in color:
                return "".join(e for e in color if e.isalnum())
        return ""

    @staticmethod
    def name(source):
        xpath = "//div[contains(@class, 'prod-name')]//h1/text()"
        name = source.xpath(xpath) or ['']
        return name[0]

    @staticmethod
    def price(source):
        xpath = "//div[contains(@id, 'productPrice')]/text()"
        price = source.xpath(xpath) or ['']
        return "".join(e for e in price[0] if e.isalnum())

    @staticmethod
    def sizes(source):
        xpath = "//li[contains(@class, 'size-select')]//a/text()"
        sizes = source.xpath(xpath) or []
        return ','.join(sizes)
