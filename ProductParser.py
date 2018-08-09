import re
import json

from scrapy import Spider

from hunkemoller.items import HunkemollerItem


class ProductParser(Spider):
    name = "hunkemoller-de-parser"
    brand = "Hunkemoller"
    gender = "women"

    def parse(self, response):
        item = HunkemollerItem()
        item['retailer_sku'] = self.extract_retailer_sku(response)
        item['trail'] = self.extract_trails(response)
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

    def extract_retailer_sku(self, response):
        retailer_sku = response.css('.article-number::text').extract_first()
        return retailer_sku.split(' ')[1]

    def extract_trails(self, response):
        return response.meta.get('trail')

    def extract_product_name(self, response):
        return response.css('.product-name h1::text').extract_first()

    def extract_product_description(self, response):
        raw_description = response.css('.description ::text').extract()
        return list(filter(lambda info: info.strip(), raw_description))

    def extract_product_care(self, response):
        product_tips = response.css('.washing-tips ::text').extract()
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
        return product_details['breadCrumbs']

    def extract_image_urls(self, response):
        raw_urls = response.css(".scroller a::attr(rel)").extract()
        return [json.loads(url).get('zoomimage') for url in raw_urls]

    def extract_sku_model(self, response):
        sku_model_no = json.loads(response.css('::attr(data-additional)').extract_first())
        return list(sku_model_no.keys())[0]

    def extract_skus(self, response):
        skus = {}
        sku_info = {
            'color': self.extract_colors(response)[0],
            'currency': self.extract_currency(response),
            'price': self.extract_price(response)
        }
        for size in response.css('.product-info .selectmenu :not([selected]):not(span)'):
            sku = sku_info.copy()
            sku['size'] = size.css('::text').extract_first().strip()
            skus[self.extract_sku_model(size)] = sku
        return skus
