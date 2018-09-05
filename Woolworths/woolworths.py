import json
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from woolworths.items import WoolworthsItem


class WoolworthSpider(CrawlSpider):
    name = "woolworths"
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
        for url in sub_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_item)

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
        item['img_urls'] = self.parse_img_urls(response)
        yield item

    def parse_script_data(self, response):
        required_script_xpath = '//script[contains(text(), "productInfo")]/text()'
        script = response.xpath(required_script_xpath).extract_first()
        script = script.lstrip('window.__INITIAL_STATE__ = ')
        data = json.loads(script)
        return data

    def parse_img_urls(self, response):
        data = self.parse_script_data(response)
        aux_media = data['pdp']['productInfo'].get("auxiliaryMedia")
        urls = []
        for item in aux_media.values():
            urls.append("www.woolworths.co.za" + item['internalAuxiliaryImage'])
        return urls

    def parse_brand(self, response):
        data = self.parse_script_data(response)
        product_attributes = data['pdp']['productInfo'].get("productAttributes")
        for attribute in product_attributes:
            if attribute['attributeDisplayName'] == "Brands":
                if attribute['attributeValue']:
                    return attribute['attributeValue']
            else:
                return "Woolworths"

    def parse_care(self, response):
        data = self.parse_script_data(response)
        product_attributes = data['pdp']['productInfo'].get("productAttributes")
        for attribute in product_attributes:
            if attribute['attributeDisplayName'] == "Care":
                care_url = response.urljoin(attribute['imageURL'])
                return care_url

    def parse_url(self, response):
        return response.url

    def parse_name(self, response):
        data = self.parse_script_data(response)
        return data['pdp']['productInfo'].get("displayName")

    def parse_description(self, response):
        data = self.parse_script_data(response)
        description = data['pdp']['productInfo'].get("longDescription")
        description_cleaned = self.clean_text(description)
        return description_cleaned

    def clean_text(self, raw_html):
        cleaner = re.compile('<.*?>')
        cleaned_text = re.sub(cleaner, '', raw_html)
        cleaned_text = cleaned_text.replace("\t", "")
        cleaned_text = cleaned_text.replace("\n", "")
        return cleaned_text

    def parse_retailer_sku(self, response):
        data = self.parse_script_data(response)
        return data['pdp']['productInfo'].get("productId")

    def parse_currency(self, response):
        data = self.parse_script_data(response)
        return data['labels']['labelsAndErrorMessages']['cart']['global-minicartpopup-currency-label']

    def parse_category(self, response):
        data = self.parse_script_data(response)
        return data['pdp']['productInfo'].get("productType")

    def parse_skus(self, response):
        data = self.parse_script_data(response)
        pdp = data['pdp']
        style_id = pdp['productInfo'].get("defaultStyleId")
        sku_prices = pdp['productPrices'][self.parse_retailer_sku(response)]['plist3620006']['skuPrices']
        sku_details = pdp['productInfo']['styleIdSizeSKUsMap'][style_id]
        for index in range(len(sku_details)):
            product_code = sku_details[index]['id']
            if index == 0:
                skus = {
                    product_code: {
                        "currency": self.parse_currency(response),
                        "colour": sku_details[index]['colour'],
                        "size": sku_details[index]['size'],
                        "price": sku_prices[product_code]['SalePrice']
                    }
                }
            else:
                skus[product_code] = {
                    "currency": self.parse_currency(response),
                    "colour": sku_details[index]['colour'],
                    "size": sku_details[index]['size'],
                    "price": sku_prices[product_code]['SalePrice']
                }
        return skus

