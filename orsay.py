import re
from datetime import datetime

from scrapy.spiders import CrawlSpider
from scrapy import Field, Item
from scrapy import Request


class OrsayItem(Item):
    name = Field()
    description = Field()
    retailer_sku = Field()
    image_urls = Field()
    care = Field()
    url = Field()
    lang = Field()
    brand = Field()
    category = Field()
    crawl_start_time = Field()
    date = Field()
    crawl_id = Field()
    market = Field()
    retailer = Field()
    gender = Field()
    skus = Field()


class OrsayySpider(CrawlSpider):
    name = "orsayy"
    allowed_domains = ["orsay.com"]
    start_urls = [
        "https://www.orsay.com/de-de/produkte/",
    ]

    retailer = "orsay-de"
    market = "DE"
    language = "de"

    gender = "Women"

    current_products = 0

    def parse(self, response):
        product_css = ".thumb-link::attr(href)"
        product_url = response.css(product_css).getall()
        for url in product_url:
            yield Request(url, callback=self.parse_item)

        pagination_details = self.get_pagination_details(response)
        self.current_products += pagination_details['product_size']

        while self.current_products < pagination_details['max_products']:
            next_page_url = pagination_details['pagination_url'] + str(self.current_products)
            self.current_products += pagination_details['product_size']
            yield Request(next_page_url, callback=self.parse)

    def parse_item(self, response):
        garment = OrsayItem()
        garment["name"] = self.get_product_name(response)
        garment["description"] = self.get_product_description(response)
        garment["retailer_sku"] = self.get_retailer_sku(response)
        garment["image_urls"] = self.get_image_urls(response)
        garment["care"] = self.get_product_care(response)
        garment["url"] = response.url
        garment["lang"] = self.language
        garment["brand"] = self.get_product_brand(response)
        garment["category"] = self.get_product_category(response)
        garment["crawl_start_time"] = datetime.now().isoformat()
        garment["date"] = int(datetime.timestamp(datetime.now()))
        garment["crawl_id"] = self.get_crawl_id()
        garment["market"] = self.market
        garment["retailer"] = self.retailer
        garment["gender"] = self.gender
        garment["skus"] = self.get_product_sku(response)

        yield garment

    def clean(self, string):
        return re.sub(r'\s+', '', string)

    def get_product_name(self, response):
        css = ".product-name::text"
        return response.css(css).get()

    def get_product_description(self, response):
        css = ".with-gutter::text"
        return response.css(css).get()

    def get_retailer_sku(self, response):
        css = ".product-sku::text"
        return response.css(css).get().split(" ", 1)[1]

    def get_image_urls(self, response):
        css = ".productthumbnail::attr(src)"
        return response.css(css).getall()

    def get_product_care(self, response):
        css = ".product-material p::text"
        return response.css(css).get()

    def get_product_brand(self, response):
        css = ".header-logo img::attr(alt)"
        return response.css(css).get()

    def get_product_category(self, response):
        css = ".breadcrumb-element-link span::text"
        return response.css(css).getall()[1]

    def get_crawl_id(self):
        return f"{self.retailer}-{datetime.now().strftime('%Y%m%d-%H%M%s')}-medp"

    def get_pagination_details(self, response):
        pagination_url = "https://www.orsay.com/de-de/produkte/?sz="
        max_products_css = ".js-pagination-product-count::attr(data-count)"
        product_size_css = ".js-custom-select option::attr(value)"
        product_size = int(re.findall(r'\d+', response.css(product_size_css).get())[0])
        max_products = int(response.css(max_products_css).get())
        self.current_products += product_size

        return {
            "pagination_url": pagination_url,
            "max_products": max_products,
            "product_size": product_size
        }

    def get_product_pricing(self, response):
        price_css = ".price-sales::text"
        currency_css = ".country-currency::text"
        previous_price_css = ".price-standard::text"
        previous_price = response.css(previous_price_css).get()

        pricing = {
            "price": self.clean(response.css(price_css).get().split(" ", 1)[0]),
            "currency": response.css(currency_css).get()
        }
        if previous_price:
            pricing["previous_price"] = self.clean(previous_price.split(" ", 1)[0])
        return pricing

    def get_product_sku(self, response):
        skus = {}
        color_css = ".swatchanchor::attr(title)"
        size_css = ".swatchanchor::text"

        common_sku = self.get_product_pricing(response)
        colors = [self.clean(color) for color in response.css(color_css).getall() if color]
        raw_sizes = response.css(size_css).getall()
        sizes = [self.clean(size) for size in raw_sizes if any(element.isdigit() for element in size)] or \
                list(map(lambda size: self.clean(size), raw_sizes))

        for size in sizes:
            for color in colors:
                sku = common_sku.copy()
                sku["size"] = size
                sku["color"] = color
                skus[f"{sku['color']}_{sku['size']}"] = sku

        return skus
