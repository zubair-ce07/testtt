import requests
import json

from parsel import Selector
from urllib.parse import urljoin

concurrent_requests = 30


# manufacturer

class Product:

    def __init__(self, gender, name, price, colors, in_stock, shipment, details, sizes,
                 image_urls):
        self.name = name
        self.gender = gender
        self.price = float(price)
        self.colors = colors
        self.in_stock = in_stock
        self.shipment = shipment
        self.details = details
        self.sizes = sizes
        self.image_urls = image_urls

    def obj_to_json(self):
        return self.__dict__


# def obj_dict(obj):
#     return obj.__dict__


def get_html(url):
    with requests.get(url) as response:
        yield response.text


# def extract_categories(start_url, query_param):  # Returns links of all categories
#     sel = Selector(text=next(get_html(start_url)))
#     category_links = sel.xpath(query_param).getall()
#     # return category_links
#     # return set(map(lambda url: urljoin(start_url, url), category_links))
#     return set(category_links)


def extract_categories(start_url, query_param):  # Returns links of all categories
    sel = Selector(text=next(get_html(start_url)))
    category_links = sel.css(query_param).getall()
    return set(map(lambda url: urljoin(start_url, url), category_links))


def extract_product_urls(url="https://www.asics.com/nz/en-nz/mens-shoes/c/mens-shoes"):
    page_no = 0
    page_urls = set()
    while (True):
        new_url = f'{url}?page={page_no}'
        sel = Selector(text=next(get_html(new_url)))
        links = sel.css('a.productMainLink::attr(href)').getall()
        if not links:
            break
        # page_urls = page_urls.union(set((map(lambda link: urljoin(url, link), links))))
        page_urls |= set((map(lambda link: urljoin(url, link), links)))
        page_no += 1
    return page_urls


# def extract_categories(start_url):  # Returns links of all categories
#     sel = Selector(text=get_html(start_url))
#     category_links = sel.xpath(".//li[@class='nav-item']//a/text()").getall()
#     return set(category_links)


def main():
    url = "http://www.asics.com/nz/en-nz/"
    visited_products = set()
    # category_links = extract_categories(url, ".//li[@class='nav-item']//a/text()")
    category_links = extract_categories(url, "li.nav-item:not(.mobile) a::attr(href)")  # links from home page

    extracted_product_links = extract_product_urls()  # for each home page link, we extract all product links

    # temp = sel.css("p.prod-classification-reference::text").getall()

    for i, link in enumerate(extracted_product_links):
        print(link, f"\n{i}\n")
        sel = Selector(text=next(get_html(link)))
        product_model = sel.css("span[itemprop='model']::text").get().strip()

        if product_model in visited_products:
            continue

        visited_products.add(product_model)
        product_gender = sel.css("div#unisex-tab::attr(class)").get()
        product_url = link
        product_name = sel.css('h1.single-prod-title::text').get()
        product_price = sel.css("div#top-right-info meta[itemprop='price']::attr(content)").get()
        product_colors = sel.css("div#colour-label span.color-label::text").get().split('/')
        product_status = sel.css("div#stock-info-container::text").get().strip()
        product_status = False if "Out" in product_status else True
        product_shipping = sel.css("div#info-container > div::text").get()
        product_details = sel.css("div#collapse1 p::text").get()
        product_image_urls = sel.css("div#pdp-main-image img.product-img::attr(data-url-src)").getall()
        product_features = sel.css("div#productFeaturesContent h5::text").getall()
        product_size = list(filter(None, set(size.strip() for size in sel.css("a.SizeOption::text").getall())))

        print(f"Gender: {product_gender}")
        print(f"url: {product_url}")
        print(f"product_name: {product_name}")
        print(f"product_price: ${product_price}")
        print(f"model: {product_model}")
        print(f"product_color: {product_colors}")
        print(f"Status: {product_status}")
        print(f"Shipment: {product_shipping}")
        print(f"details: {product_details}")
        print(f"Size: {product_size}")
        print(f"Images: {product_image_urls}")
        print(f"Product features: {product_features}")
        # myobj.append(
        #     Product(product_gender, product_name, product_price, product_colors,
        #             product_status, product_shipping, product_details, product_size, product_image_urls))
        #
        # myobj.append(
        #     Product(product_gender, product_name, product_price, product_colors,
        #             product_status, product_shipping, product_details, product_size, product_image_urls))
        #
        # json_string = json.dumps([obj.obj_to_json() for obj in myobj], indent=4)
        #
        # print("\n\n", json_string)
        if i > 4:
            break


if __name__ == '__main__':
    main()