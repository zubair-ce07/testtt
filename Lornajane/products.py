import json
import re
from html.parser import HTMLParser

import scrapy
from lornajane.items import LornajaneItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import CrawlSpider, Rule
from twisted.internet.error import (DNSLookupError, TCPTimedOutError,
                                    TimeoutError)


class ProductsSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['www.lornajane.sg']
    start_urls = ['http://www.lornajane.sg/']

    rules = (
        Rule(LinkExtractor(
            allow=('https://www.lornajane.sg/c-Shop-All')),
            callback='get_products_list'),
        )

    selectors = {
        "products": ".name::attr(href)",
        "total_products": ".count-text::text",
        "name": ".limitedEdit + h1::text",
        "id": ".mobile_toggle p::text",
        "category": ".breadcrumb ul li a::text",
        "care": ".garment-care p::text",
        "note": ".product-desc > div > div > p:nth-child(3)::text",
        "tech": ".product-desc > div > div > ul:nth-child(6) li::text",
        "style": ".product-desc > div > div > ul:nth-child(9) li::text",
        "note_extra": ".product-desc > div > div > p:nth-child(2)::text",
        "tech_extra": ".product-desc > div > div > ul:nth-child(5) li::text",
        "style_extra": ".product-desc > div > div > ul:nth-child(8) li::text",
        "images": ".aos-item__inner img::attr(src)",
        "main_image": ".pdpBannerImage::attr(style)",
        "currency": ".currency::text",
        "price": ".price::text"
    }

    xpaths = {
        "size": "//a[@class=' product-detail-swatch-btn']/text()",
        "color": "//a[@class='product-detail-swatch-btn selected']/@title",
        "more_colors": "//a[@class='product-detail-swatch-btn ']/@data-url"
    }

    def get_products_list(self, response):
        """Gets all the products list"""

        if "page" in response.meta:
            page = response.meta["page"]
        else:
            page = 0

        yield scrapy.Request(
            url="{}{}".format(
                "https://www.lornajane.sg/c-Shop-All?" +
                "partitial=true&q=&sort=&count=1&page=",
                page),
            callback=self.get_product_urls,
        )

        if page <= int(self.get_total_products(response)):
            yield scrapy.Request(
                url="https://www.lornajane.sg/c-Shop-All",
                callback=self.get_products_list,
                meta={
                    "page": page + 20
                },
                dont_filter=True
            )

    def get_product_urls(self, response):
        """Extracts all the urls of the products in the list loaded"""
        json_data = json.loads(response.body)
        parser = HTMLParser()
        new_response = response.replace(
            body=parser.unescape(json_data['products'])
            )

        urls = new_response.css(
            self.selectors["products"]
        ).extract()
        urls = [response.urljoin(url) for url in urls]

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.get_product
            )

    def get_product(self, response):
        """Getting all the product details and storind it in the item"""

        product_details = {
            '_id': self.get_id(response),
            'brand': "Lornajane",
            'care': [self.get_care(response)],
            'category': self.get_category(response),
            'description': self.get_description(response),
            'gender': "Women",
            'image_urls': self.get_image_urls(response),
            'name': self.get_name(response),
            'retailer_sku': self.get_id(response),
            'skus': self.get_skus(response),
            'url': {response.url}
        }
        item = LornajaneItem(product_details)

        colors = self.more_colors(response)
        if len(colors):
            color_url = colors.pop(0)
            yield scrapy.Request(
                    url=color_url,
                    callback=self.get_skus,
                    errback=self.errback_httpbin,
                    meta={'colors': colors,
                          'item':  item})
        else:
            yield item

    def more_colors(self, response):
        """Checks if the product has more than one color and
        returns the urls"""
        urls = response.xpath(
            self.xpaths["more_colors"]
        ).extract()

        return [response.urljoin(url) for url in urls]

    def get_skus(self, response):
        """Develops skus sturcture and returns it"""
        sizes = self.get_sizes(response)
        image_urls = self.get_image_urls(response)

        skus = {}

        if not sizes:
            sizes.append("One_Sz")

        for size in sizes:
            skus["{}_{}".format(self.get_color(response), size)] = {
                "color": self.get_color(response),
                "currency": self.get_currency(response),
                "price": self.get_price(response),
                "size": size
            }

        if self.has_more_colors(response):
            return self.get_color_variations(response, skus, image_urls)
        else:
            return skus

    def has_more_colors(self, response):
        """Checks if the meta has been initailized with more colors"""
        if 'colors' in response.meta:
            return True
        else:
            return False

    def get_color_variations(self, response, skus, image_urls):
        """Updates the skus according to the provided colors in meta"""
        item = response.meta['item']
        item['skus'].update(skus)
        # Appending new color url
        item['url'].add(response.url)
        # Appending new color images
        item['image_urls'] = item['image_urls'] | image_urls
        if len(response.meta['colors']) == 0:
            yield item
        else:
            colors = response.meta['colors']
            color_url = colors.pop(0)
            yield scrapy.Request(
                    url=color_url,
                    callback=self.get_skus,
                    errback=self.errback_httpbin,
                    meta={'colors': colors,
                          'item':  item})

    # Getters using xpaths and css selectors #

    def get_total_products(self, response):
        total_products = response.css(
            self.selectors["total_products"]
        ).extract()
        return re.findall(r'\d+', total_products[0])[0]

    def get_name(self, response):
        return response.css(
            self.selectors["name"]
        ).extract_first()

    def get_id(self, response):
        _id = response.css(
            self.selectors["id"]
        ).extract_first()
        return re.findall(r'\d+', _id)[0]

    def get_category(self, response):
        breadcrum = response.css(
            self.selectors["category"]
            ).extract()
        return breadcrum[-1]

    def get_care(self, response):
        care = response.css(
                self.selectors["care"]
                ).extract()
        if len(care) > 2:
            return care[1].replace("/", ",")
        else:
            return None

    def get_description(self, response):
        description = set(response.css(
            self.selectors["note"]
        ).extract() + response.css(
            self.selectors["tech"]
        ).extract() + response.css(
            self.selectors["style"]
        ).extract())
        if len(description) > 1:
            return description
        else:
            return set(response.css(
                self.selectors["note_extra"]
            ).extract() + response.css(
                self.selectors["tech_extra"]
            ).extract() + response.css(
                self.selectors["style_extra"]
            ).extract())

    def get_image_urls(self, response):
        images = response.css(
            self.selectors["images"]
        ).extract()
        main_image = response.css(
            self.selectors["main_image"]
        ).extract_first()
        main_image_url = re.findall(r'(\/medias.+\))', main_image)
        if main_image_url:
            main_image_url = main_image_url[0].replace(")", "")
            images.append(main_image_url)
        return {response.urljoin(image) for image in images}

    def get_sizes(self, response):
        return response.xpath(
            self.xpaths["size"]
        ).extract()

    def get_color(self, response):
        return response.xpath(
            self.xpaths["color"]
        ).extract_first()

    def get_currency(self, response):
        currency = set(
            response.css(
                self.selectors["currency"]
            ).extract()
        )
        if currency:
            return currency.pop()

    def get_price(self, response):
        price = response.css(
            self.selectors["price"]
        ).extract()
        if price:
            return price[1]

    def errback_httpbin(self, failure):
        """Error back function for detecting the request errors"""
        # log all failures
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
