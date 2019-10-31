import scrapy
from scrapy.http.request import Request


class AsicsSpider(scrapy.Spider):
    name = 'asics'

    start_urls = [
        "http://www.asics.com/us/en-us/"
    ]

    def start_requests(self):
        yield Request(url="http://www.asics.com/us/en-us/", callback=self.parse_categories)

    def parse_categories(self, response):
        for link in response.css(".show-menu-item::attr(href)").getall():
            page = response.urljoin(f'{link}?start=0')
            yield response.follow(page, callback=self.parse_products)  # going to one layer deep from landing page

    def parse_products(self, response):
        counter = 0
        products = response.css(".product-image a::attr(href)").getall()
        current_product = int(response.request.url.split("start=")[1])
        print(f'Products Count {current_product}')
        for link in products:
            # print(link)
            page = response.urljoin(link)
            yield response.follow(page, callback=self.parse_product)
            counter += 1

        if len(products) > 0:
            page = response.urljoin(f"{response.request.url.split('start=')[0]}start={current_product + counter}")
            yield response.follow(page, callback=self.parse_products)

    def parse_product(self, response):
        description = response.css(".product-info-section-inner::text").get()
        product_name = response.css(".pdp-top__product-name::text").get()
        category = response.css(".product-classification span::text").get()
        image_url = response.css(".thumbnail-link::attr(href)").getall()
        script = response.xpath('//script[@type="text/javascript"]')
        brand = script.re(r'"brand": "(\w+)"')
        currency = script.re(r'"currency": "(\w+)"')
        lang = script.re(r'"language": "(\w+)"')
        gender = script.re(r'"product_gender": \[\n +"(\w+)"')
        price = script.re(r'"product_unit_price": \[\n +"(\w+)"')
        print({'product_name': product_name, 'description': description, 'image_url': image_url, 'brand':brand})
        yield {}

    # def parse_target_links(self, response):
    #     for link in response.css('.art-indexbutton-wrapper .art-indexbutton::attr(href)').extract():
    #         yield response.follow(link, callback=self.parse_docs)  # tracking links leading to the target page
    #
    # def parse(self, response):
    #     items = [item for item in response.css('.titre_12_red::text').extract()]
    #     yield {"categories": items}  # this is where the scraper parses the info
