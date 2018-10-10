# -*- coding: utf-8 -*-
import re
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from eloquiibot.items import EloquiiProduct


class EloquiiSpider(CrawlSpider):
    name = 'eloquii'
    allowed_domains = ['www.eloquii.com']
    start_urls = ['https://www.eloquii.com']

    rules = (
        Rule(
            LinkExtractor(
                allow=(r'https://www.eloquii.com/.*'),
                deny=(r'.*\.html.*')
            )
        ),
        Rule
        (
            LinkExtractor(
                allow=(r'.*\.html.*')
            ),
            callback='parse_product_details'
        )

    )

    def parse_product_details(self, response):
        product = EloquiiProduct()

        product["product_id"] = response.css(
            "#yotpo-bottomline-top-div::attr(data-product-id)"
            ).extract_first()

        product["brand"] = 'Eloquii'
        product["name"] = response.css(
            "#yotpo-bottomline-top-div::attr(data-name)"
            ).extract_first()

        product["category"] = response.css(
            "#yotpo-bottomline-top-div::attr(data-bread-crumbs)"
            ).extract_first()

        product["description"] = response.css(
            "[name=description]::attr(content)"
            ).extract_first()

        if not product["description"]:
            product["description"] = "description isn't available"
        product["url"] = response.url
        product["image_urls"] = self.get_img_urls(response)
        product["skus"] = {}

        merch_info = self.get_merch_info(response)

        if not merch_info:
            product["merch_info"] = "Available"
            product["skus"] = self.get_product_skus(response)
        else:
            product["merch_info"] = merch_info

        yield product

    def get_img_urls(self, response):
        raw_img_url = response.css(
            ".productthumbnails img::attr(src)"
            ).extract()

        img_url = [i.replace("small", "large", 1) for i in raw_img_url]
        img_url = [response.urljoin(i) for i in img_url]

        if not img_url:
            img_url = response.css(
                "div.productimagearea img::attr(src)"
                ).extract_first()
            img_url = response.urljoin(img_url)

        return img_url

    def get_merch_info(self, response):
        merch_info = response.css(
            "h3.text-24.font-demi.mb-3::text"
            ).extract_first()

        if not merch_info:
            merch_info = re.findall(
                r'\'COMINGSOON\': (true|false)', response.text
            )
            if merch_info:
                merch_info = merch_info[0]
                merch_info = "Coming Soon"

        return merch_info

    def get_product_skus(self, response):
        skus = {}
        colours = response.css(
            ".swatchesdisplay a::attr(title)"
            ).extract()
        sizes = response.css(
            "#product_detail_size_drop_down_expanded a::attr(title)"
            ).extract()
        sizes = sizes[1:]

        previous_price = response.css(
            ".priceGroup strike::text"
            ).extract_first()

        price = response.css(".priceGroup span::text").extract_first()

        currency = ''
        if price:
            currency = re.search(r'([^0-9.])', price).group(1)
            price = float(re.search(r'(\d+\.\d+)', price).group(1))

        for colour in colours:
            for size in sizes:
                skus[colour + '_' + size] = {
                    "colour": colour,
                    "currency": currency,
                    "previous_price": previous_price,
                    "price": price,
                    "size": size,
                }
        return skus
