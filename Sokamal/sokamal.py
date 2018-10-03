"""SoKamal Spider"""
import json

import scrapy
from scrapy import FormRequest
from SOKAMAL.items import SokamalLoader


class SokamalSpider(scrapy.Spider):
    """This class basically scrapes the site sokamal.com using specific formdata parameters and ItemLoaders while it
     stores the scraped data in a json file"""
    name = "sokamal"
    start_urls = ["http://sokamal.com/"]

    def parse(self, response):
        url = "https://fishry-api-live.azurewebsites.net/collection_request"
        yield FormRequest(url=url, callback=self.parse_item, method='POST', dont_filter=True,
                          headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                          formdata={"storeID": "480EFD74-078D-4CF2-AC68-270940ED408F", "take": "5000"})

    @staticmethod
    def parse_item(response):
        """Parses response to create product items with the following fields: url, name, brand, description, skus,
        retailer_sku, category, image_urls, barcode"""
        data = json.loads(response.text)
        for product in data:
            loader = SokamalLoader()
            loader.add_value("url", product['productUrl'])
            loader.add_value("name", product['productName'])
            loader.add_value("brand", "Sokamal")
            loader.add_value("description", product['productDescription'])
            loader.add_value("retailer_sku", product['productSKU'])
            loader.add_value("category", product.get('productCollections'))
            loader.add_value("image_urls", product.get('productImage'))
            loader.add_value("skus", product['productVarients'])
            loader.add_value("barcode", product['productBarcode'])
            yield loader.load_item()
