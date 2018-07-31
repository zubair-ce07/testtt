from parsel import Selector


class ProductParser:

    def __init__(self, product_url, product_page_content):
        self.product_url = product_url
        self.url_selector = Selector(text=product_page_content)

    def extract_product_name(self):
        return self.url_selector.css('.single-prod-title::text').get()

    def extract_product_gender(self):
        return self.url_selector.css("#unisex-tab::attr(class)").get()

    def extract_product_price(self):
        return self.url_selector.css("meta[itemprop='price']::attr(content)").get()

    def extract_product_model(self):
        return self.url_selector.css("span[itemprop='model']::text").get().strip()

    def extract_product_colors(self):
        return self.url_selector.css("#colour-label .color-label::text").get().split('/')

    def extract_product_features(self):
        return self.url_selector.css("#productFeaturesContent h5::text").getall()

    def extract_product_shipping(self):
        return self.url_selector.css("#info-container > ::text").get()

    def extract_product_details(self):
        return self.url_selector.css("#collapse1 p::text").get() or self.url_selector.css(
            "#collapse1 li::text").getall()

    def extract_product_image_urls(self):
        return self.url_selector.css("#pdp-main-image .product-img::attr(data-url-src)").getall()

    def extract_product_status(self):
        product_status = self.url_selector.css("#stock-info-container::text").get().strip()
        return False if "Out" in product_status else True

    def extract_product_size(self):
        return list(filter(None, set(size.strip() for size in self.url_selector.css("a.SizeOption::text").getall())))

    def get_product(self):
        return {
            "name": self.extract_product_name(),
            "gender": self.extract_product_gender(),
            "product_model_no": self.extract_product_model(),
            "price": self.extract_product_price(),
            "colors": self.extract_product_colors(),
            "url": self.product_url,
            "features": self.extract_product_features(),
            "in_stock": self.extract_product_status(),
            "shipment": self.extract_product_shipping(),
            "details": self.extract_product_details(),
            "sizes": self.extract_product_size(),
            "image_urls": self.extract_product_image_urls()
        }
