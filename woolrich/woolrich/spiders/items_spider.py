import time
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
        Rule(LinkExtractor(restrict_css=".card-figure"), 
                            callback = "parse_item")
    )

    def parse_item(self, response):
        size_css = (
            '.productView-options .product-size .form-option:not(.unavailable)'
            ' span.form-option-variant::text'
        )
        categories = response.css(".breadcrumb-label::text").getall()
        gender = "Male" if "Men" in categories else "Female" if "Women" in categories else "Unisex"
        yield {
            'sku': response.css(".parent-sku::text").get(),
            'name': response.css(".productView-title::text").get(),
            'url': response.url,
            'date': time.time(),
            'description': response.css("#details-content::text").get(),
            'categories': categories,
            'price': response.css(".price.price--withoutTax.bfx-price::text").get(),
            'gender': gender,
            'image-urls': response.css("#zoom-modal img::attr(src)").getall(),
            'colors': response.css(".productView-options .form-option-variant--pattern::attr(title)").getall(),
            'sizes-available': response.css(size_css).getall()
        }
