import scrapy
from vans.items import VansItem
from scrapy.spiders import CrawlSpider
import json
import re
from scrapy.http import HtmlResponse
from urllib.parse import urlencode


class VansParser(CrawlSpider):
    name = "vans_parser"
    start_urls = ["https://www.vans.co.uk/"]
    skus_api = "https://www.vans.co.uk/webapp/wcs/stores/servlet/VFAjaxProductAvailabilityView?"

    genders = {
        "WOMEN": "Women",
        "MEN": "Men",
        "KIDS": "Kids",
    }

    def product_id(self, response):
        return response.xpath('//input[@name="catEntryId"]/@value').extract_first()

    def attribute_id(self, response):
        return response.xpath('//section/@data-attribute-id').extract_first()

    def product_info(self, response):
        product_info = response.xpath('//script[contains(text(),"itemPrices")]/text()').extract_first()
        return json.loads(re.findall('Prices = (.+);', product_info)[0])

    def colour(self, response):
        return response.css('.attr-selected-color-js ::text').extract_first()

    def sku_ids_url(self, response):
        params = {
            'storeId': response.xpath('//meta[@name="storeId"]/@content').extract_first(),
            'langId': response.xpath('//meta[@name="langId"]/@content').extract_first(),
            'productId': self.product_id(response),
            'requesttype': 'ajax',
        }
        return self. skus_api+urlencode(params)

    def gender(self, response):
        gender_info = response.xpath('//script[contains(text(),"pageName")]/text()').extract_first()
        category = re.findall('Name":"[A-Z]+', gender_info)[0][7:]
        return self.genders.get(category) or 'Adults'

    def parse_product(self, response):
        item = VansItem()
        item["title"] = response.xpath('//h1[@class="product-info-js"]/text()').extract()
        item["description"] = response.css('.desc-container::text').extract()[0]
        item["composition"] = response.css('.desc-container::text').extract()[1:]
        item["retailer_id"] = self.product_id(response)
        item["url"] = response.url
        item["images_url"] = response.css('.selected-view-js img::attr(src)').extract()
        item["gender"] = self.gender(response)

        yield scrapy.Request(url=self.sku_ids_url(response), meta={"item": item, "colour": self.colour(response)},
                             dont_filter=True, callback=self.skus_output)

    def price_details(self, sku_ids_content):
        price_html = sku_ids_content["productPriceHTML"]
        price_html = (price_html.replace('&lt;', '<').replace('&gt;', '>').replace('&#034;', '').replace('&amp;', '&'))
        new_response = HtmlResponse(url="", body=price_html, encoding='utf-8')
        return new_response

    def previous_price(self, new_response):
        previous_price = new_response.css('.product-block-price::text').extract_first()
        return previous_price.strip() if previous_price else "None"

    def stock_information(self, sku_ids_content):
        available_sku_ids = []
        for sku_key, sku_value in sku_ids_content["stock"].items():
            if sku_value != 0:
                available_sku_ids.append(sku_key)
        return available_sku_ids

    def price(self, new_response):
        return new_response.xpath('//span/text()').extract()[-1].strip()

    def skus(self, new_response, sku_ids_content):
        sizes_and_sku_ids = sku_ids_content["attributes"]["7000000000000013954"]
        skus = {}
        for size_and_sku_id in sizes_and_sku_ids:
            if str(size_and_sku_id["catentryId"][0]) in self.stock_information(sku_ids_content):
                skus[size_and_sku_id["catentryId"][0]] = {
                    "size": size_and_sku_id["display"],
                    "stock": "available",
                    "price": self.price(new_response),
                    "previous_price": self.previous_price(new_response),
                }
            else:
                skus[size_and_sku_id["catentryId"][0]] = {
                    "size": size_and_sku_id["display"],
                    "stock": "out_of_stock",
                    "price": self.price(new_response),
                    "previous_price": self.previous_price(new_response),
                }
        return skus

    def skus_output(self, response):
        item = response.meta["item"]
        if response.text:
            sku_ids_content = json.loads(response.text)
            new_response = self.price_details(sku_ids_content)
            item["skus"] = self.skus(new_response, sku_ids_content)
        yield item
