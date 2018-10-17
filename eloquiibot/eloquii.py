import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from eloquiibot.items import EloquiiProduct


class EloquiiSpider(CrawlSpider):
    name = 'eloquii'
    allowed_domains = ['www.eloquii.com']
    start_urls = ['https://www.eloquii.com']

    listings_css = ['#nav_menu', '.row.justify-content-center.mt-5']
    products_css = ".product-images a"
    merch_map = [("limited edition", "Limited Edition"), ("special edition",
                                                          "Special Edition"), ("discounted", "Discount")]

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product')
    )

    def parse_product(self, response):
        product = EloquiiProduct()
        product["product_id"] = self.product_id(response)
        product["brand"] = 'Eloquii'
        product["name"] = self.product_name(response)
        product["category"] = self.product_category(response)
        product["description"] = self.product_description(response)
        product["url"] = response.url
        product["image_urls"] = self.image_urls(response)
        product["out_of_stock"] = self.out_of_stock(response)
        product["skus"] = {}
        product["merch_info"] = self.merch_info(response, product)
        if self.is_coming_soon(product["merch_info"]) and not product["out_of_stock"]:
            product["skus"] = self.skus(response)
        yield product

    def product_id(self, response):
        css = "#yotpo-bottomline-top-div::attr(data-product-id)"
        return response.css(css).extract_first()

    def product_name(self, response):
        css = "#yotpo-bottomline-top-div::attr(data-name)"
        return response.css(css).extract_first()

    def product_category(self, response):
        css = "#yotpo-bottomline-top-div::attr(data-bread-crumbs)"
        return response.css(css).extract_first()

    def product_description(self, response):
        css = "[name=description]::attr(content)"
        return response.css(css).extract_first()

    def image_urls(self, response):
        css = ".productthumbnails img::attr(src),.productimagearea img::attr(src)"
        image_urls = list(set(response.css(css).extract()))
        return [response.urljoin(i.replace('small', 'large', 1)) for i in image_urls]

    def merch_info(self, response, product):
        soup = ' '.join(product["name"] + product["description"]).lower()
        merch_info = [i[1] for i in self.merch_map if i[0] in soup]
        if bool(re.search(r'\'COMINGSOON\': (true)', response.text)):
            merch_info.append("COMING SOON")
        return merch_info

    def is_coming_soon(self, merch_info):
        if "COMING SOON" not in merch_info:
            return True
        else:
            return False

    def out_of_stock(self, response):
        availability = response.css("[property='og:availability']::attr(content)").extract_first()
        if availability is "IN_STOCK":
            return False
        else:
            return True

    def skus(self, response):
        skus = {}
        colours = response.css(".swatchesdisplay a::attr(title)").extract()
        sizes_css = "#product_detail_size_drop_down_expanded a::attr(title)"
        sizes = response.css(sizes_css).extract()[1:]
        for colour in colours:
            for size in sizes:
                sku = self.product_pricing(response).copy()
                sku['size'] = size
                sku['colour'] = colour
                skus[colour + "_" + size] = sku.copy()
        return skus

    def product_pricing(self, response):
        prices = {}
        previous_price = response.css(".priceGroup strike::text").re_first(r'(\d+\.\d+)')
        prices["price"] = response.css(".priceGroup span::text").re_first(r'(\d+\.\d+)')
        prices["currency"] = response.css("[property='og:price:currency']::attr(content)").extract_first()
        if previous_price:
            prices["previous_price"] = previous_price
        return prices
