import json
import re

import scrapy
from orsay.items import OrsayItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import CrawlSpider, Rule
from twisted.internet.error import (DNSLookupError, TCPTimedOutError,
                                    TimeoutError)


class ProductsSpider(CrawlSpider):

    name = 'products'
    allowed_domains = ['www.orsay.com']
    start_urls = [
        'http://www.orsay.com/de-de/',
    ]

    extra_links = [
        'http://www.orsay.com/de-de/help/faq.html',
        'http://www.orsay.com/de-de/help/privacy-policy.html',
        'http://www.orsay.com/de-de/help/terms-and-conditions.html',
        'http://www.orsay.com/de-de/help/contact.html',
        'http://www.orsay.com/de-de/help/club-term-conditions.html',
        'http://www.orsay.com/de-de/help/imprimint.html']

    rules = (
        Rule(LinkExtractor(
            allow=(r'http://www.orsay.com/de-de/produkte/.*')),
            callback='get_product_list'),
        Rule(LinkExtractor(
            allow=(r'http://www.orsay.com/de-de/.*[.]html\Z'),
            deny=extra_links),
            callback='get_product',
            follow=True)
    )

    # List of css selectors used in the crawler
    selectors = {
        "products": ".grid-tile .product-image a::attr(href)",
        "next_page": "#primary > div.load-more-wrapper > button",
        "details": ".js-product-content-gtm::attr(data-product-details)",
        "care": "div.js-material-container p::text",
        "images": ".productthumbnail::attr(src)",
        "description": ".product-details div::text",
        "size": ".swatches li.selectable a::text",
        "availability": ".in-stock-msg::text",
        "total_products": ".load-more-progress-label::text",
        "more_colors": ".color .selectable a::attr(href)"
    }

    def extract_product_urls(self, response):
        """Extracts all the products url for a particular category"""
        products = response.css(
            self.selectors["products"]
        ).extract()
        products = [response.urljoin(url) for url in products]
        return products

    def get_product_list(self, response):
        """Gets all the products list"""
        product_urls = self.extract_product_urls(response)
        next_page = self.get_next_page(response)

        if next_page:
            yield scrapy.Request(
                url=next_page,
                errback=self.errback_httpbin,
                callback=self.get_product_list
            )
        # Sending request for getting products detail
        for product in product_urls:
            yield scrapy.Request(
                url=product,
                callback=self.get_product,
                errback=self.errback_httpbin,
                dont_filter=True
            )

    def get_next_page(self, response):
        """Finds if the page has more items and returns the link"""
        check = response.css(
            self.selectors["next_page"]
        )
        if check:
            new_url = response.url
            if not self.has_digits(response.url):
                new_url = response.urljoin("?sz=72")

            total_products = self.get_total_products(response)
            shown_products = re.findall(r'\d+', new_url)[0]

            if (int(shown_products) < int(total_products)):
                return new_url.replace(
                    shown_products, str(int(shown_products) + 72))
            else:
                return None
        else:
            return False

    def has_digits(self, url):
        """Finds the digits in the url and returns it"""
        if any(char.isdigit() for char in url):
            return True
        else:
            return False

    def get_product(self, response):
        """Getting all the product details and storind it in the item"""
        details = self.get_details(response)

        product_details = {
            '_id': details["productId"],
            'brand': "Orsay",
            'care': self.get_care(response),
            'category': details["categoryName"],
            'description': self.get_description(response),
            'gender': "Women",
            'image_urls': self.get_image_urls(response),
            'name': details["name"],
            'retailer_sku': details["idListRef6"],
            'skus': self.get_skus(response),
            'url': {response.url}
        }
        item = OrsayItem(product_details)  # Initializing Item

        colors = self.more_colors(response)
        if len(colors) > 1:
            color_url = colors.pop(0)
            yield scrapy.Request(
                    url=color_url,
                    callback=self.get_skus,
                    errback=self.errback_httpbin,
                    meta={'colors': colors,
                          'item':  item})
        else:
            yield item

    def clean_care_text(self, details):
        """Remove the irrelevant data from the care text"""
        return [
            care.replace("-", ",")
            for care in
            [care.replace(",", "") for care in details]
        ]

    def clean_description(self, details):
        """Remove the irrelevant data from the description"""
        details = [txt.strip() for txt in details]
        details = list(filter(lambda txt: txt != '', details))
        details.pop(0)

        return details

    def get_skus(self, response):
        """Develops skus sturcture and returns it"""
        details = self.get_details(response)
        sizes = self.get_size(response)
        image_urls = self.get_image_urls(response)

        skus = {}

        if not sizes:
            sizes.append("<constant>")

        for size in sizes:
            skus["{}_{}".format(details["color"], size)] = {
                "color": details["color"],
                "currency": details["currency_code"],
                "price": details["grossPrice"],
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

    # Getters using css selectors #

    def get_details(self, response):
        return json.loads(
            response.css(self.selectors["details"]).extract_first()
        )

    def get_description(self, response):
        description = response.css(
            self.selectors["description"]
        ).extract()

        return self.clean_description(description)

    def get_care(self, response):
        return self.clean_care_text(
            response.css(
                self.selectors["care"]
            ).extract()
        )

    def get_image_urls(self, response):
        images = response.css(
            self.selectors["images"]
        ).extract()
        return {re.sub(r'[?].*fit$', "", image) for image in images}

    def get_size(self, response):
        sizes = set(response.css(
            self.selectors["size"]
        ).extract())
        sizes = [re.sub('\s+', ' ', size).strip() for size in sizes if size]
        return [size for size in sizes if size]

    def get_availability(self, response):
        return response.css(
            self.selectors["availability"]
        ).extract()

    def get_total_products(self, response):
        total_products = response.css(
            self.selectors["total_products"]
        ).extract()

        for text in total_products:
            if self.has_digits(text):
                text = text.replace(".", "")
                return re.findall(r'\d+', text)[0]

    def more_colors(self, response):
        colors = response.css(
            self.selectors["more_colors"]).extract()
        return colors

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
