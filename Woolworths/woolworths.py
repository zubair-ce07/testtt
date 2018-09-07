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
        Rule(LinkExtractor(allow=[r".*/cat/Women[^?]+", r".*/cat/Men[^?]+", r".*/cat/Kids[^?]+", r".*/cat/Baby[^?]+"]), callback='parse_pages'),
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
        data = self.parse_script_data(response)
        item['brand'] = self.parse_brand(data)
        item['url'] = self.parse_url(response)
        item['name'] = self.parse_name(data)
        item['description'] = self.parse_description(data)
        item['retailer_sku'] = self.parse_retailer_sku(data)
        item['care'] = self.parse_care(response, data)
        item['category'] = self.parse_category(data)
        item['skus'] = self.parse_skus(response, data)
        item['img_urls'] = self.parse_img_urls(data)
        yield item

    def parse_script_data(self, response):
        required_script_xpath = '//script[contains(text(), "productInfo")]/text()'
        script = response.xpath(required_script_xpath).extract_first()
        script = script.lstrip('window.__INITIAL_STATE__ = ')
        data = json.loads(script)
        return data

    def parse_img_urls(self, data):
        aux_media = data['pdp']['productInfo'].get("auxiliaryMedia")
        urls = []
        for item in aux_media.values():
            urls.append("www.woolworths.co.za" + item['internalAuxiliaryImage'])
        return urls

    def parse_brand(self, data):
        product_attributes = data['pdp']['productInfo'].get("productAttributes")
        for attribute in product_attributes:
            if attribute['attributeDisplayName'] == "Brands":
                    return attribute['attributeValue']
        return "Woolworths"

    def parse_care(self, response, data):
        product_attributes = data['pdp']['productInfo'].get("productAttributes")
        care = []
        for attribute in product_attributes:
            if attribute['attributeDisplayName'] == "Care":
                care_url = response.urljoin(attribute['imageURL'])
                return care_url
        return care

    def parse_url(self, response):
        return response.url

    def parse_name(self, data):
        return data['pdp']['productInfo'].get("displayName")

    def parse_description(self, data):
        description = data['pdp']['productInfo'].get("longDescription")
        description_cleaned = self.clean_text(description)
        return description_cleaned

    def clean_text(self, raw_html):
        cleaner = re.compile('<.*?>')
        cleaned_text = re.sub(cleaner, '', raw_html)
        cleaned_text = cleaned_text.replace("\t", "")
        cleaned_text = cleaned_text.replace("\n", "")
        return cleaned_text

    def parse_retailer_sku(self, data):
        return data['pdp']['productInfo'].get("productId")

    def parse_currency(self, data):
        return data['labels']['labelsAndErrorMessages']['cart']['global-minicartpopup-currency-label']

    def parse_category(self, data):
        return data['pdp']['productInfo'].get("productType")

    def parse_skus(self, response, data):
        pdp = data['pdp']
        style_id = pdp['productInfo'].get("defaultStyleId")
        sku_prices = pdp['productPrices'][self.parse_retailer_sku(data)]['plist3620006']['skuPrices']
        sku_details = pdp['productInfo']['styleIdSizeSKUsMap'][style_id]
        skus = {}
        for sku in sku_details:
            product_code = sku['id']
            skus[product_code] = {
                "currency": self.parse_currency(data),
                "colour": sku['colour'],
                "size": sku['size'],
                "price": sku_prices[product_code]['SalePrice']
            }
        return skus

