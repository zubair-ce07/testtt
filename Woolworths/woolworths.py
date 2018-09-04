import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from woolworths.items import WoolworthsItem


class WoolworthSpider(CrawlSpider):
    name = "woolworth"
    start_urls = ["https://www.woolworths.co.za"]

    rules = (
        Rule(LinkExtractor(allow=[r".*/cat/Women[^?]+", r".*/cat/Men[^?]+", r".*/cat/Kids[^?]+", r".*/cat/Baby[^?]+"])
             , callback='parse_pages'),
    )

    def parse_pages(self, response):
        total_items = response.xpath('//label[@class="list-options__label"]/text()').extract_first()
        total_items_number = total_items.split()[0]
        for index in range(0, int(total_items_number), 60):
            url = "{}?No={}".format(response.url, str(index))
            yield scrapy.Request(url, callback=self.parse_products)

    def parse_products(self, response):
        sub_urls = response.xpath('//a[@class="product-card__details"]/@href').extract()
        hrefs = []
        for url in sub_urls:
            hrefs.append(response.urljoin(url))
        for href in hrefs:
            yield scrapy.Request(href, callback=self.parse_item)

    def parse_item(self, response):
        item = WoolworthsItem()
        item['brand'] = self.parse_brand(response)
        item['url'] = self.parse_url(response)
        item['name'] = self.parse_name(response)
        item['description'] = self.parse_description(response)
        item['retailer_sku'] = self.parse_retailer_sku(response)
        item['care'] = self.parse_care(response)
        item['category'] = self.parse_category(response)
        item['skus'] = self.parse_skus(response)
        item['img_details'] = self.parse_img_details(response)
        yield item

    def parse_img_details(self, response):
        required_script_xpath = '//script[contains(text(), "window.__INITIAL_STATE__ ")]/text()'
        data = response.xpath(required_script_xpath).extract_first()
        data = data.lstrip('window.__INITIAL_STATE__ = ')
        product_details = json.loads(data)
        img_details = product_details['pdp']['productInfo']['auxiliaryMedia']
        return img_details

    def parse_brand(self, response):
        required_script_xpath = '//script[contains(text(), "window.__INITIAL_STATE__ ")]/text()'
        data = response.xpath(required_script_xpath).extract_first()
        data = data.lstrip('window.__INITIAL_STATE__ = ')
        product_details = json.loads(data)
        try:
            attribute_display_name = product_details['pdp']['productInfo']['productAttributes'][0]['attributeDisplayName']
        except (IndexError, ValueError, KeyError):
            return "Woolworths"
        if attribute_display_name == "Brands":
            return product_details['pdp']['productInfo']['productAttributes'][0]['attributeValue']
        else:
            return "Woolworths"

    def parse_url(self, response):
        return response.url

    def parse_name(self, response):
        return response.xpath('//h1[contains(@class, "font-graphic")]/text()').extract_first()

    def parse_description(self, response):
        return response.xpath('//div[@class="accordion__content--chrome accordion__content"]/ul[1]').extract()

    def parse_retailer_sku(self, response):
        return response.xpath('//ul[@class="list--silent"]/li[2]/text()').extract_first()

    def parse_care(self, response):
        required_script_xpath = '//script[contains(text(), "window.__INITIAL_STATE__ ")]/text()'
        data = response.xpath(required_script_xpath).extract_first()
        data = data.lstrip('window.__INITIAL_STATE__ = ')
        product_details = json.loads(data)
        try:
            care = product_details['pdp']['productInfo']['productAttributes'][1]['imageURL']
        except (IndexError, ValueError, KeyError):
            return "None"
        care_url = response.urljoin(care)
        return care_url

    def parse_category(self, response):
        return response.xpath('//li[@class="breadcrumb__crumb"][3]/a/text()').extract()

    def parse_skus(self, response):
        required_script_xpath = '//script[contains(text(), "window.__INITIAL_STATE__ ")]/text()'
        data = response.xpath(required_script_xpath).extract_first()
        data = data.lstrip('window.__INITIAL_STATE__ = ')
        product = json.loads(data)
        try:
            sku_prices = product['pdp']['productPrices'][self.parse_retailer_sku(response)]['plist3620006']['skuPrices']
        except KeyError:
            sku_prices = "Not mentioned"
        try:
            sku_details = product['pdp']['productInfo']['styleIdSizeSKUsMap']
        except KeyError:
            return
        for values in sku_details.values():
            for value in values:
                value['price'] = sku_prices[value['id']]['SalePrice']
        return sku_details
