import json
import re
from html.parser import HTMLParser

import scrapy
from lornajane.items import LornajaneItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ProductsSpider(CrawlSpider):
    name = 'products'
    allowed_domains = ['www.lornajane.sg']
    start_urls = ['http://www.lornajane.sg/']
    rules = (
        Rule(LinkExtractor(
            allow=('/c-Shop-All')),
            callback='parse_products_list'),
        )

    def parse_products_list(self, response):
        if "page" in response.meta:
            page = response.meta["page"]
        else:
            page = 0

        yield scrapy.Request(
            url="{}{}".format(
                "https://www.lornajane.sg/c-Shop-All?" +
                "partitial=true&q=&sort=&count=1&page=",
                page),
            callback=self.extract_product_urls,
        )
        if page <= int(self.find_total_products(response)):
            yield scrapy.Request(
                url="https://www.lornajane.sg/c-Shop-All",
                callback=self.parse_products_list,
                meta={
                    "page": page + 20
                },
                dont_filter=True
            )

    def extract_product_urls(self, response):
        """Extracts all the urls of the products in the list loaded"""
        json_data = json.loads(response.body)
        parser = HTMLParser()
        new_response = response.replace(
            body=parser.unescape(json_data['products'])
            )
        urls = new_response.css(".name::attr(href)").extract()
        urls = [response.urljoin(url) for url in urls]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        """Getting all the product details and storind it in the item"""

        product_details = {
            '_id': self.find_id(response),
            'brand': "Lornajane",
            'care': [self.find_care_text(response)],
            'category': self.find_category(response),
            'description': self.find_description(response),
            'gender': "Women",
            'image_urls': self.extract_image_urls(response),
            'name': self.find_name(response),
            'retailer_sku': self.find_id(response),
            'skus': self.develop_skus(response),
            'url': {response.url}
        }
        item = LornajaneItem(product_details)

        colors = self.find_more_colors(response)
        if len(colors):
            color_url = colors.pop(0)
            yield scrapy.Request(
                    url=color_url,
                    callback=self.develop_skus,
                    meta={'colors': colors,
                          'item':  item})
        else:
            yield item

    def find_more_colors(self, response):
        urls = response.xpath(
            "//a[@class='product-detail-swatch-btn ']/@data-url").extract()
        return [response.urljoin(url) for url in urls]

    def develop_skus(self, response):
        """Develops skus sturcture and returns it"""
        sizes = self.find_sizes(response)
        image_urls = self.extract_image_urls(response)
        skus = {}

        if not sizes:
            sizes.append("One_Sz")
        for size in sizes:
            skus["{}_{}".format(self.find_color(response), size)] = {
                "color": self.find_color(response),
                "currency": self.find_currency(response),
                "price": self.find_price(response),
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
        item['url'].add(response.url)
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
                          'item':  item}
            )

    def find_total_products(self, response):
        total_products = response.css(".count-text::text").extract()
        return re.findall(r'\d+', total_products[0])[0]

    def find_name(self, response):
        return response.css(".limitedEdit + h1::text").extract_first()

    def find_id(self, response):
        _id = response.css(".mobile_toggle p::text").extract_first()
        return re.findall(r'\d+', _id)[0]

    def find_category(self, response):
        breadcrum = response.css(".breadcrumb ul li a::text").extract()
        return breadcrum[-1]

    def find_care_text(self, response):
        care = response.css(".garment-care p::text").extract()
        if len(care) > 2:
            return care[1].replace("/", ",")
        else:
            return None

    def find_description(self, response):
        return set(response.css(
            ".product-desc > div > div > p:nth-child(3)::text"
        ).extract() + response.css(
            ".product-desc > div > div > ul:nth-child(6) li::text"
        ).extract() + response.css(
            ".product-desc > div > div > ul:nth-child(9) li::text"
        ).extract())

    def extract_image_urls(self, response):
        images = response.css(".aos-item__inner img::attr(src)").extract()
        main_image = response.css(
            ".pdpBannerImage::attr(style)").extract_first()
        main_image_url = re.findall(r'(\/medias.+\))', main_image)
        if main_image_url:
            main_image_url = main_image_url[0].replace(")", "")
            images.append(main_image_url)
        return {response.urljoin(image) for image in images}

    def find_sizes(self, response):
        return response.xpath(
            "//a[@class=' product-detail-swatch-btn']/text()").extract()

    def find_color(self, response):
        return response.xpath(
            "//a[@class='product-detail-swatch-btn selected']/@title"
            ).extract_first()

    def find_currency(self, response):
        currency = set(response.css(".currency::text").extract())
        return currency.pop()

    def find_price(self, response):
        price = response.css(".price::text").extract()
        return price[1]
