import requests
import json

from parsel import Selector
from urllib.parse import urljoin


class Product:

    def __init__(self, name, gender, model, price, colors, url, features, in_stock, shipment, details, sizes,
                 image_urls):
        self.name = name
        self.gender = gender
        self.model = model
        self.price = float(price)
        self.colors = colors
        self.url = url
        self.features = features
        self.in_stock = in_stock
        self.shipment = shipment
        self.details = details
        self.sizes = sizes
        self.image_urls = image_urls

    def obj_to_json(self):
        return self.__dict__


def get_html(url):
    with requests.get(url, allow_redirects=False) as response:
        yield response.text or None


def extract_categories(start_url):                          # Returns links of all categories
    sel = Selector(text=next(get_html(start_url)))
    category_links = sel.css("li.nav-item:not(.mobile) a::attr(href)").getall()
    return set(map(lambda url: urljoin(start_url, url), category_links))


def extract_product_urls(url):
    page_no = 0
    page_urls = set()
    while True:
        sel = Selector(text=next(get_html(f'{url}?page={page_no}')))
        links = sel.css('a.productMainLink::attr(href)').getall()
        if not links:
            break
        page_urls |= set((map(lambda link: urljoin(url, link), links)))
        page_no += 1
    return page_urls


def get_product_obj(sel, model_no, product_url):
    product_name = sel.css('h1.single-prod-title::text').get()
    product_gender = sel.css("div#unisex-tab::attr(class)").get()
    product_price = sel.css("div#top-right-info meta[itemprop='price']::attr(content)").get()
    product_colors = sel.css("div#colour-label span.color-label::text").get().split('/')
    product_features = sel.css("div#productFeaturesContent h5::text").getall()
    product_shipping = sel.css("div#info-container > div::text").get()
    product_details = sel.css("div#collapse1 p::text").get() or sel.css("div#collapse1 li::text").getall()
    product_image_urls = sel.css("div#pdp-main-image img.product-img::attr(data-url-src)").getall()
    product_status = sel.css("div#stock-info-container::text").get().strip()
    product_status = False if "Out" in product_status else True
    product_size = list(filter(None, set(size.strip() for size in sel.css("a.SizeOption::text").getall())))

    return Product(product_name, product_gender, model_no, product_price, product_colors, product_url,
                   product_features, product_status, product_shipping, product_details, product_size,
                   product_image_urls)


def crawl(category_links, visited_products):
    myobj = []
    for category in category_links:
        print(category)
        extracted_product_links = extract_product_urls(
            "https://www.asics.com/nz/en-nz/gel-quantum-collection/c/gel-quantum")  # For each category, extract product links to crawl

        for product in extracted_product_links:
            print(f'product=link: {product}')
            html = next(get_html(product))
            if not html:
                continue
            sel = Selector(text=html)
            product_model = sel.css("span[itemprop='model']::text").get().strip()

            if product_model in visited_products:
                continue
            visited_products.add(product_model)
            myobj.append(get_product_obj(sel, product_model, product))
        break
    return myobj


def get_json(pods):
    json_string = json.dumps([obj.obj_to_json() for obj in pods], indent=4)
    print("\n\n", json_string)


def main():
    url = "http://www.asics.com/nz/en-nz/"
    visited_products = set()
    category_links = extract_categories(url)                # links from home page
    pods = crawl(category_links, visited_products)
    get_json(pods)


if __name__ == '__main__':
    main()
