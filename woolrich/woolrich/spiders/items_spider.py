import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ProductsSpider(CrawlSpider):
    name = "products"
    start_urls = [
        'https://www.woolrich.com/'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css="#primary > ul:nth-child(3) > li")),
        Rule(LinkExtractor(restrict_css=".pagination-item--next")),
        Rule(LinkExtractor(restrict_css="#product-listing-container .product article figure"), callback = "parse_item")
    )

    def parse_item(self, response):
        yield {
            'sku': response.css(".parent-sku::text").get(),
            'name': response.css(".productView-title::text").get(),
            'url': response.url,
            'description': response.css("#details-content::text").get(),
            'categories': response.css(".breadcrumb-label::text").getall(),
            'price': response.css(".price.price--withoutTax.bfx-price::text").get(),
            'image-urls': response.css("#zoom-modal img::attr(src)").getall()
        }
