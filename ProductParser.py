import json
import re

from scrapy import Spider
from hunkemoller.items import HunkemollerItem


class ProductParser(Spider):
    name = "hunkemoller_parser"
    brand = "Hunkemoller"
    gender = "women"

    def extract_retailer_sku(self, response):
        retailer_sku = response.css('.article-number::text').extract_first()
        return retailer_sku.split(' ')[1] if retailer_sku else None

    def extract_trail(self, response):
        trail = list()
        trail.append(['', 'https://www.hunkemoller.de/de_de/'])
        trail.append(response.meta.get('trail'))
        return trail

    def extract_product_name(self, response):
        return response.css('.product-name h1::text').extract_first()

    def extract_product_description(self, response):
        raw_description = response.css('.description *::text').extract()
        return list(filter(lambda info: info.strip(), raw_description))

    def extract_product_care(self, response):
        product_tips = response.css('.washing-tips *::text').extract()
        return list(filter(lambda tip: tip.strip(), product_tips))

    def extract_price(self, response):
        return response.css(".ratings-wrap span[itemprop='price']::text").extract_first()

    def extract_currency(self, response):
        return response.css("span[itemprop='priceCurrency']::attr(content)").extract_first()

    def extract_colors(self, response):
        return response.css('.product-info .pdp-colors a::attr(title)').extract()

    def extract_category(self, response):
        page_details = response.css('.kega-ddl-script::text').extract_first()
        product_details = json.loads(re.findall('digitalData.page.pageInfo = (.*?);\s*$', page_details, re.M)[0])
        return product_details.get('breadCrumbs')

    def extract_image_urls(self, response):
        raw_urls = response.css(".scroller a::attr(rel)").extract()
        return [json.loads(url).get('zoomimage') for url in raw_urls]

    def extract_sku_model(self, response):
        sku_model_no = response.css('::attr(data-products)').extract_first()
        sku_model_no = re.findall(r'-?\d+\.?\d*', sku_model_no)[0]
        return sku_model_no

    def extract_skus(self, response):
        return [{
            "price": self.extract_price(response),
            "currency": self.extract_currency(response),
            "colour": self.extract_colors(response)[0],
            "size": size.css('::text').extract_first().strip(),
            "sku_id": self.extract_sku_model(size)
        } for size in response.css('.product-info .selectmenu :not([selected]):not(.out-of-stock)')]

    def parse(self, response):
        item = HunkemollerItem()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['trail'] = self.extract_trail(response)
        item['gender'] = self.gender
        item['category'] = self.extract_category(response)
        item['brand'] = self.brand
        item['url'] = response.url
        item['name'] = self.extract_product_name(response)
        item['description'] = self.extract_product_description(response)
        item['care'] = self.extract_product_care(response)
        item['image_urls'] = self.extract_image_urls(response)
        item['skus'] = self.extract_skus(response)
        item['price'] = self.extract_price(response)
        item['currency'] = self.extract_currency(response)
        return item
