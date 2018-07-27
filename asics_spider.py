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
    with requests.get(url) as response:
        yield response.text or ""


def extract_categories(start_url):                                  # Returns links of all categories
    sel = Selector(text=next(get_html(start_url)))
    category_links = sel.css("li.nav-item:not(.mobile) a::attr(href)").getall()
    yield set(map(lambda url: urljoin(start_url, url), category_links))


def extract_product_links(category_links):                          # Return links of all products on site
    product_links = set()
    for category in category_links:
        product_links |= extract_relative_urls(category)
    yield product_links


def extract_relative_urls(url):                                     # Get url of each product for a category
    page_no = 0
    page_urls = set()
    seen_urls = set()
    while True:
        url_sel = Selector(text=next(get_html(f'{url}?page={page_no}')))
        product_links = url_sel.css('a.productMainLink::attr(href)').getall()
        if not product_links:                                       # if next page exists
            break
        seen_urls |= set(product_links)
        if not seen_urls - page_urls:                               # if on the same page
            break
        page_urls |= seen_urls
        page_no += 1                                                # Move to next page
    page_urls = set(map(lambda link: urljoin(url, link), filter(lambda url: "//" not in url, page_urls)))
    return set(filter(lambda url: "onitsukatiger" not in url, page_urls))


def get_product(sel, product_url):                                  # Extract product information
    product_name = sel.css('.single-prod-title::text').get()
    product_gender = sel.css("#unisex-tab::attr(class)").get()
    product_price = sel.css("meta[itemprop='price']::attr(content)").get()
    product_model = sel.css("span[itemprop='model']::text").get().strip()
    product_colors = sel.css("#colour-label span.color-label::text").get().split('/')
    product_features = sel.css("#productFeaturesContent h5::text").getall()
    product_shipping = sel.css("#info-container > div::text").get()
    product_details = sel.css("#collapse1 p::text").get() or sel.css("#collapse1 li::text").getall()
    product_image_urls = sel.css("#pdp-main-image .product-img::attr(data-url-src)").getall()
    product_status = sel.css("#stock-info-container::text").get().strip()
    product_status = False if "Out" in product_status else True
    product_size = list(filter(None, set(size.strip() for size in sel.css("a.SizeOption::text").getall())))

    return Product(product_name, product_gender, product_model, product_price, product_colors, product_url,
                   product_features, product_status, product_shipping, product_details, product_size,
                   product_image_urls)


def crawl(extracted_product_links):
    return [get_product(Selector(text=next(get_html(product))), product) for product in
            extracted_product_links]


def get_json(total_products):
    json_string = json.dumps([product.obj_to_json() for product in total_products], indent=4)
    print("\n\n", json_string)


def main():
    start_url = "http://www.asics.com/nz/en-nz/"
    category_links = next(extract_categories(start_url))
    product_links = next(extract_product_links(category_links))
    total_products = crawl(product_links)
    get_json(total_products)


if __name__ == '__main__':
    main()
