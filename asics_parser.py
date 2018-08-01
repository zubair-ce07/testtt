from parsel import Selector


class ProductParser:

    def __init__(self, product_url, product_page_content):
        self.product_url = product_url
        self.url_selector = Selector(text=product_page_content)

    def extract_product_name(self):
        return self.url_selector.css('.single-prod-title::text').get()

    def extract_product_gender(self):
        return self.url_selector.css("#unisex-tab::attr(class)").get()

    def extract_product_category(self):
        category = self.url_selector.css(".breadcrumb > a::text").get()
        return category.split(' ')

    def extract_product_price(self):
        price = self.url_selector.css("meta[itemprop='price']::attr(content)").get()
        return None if not price else float(price)

    def extract_previous_price(self):
        previous_price = self.url_selector.css("del::text").getall()
        if not previous_price:
            return "none"
        return [float(price[1:]) for price in set(previous_price)]

    def extract_product_model(self):
        return self.url_selector.css("span[itemprop='model']::text").get().strip()

    def extract_product_colors(self):
        return self.url_selector.css("#colour-label .color-label::text").get().split('/')

    def extract_currency(self):
        return self.url_selector.css("meta[itemprop='priceCurrency']::attr(content)").get()

    def extract_product_features(self):
        return self.url_selector.css("#productFeaturesContent h5::text").getall()

    def extract_product_details(self):
        return self.url_selector.css("#collapse1 p::text").get() or self.url_selector.css(
            "#collapse1 li::text").getall()

    def extract_product_image_urls(self):
        return self.url_selector.css("#pdp-main-image .product-img::attr(data-url-src)").getall()

    def extract_product_status(self):
        product_status = self.url_selector.css("#stock-info-container::text").get().strip()
        return False if "Out" in product_status else True

    def extract_total_sizes(self):
        return set(
            filter(None, set(size.strip() for size in self.url_selector.css("a.SizeOption::text").getall())))

    def extract_unavailable_sizes(self):
        return set(
            filter(None, set(size.strip() for size in self.url_selector.css("a.SizeUnavailable::text").getall())))

    def get_skus(self):
        color = self.extract_product_colors()[0]
        total_sizes = self.extract_total_sizes()
        unavailable_sizes = self.extract_unavailable_sizes()

        return [{"color": color, "price": self.extract_product_price(), "currency": self.extract_currency(),
                 "size": size, "previous_prices": self.extract_previous_price(),
                 "out_of_stock": True if size in unavailable_sizes else False,
                 "sku_id": f'{color}_{size}'} for size in total_sizes]

    def get_product(self):
        return {
            "retailer_sku": self.extract_product_model(),
            "gender": self.extract_product_gender(),
            "category": self.extract_product_category(),
            "brand": "Asics Tiger",
            "url": self.product_url,
            "name": self.extract_product_name(),
            "description": self.extract_product_details(),
            "care": self.extract_product_features(),
            "image_urls": self.extract_product_image_urls(),
            "colors": self.extract_product_colors(),
            "skus": self.get_skus()
        }
