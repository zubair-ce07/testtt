import json
import scrapy


from scrapy import Request
from ..items import Product


class NewLookSpider(scrapy.Spider):
    BASE_URL = "https://www.newlook.com/uk"
    page_no = 1
    next_page = "https://www.newlook.com/uk/womens/sale/c/uk-womens-sale/data-48.json?currency=GBP&language=en&page={}"

    name = 'newlookspider'
    start_urls = [
        f"{BASE_URL}/login"
    ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formnumber=1,
            formdata={
                "j_username": "fahadashraf9612@gmail.com",
                "j_password": "fahad6151774"
            },
            callback=self.redirect_product)

    def redirect_product(self, response):
        link = response.css('li.main-navigation__secondary-menu-item a::attr(href)').extract_first()
        yield Request(self.BASE_URL + link, callback=self.start_scraping)

    def start_scraping(self, response):
        products = response.css("div.plp-item")
        for scraped_product in products:
            product = Product()
            product['name'] = scraped_product.css("div.product-item__details-wrapper span a::text").extract_first()
            product['price'] = scraped_product.css("span.price::text").extract_first()
            yield product
        yield Request(self.next_page.format(self.page_no), method='GET', callback=self.scrap_next_pages)

    def scrap_next_pages(self, response):
        results = json.loads(response.body_as_unicode())["data"]["results"]
        if results:
            for scraped_product in results:
                product = Product()
                product['name'] = scraped_product["name"]
                product['price'] = scraped_product["price"]["formattedValue"]
                yield product
            self.page_no += 1
            yield Request(self.next_page.format(self.page_no), callback=self.scrap_next_pages)
