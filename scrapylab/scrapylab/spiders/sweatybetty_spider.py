import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import SweatBettyItem


class SweatyBetty(CrawlSpider):
    name = 'sweatybetty'
    allowed_domains = ['sweatybetty.com']
    start_urls = ['http://www.sweatybetty.com/']
    rule_xpaths = ['//*[contains(@class, "megamenu")]', '//*[contains(@href, "page=all")]']
    sub_rule_xpaths = ['//*[contains(@class, "productname")]//a']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=rule_xpaths), callback='parse'),
        Rule(LinkExtractor(restrict_xpaths=sub_rule_xpaths), callback='parse_item'),
    )

    def parse_item(self, response):
        item = SweatBettyItem()
        raw_product = self.product_schema(response)

        item['retailer_sku'] = raw_product['product']['id'].split('_')[0]
        item['category'] = raw_product['page']['breadcrumb']
        item['name'] = raw_product['product']['name']
        item['url'] = raw_product['product']['url']
        item['currency'] = raw_product['product']['currency']

        item['brand'] = self.product_brand(response)
        item['description'] = self.product_description(response)
        item['care'] = self.product_care(response)
        item['image_urls'] = self.image_urls(response)
        item['skus'] = self.skus(response)

        return item

    def product_schema(self, response):
        correct_schema = ""
        raw_schema = response.xpath('//script[contains(text(),"window.universal_variable")]').extract()
        for schema in raw_schema:
            match_schema = re.findall('window\.universal\_variable = (\{\s+.*\s+.*\s+\})\s+\<\/script\>', schema)
            if match_schema:
                correct_schema = match_schema[0].replace(",]", "]")
                break
        return json.loads(correct_schema)

    def product_brand(self, response):
        return response.xpath('//*[contains(@itemprop, "logo")]//@title').extract_first()

    def product_care(self, response):
        raw_care = response.xpath('//*[contains(@class, "fabricdesc")]//text()').extract()
        return self.clean(raw_care)

    def product_description(self, response):
        raw_description = response.xpath('//*[contains(@itemprop , "description")]//p//text()').extract()
        raw_description.extend(response.xpath('//*[contains(@itemprop , "description")]//li//text()').extract())
        return self.clean(raw_description)

    def image_urls(self, response):
        image_urls = []
        script_container = response.xpath('//script').extract()
        for req_schema in script_container:
            raw_image_urls = re.findall("large.*new\sArray\((.*?)\)", req_schema)
            for per_image_url in raw_image_urls:
                image_urls = list(per_image_url.split(","))

        image_urls = [quote_in_url.replace('\"', '') for quote_in_url in image_urls]
        return self.clean(image_urls)

    def skus(self, response):
        raw_skus = response.css('script:contains(vcaption1)').re("vdata1\[\d+\]=.*?\(.*?\((.*?)\);")
        sku_blocks = []
        length_exist, size_exist = self.verify_length_size(response)

        for js_sku in raw_skus:
            js_sku = js_sku.replace(")", "")
            js_sku = js_sku.replace("'", "")

            if 'length' in js_sku or 'Size' in js_sku:
                continue

            refined_sku = js_sku.split(",")
            req_sku_schema = refined_sku[:-10]

            if length_exist:
                colour, size, length, price = req_sku_schema

                main_price, previous_price = self.product_pricing(price)
                size_values, out_of_stock = self.product_stock_check(size)
                length, out_of_stock = self.product_stock_check(length)
                sub_sku = {'colour': colour,
                           'size': "{0}/{1}".format(size_values, length),
                           'price': main_price,
                           'sku_id': "{0}_{1}/{2}".format(colour, size_values, length),
                           'previous_prices': previous_price}
                if out_of_stock:
                    sub_sku['out_of_stock'] = out_of_stock

                sku_blocks.append(sub_sku)
            elif size_exist:
                colour, size, price = req_sku_schema

                main_price, previous_price = self.product_pricing(price)
                size_values, out_of_stock = self.product_stock_check(size)

                sub_sku = {'colour': colour,
                           'size': "{0}".format(size_values),
                           'price': main_price,
                           'sku_id': "{0}_{1}".format(colour, size_values),
                           'previous_prices': previous_price}
                if out_of_stock:
                    sub_sku['out_of_stock'] = out_of_stock

                sku_blocks.append(sub_sku)
            else:
                colour, price = req_sku_schema
                size = "One Size"
                main_price, previous_price = self.product_pricing(price)
                sub_sku = {'colour': colour,
                           'size': "{0}".format(size),
                           'price': main_price,
                           'sku_id': "{0}_{1}".format(colour, size),
                           'previous_prices': previous_price}

                sku_blocks.append(sub_sku)
        return sku_blocks

    def product_stock_check(self, measurement):
        out_of_stock = False
        if 'out' in measurement and 'stock' in measurement:
            measurement = measurement.split("-")[:-1]
            measurement = ''.join(measurement)
            out_of_stock = True
        elif 'stock' in measurement:
            measurement = measurement.split("-")[:-1]
            measurement = ''.join(measurement)

        measurement.rstrip()
        return measurement, out_of_stock

    def product_pricing(self, price):
        raw_prices = re.findall("([\d.\d]+)", price)
        org_prices = [int(float(prices) * 100) for prices in raw_prices]
        org_prices.sort()

        current_price = org_prices.pop(0)
        previous_prices = [org_prices.pop() for _ in org_prices]

        return current_price, previous_prices

    def verify_length_size(self, response):
        raw_script = response.css('script:contains("var vcaption1")').extract_first()
        if raw_script:
            length_exist = True if 'Choose Length' in raw_script else False
            size_exist = True if 'Choose Size' in raw_script else False
            return length_exist, size_exist
        return False, False

    def clean(self, to_clean):
        cleaned = [per_entry.rstrip() for per_entry in to_clean] if to_clean else ""
        return list(filter(None, cleaned))
