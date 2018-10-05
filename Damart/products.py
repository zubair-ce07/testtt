import scrapy
import re
import json
from damart.items import DamartItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class ProductsSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['www.damart.co.uk']
    start_urls = ['http://www.damart.co.uk/']
    rules = (
            Rule(LinkExtractor(
                allow=(r'/C-.*')),
                callback='parse_list'),
            )

    selectors = {
        "products_url": ".photo-data a::attr(href)",
        "name": ".name::text",
        "description": ".product-info li::text, .para_hide::text",
        "care": "#careAdvicesZoneNew div::text",
        "category": ".breadcrum span:nth-child(4) a span::text",
        "images": ".thumblist a::attr(href)",
        "next_page": ".next::attr(href)",
        "color_names": ".picto_color img::attr(alt)",
        "color_urls": ".picto_color a::attr(href)",
        "price": ".sale::text, .sale span::text"
    }

    def parse_list(self, response):
        """Gets all the products list"""
        urls = self.get_product_urls(response)
        next_page = self.get_next_page(response)

        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_list
            )

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_product,
                dont_filter=True
            )

    def parse_product(self, response):
        """Getting all the product details and storind it in the item"""

        product_details = {
            '_id': self.get_id(response),
            'brand': "Damart",
            'care': self.get_care(response),
            'category': self.get_category(response),
            'description': self.get_description(response),
            'image_urls': self.get_images(response),
            'name': self.get_name(response),
            'retailer_sku': "P-" + self.get_id(response),
            'skus': {},
            'url': {response.url}
        }
        item = DamartItem(product_details)

        color_names = self.get_color_names(response)
        color_urls = self.get_color_urls(response)

        if color_urls:
            yield scrapy.Request(
                url=color_urls.pop(0),
                callback=self.get_color_variations,
                headers={
                    "X-Requested-With": "XMLHttpRequest"},
                meta={
                    "item": item,
                    "color_names": color_names,
                    "color_urls": color_urls,
                }
            )
        else:
            yield item

    def get_skus(self, response):
        """Develops skus sturcture and returns it"""
        color_name = (response.meta["color_names"]).pop(0)
        details = self.get_sizes_and_stock_availability(response)
        price = self.get_price(response)

        skus = {}

        for i, size in enumerate(details["sizes"]):
            if "length" in details.keys():
                for length in details["length"]:
                    skus["{}_{}_{}".format(
                        color_name, size, length["text"]
                        )] = {
                        "color": color_name,
                        "currency": "Dollar",
                        "price": price,
                        "size": size
                    }
            else:
                skus["{}_{}".format(color_name, size)] = {
                    "color": color_name,
                    "currency": "Dollar",
                    "price": price,
                    "size": size
                }
            if details["in_stock"]:
                skus[
                    "{}_{}".format(color_name, size)
                    ]["in_stock"] = details["in_stock"][i]

        return skus

    def get_sizes_and_stock_availability(self, response):
        """Parse the json object and returns the specified
        size and stock description"""
        json_data = json.loads(response.body.decode('utf-8'))
        component = json_data['inits'][2]['initDDdSlickComponent']
        ddData = component[0]["ddData"]
        info = {
            "sizes": [],
            "in_stock": []
        }
        if len(component) > 1:
            length = component[1]["ddData"]
            info["length"] = length

        for details in ddData:
            info["sizes"].append(details["text"])
            if "description" in details.keys():
                if "Available" in details["description"]:
                    info["in_stock"].append(True)
                else:
                    info["in_stock"].append(False)
        return info

    def get_price(self, response):
        """Get's the price attribute from the jason data for
        each color"""
        json_data = json.loads(response.body.decode('utf-8'))
        zone = json_data["zones"]

        zone["priceZone"]
        new_response = response.replace(
            body=zone["priceZone"]
            )
        price = new_response.css(
            self.selectors["price"]
        ).extract()

        return "".join(price).split()

    def get_color_variations(self, response):
        """Updates the skus according to the provided colors in meta"""
        if "item" in response.meta:
            color_names = response.meta["color_names"]
            color_urls = response.meta["color_urls"]
            item = response.meta["item"]

            skus = self.get_skus(response)
            item['skus'].update(skus)

            if color_urls:
                yield scrapy.Request(
                    url=color_urls.pop(0),
                    callback=self.get_color_variations,
                    headers={
                        "X-Requested-With": "XMLHttpRequest"},
                    meta={
                        "item": item,
                        "color_names": color_names,
                        "color_urls": color_urls,
                    }
                )
            else:
                yield item

    # Getters using CSS Selectors #

    def get_next_page(self, response):
        return response.urljoin(
            response.css(
                self.selectors["next_page"]
            ).extract_first()
        )

    def get_product_urls(self, response):
        urls = response.css(
            self.selectors["products_url"]
        ).extract()

        return [response.urljoin(url) for url in urls]

    def get_name(self, response):
        return response.css(
            self.selectors["name"]
        ).extract_first()

    def get_id(self, response):
        return re.findall(r"P-(\d*)", response.url)[0]

    def get_description(self, response):
        description = list(set(response.css(
            self.selectors["description"]
        ).extract()))
        return [des.strip() for des in description]

    def get_care(self, response):
        product_care = response.css(
            self.selectors["care"]
        ).extract()

        return [care.strip() for care in product_care if not care == " "]

    def get_category(self, response):
        return response.css(
            self.selectors["category"]
        ).extract_first()

    def get_images(self, response):
        images = response.css(
            self.selectors["images"]
        ).extract()
        return [response.urljoin(image) for image in images]

    def get_color_names(self, response):
        return response.css(
            self.selectors["color_names"]
        ).extract()

    def get_color_urls(self, response):
        color_urls = response.css(
            self.selectors["color_urls"]
        ).extract()
        return [response.urljoin(url) for url in color_urls]

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
