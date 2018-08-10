import re
import json

from scrapy import Spider

from hunkemoller.items import HunkemollerItem


class ProductParser(Spider):
    name = "hunkemoller-de-parser"
    brand = "Hunkemoller"
    gender = "women"
    category_regex = re.compile('pageInfo = (.*?);\s*$', re.M)

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
        return retailer_sku.split()[1]

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
        return response.css(".ratings-wrap [itemprop='price']::text").extract_first()

    def extract_currency(self, response):
        return response.css("[itemprop='priceCurrency']::attr(content)").extract_first()

    def extract_colors(self, response):
        return response.css('.product-info .pdp-colors ::attr(title)').extract()

    def extract_category(self, response):
        page_details = response.css('.kega-ddl-script::text').extract_first()
        product_details = json.loads(re.findall(self.category_regex, page_details)[0])
        return product_details['breadCrumbs']

    def extract_image_urls(self, response):
        raw_urls = response.css(".scroller ::attr(rel)").extract()
        return [json.loads(url).get('zoomimage') for url in raw_urls]

    def extract_sku_sizes(self, response):
        raw_sku_sizes = response.css('.product-info .selectmenu :not([selected]):not(span) ::text').extract()
        return [size.strip() for size in raw_sku_sizes]

    def extract_sku_models(self, response):
        raw_sku_models = response.css(
            '.product-info .selectmenu :not([selected]):not(span) ::attr(data-additional)').extract()
        return [list(json.loads(sku_model).keys())[0] for sku_model in raw_sku_models]

    def extract_skus(self, response):
        sku_sizes = self.extract_sku_sizes(response)
        sku_models = self.extract_sku_models(response)
        sku_info = {
            'color': self.extract_colors(response)[0],
            'currency': self.extract_currency(response),
            'price': self.extract_price(response)
        }
        skus = {}
        for sku_model, size in zip(sku_models, sku_sizes):
            sku = sku_info.copy()
            sku['size'] = size
            skus[sku_model] = sku

        return skus

