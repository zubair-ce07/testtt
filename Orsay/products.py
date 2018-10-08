import json
import re

import scrapy
from orsay.items import OrsayItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ProductsSpider(CrawlSpider):

    name = 'products'
    allowed_domains = ['www.orsay.com']
    start_urls = [
        'http://www.orsay.com/de-de/',
    ]

    rules = (
        Rule(LinkExtractor(
            allow=(r'/produkte/')),
            callback='parse_product_list'),
        Rule(LinkExtractor(
            allow=(r'/.*[.]html$'),
            deny=('/help/')),
            callback='parse_product')
    )

    def extract_product_urls(self, response):
        """Extracts all the products url for a particular category"""
        products = response.css(
            ".grid-tile .product-image a::attr(href)"
            ).extract()
        return [response.urljoin(url) for url in products]

    def parse_product_list(self, response):
        """Gets all the products list"""
        product_urls = self.extract_product_urls(response)
        next_page = self.has_next_page(response)
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_product_list
            )
        # Sending request for getting products detail
        for product in product_urls:
            yield scrapy.Request(
                url=product,
                callback=self.parse_product,
                dont_filter=True
            )

    def has_next_page(self, response):
        """Finds if the page has more items and returns the link"""
        if response.css("#primary > div.load-more-wrapper > button"):
            url = response.url
            if not self.has_digits(response.url):
                url = response.urljoin("?sz=72")
            total_products = self.find_total_products(response)
            shown_products = int(re.findall(r'\d+', url)[0])
            if (shown_products < total_products):
                return url.replace(str(shown_products), str(shown_products+72))
        else:
            return False

    def has_digits(self, url):
        """Finds the digits in the url and returns it"""
        return any(char.isdigit() for char in url)

    def parse_product(self, response):
        """Getting all the product details and storind it in the item"""
        details = self.parse_product_details(response)
        product_details = {
            '_id': details["productId"],
            'brand': "Orsay",
            'care': self.find_care_text(response),
            'category': details["categoryName"],
            'description': self.find_description(response),
            'gender': "Women",
            'image_urls': self.extract_image_urls(response),
            'name': details["name"],
            'retailer_sku': details["idListRef6"],
            'skus': self.develop_skus(response),
            'url': {response.url}
        }
        item = OrsayItem(product_details)  # Initializing Item

        colors = self.find_more_colors(response)
        if len(colors) > 1:
            color_url = colors.pop(0)
            yield scrapy.Request(
                    url=color_url,
                    callback=self.develop_skus,
                    meta={'colors': colors,
                          'item':  item})
        else:
            yield item

    def clean_care_text(self, care_text):
        """Remove the irrelevant data from the care text"""
        return [c.replace("-", ",") for c in care_text]

    def clean_description(self, details):
        """Remove the irrelevant data from the description"""
        details = [re.sub('\s+', ' ', d).strip() for d in details if d]
        details = [d for d in details if d]
        details.pop(0)
        return details

    def develop_skus(self, response):
        """Develops skus sturcture and returns it"""
        details = self.parse_product_details(response)
        sizes = self.find_sizes(response)
        image_urls = self.extract_image_urls(response)
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
            return self.find_color_variations(response, skus, image_urls)
        else:
            return skus

    def has_more_colors(self, response):
        """Checks if the meta has been initailized with more colors"""
        if 'colors' in response.meta:
            return True
        else:
            return False

    def find_color_variations(self, response, skus, image_urls):
        """Updates the skus according to the provided colors in meta"""
        item = response.meta['item']
        item['skus'].update(skus)
        item['url'].add(response.url)  # Appending new color url
        item['image_urls'] = item['image_urls'] | image_urls
        if len(response.meta['colors']) == 0:
            yield item
        else:
            colors = response.meta['colors']
            color_url = colors.pop(0)
            yield scrapy.Request(
                    url=color_url,
                    callback=self.develop_skus,
                    meta={'colors': colors,
                          'item':  item})

    def parse_product_details(self, response):
        return json.loads(
            response.css(
                ".js-product-content-gtm::attr(data-product-details)"
                ).extract_first()
        )

    def find_description(self, response):
        description = response.css(".product-details div::text").extract()
        return self.clean_description(description)

    def find_care_text(self, response):
        return self.clean_care_text(
            response.css("div.js-material-container p::text").extract()
        )

    def extract_image_urls(self, response):
        images = response.css(".productthumbnail::attr(src)").extract()
        return {re.sub(r'[?].*fit$', "", image) for image in images}

    def find_sizes(self, response):
        sizes = set(response.css(".swatches li.selectable a::text").extract())
        sizes = [re.sub('\s+', ' ', size).strip() for size in sizes if size]
        return [size for size in sizes if size]

    def find_availability(self, response):
        return response.css(".in-stock-msg::text").extract()

    def find_total_products(self, response):
        count = response.css(
            ".pagination-product-count b::text").extract_first()
        count = count.replace(".", "")
        return int(count)

    def find_more_colors(self, response):
        return response.css(".color .selectable a::attr(href)").extract()
