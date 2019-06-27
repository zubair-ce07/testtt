import scrapy

class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://www.woolrich.com/'
    ]

    def parse(self, response):
        for link in response.css('#primary > ul:nth-child(3) > li'):
            yield response.follow(link.css('a::attr(href)').get(), self.parse_category)
    def parse_category(self, response):
        for link in response.css('#product-listing-container > form > ul > li'):
            yield response.follow(link.css('article figure a::attr(href)').get(), self.parse_item)
        next_page_css = (
            '#product-listing-container > div > ul > '
            'li.pagination-item.pagination-item--next a::attr(href)'
        )
        next_page = response.css(next_page_css).get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_category)

    def parse_item(self, response):
        yield {
            'href': response.url
        }
