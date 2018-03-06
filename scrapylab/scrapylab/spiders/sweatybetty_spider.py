import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import SweatBettyItem


class SweatyBetty(CrawlSpider):
    name = 'sweatybetty'
    allowed_domains = ['sweatybetty.com']
    start_urls = ['http://www.sweatybetty.com/']
    listings_xpath = ['//*[contains(@class, "megamenu")]', '//*[contains(@href, "page=all")]']
    products_xpath = ['//*[contains(@class, "productname")]//a']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=listings_xpath), callback='parse'),
        Rule(LinkExtractor(restrict_xpaths=products_xpath), callback='parse_item'),
    )

    def parse_item(self, response):
        item = SweatBettyItem()
        raw_product = self.raw_product(response)

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

    def raw_product(self, response):
        products_xpath = '//script[contains(text(),"window.universal_variable = ")]'
        raw_product_re = re.compile('({.*})', re.DOTALL)
        raw_json = response.xpath(products_xpath).re(raw_product_re)
        correct_json = raw_json[0].replace(",]", "]")
        return json.loads(correct_json)

    def product_brand(self, response):
        return response.xpath('//*[contains(@itemprop, "logo")]//@title').extract_first()

    def product_care(self, response):
        raw_care = response.xpath('//*[contains(@class, "fabricdesc")]//text()').extract()
        return self.clean(raw_care)

    def product_description(self, response):
        description_xpath = '//*[contains(@itemprop , "description")]//*[self::p or self::li]//text()'
        return self.clean(response.xpath(description_xpath).extract())

    def image_urls(self, response):
        images_xpath = '//script[contains(text(),"largeArray")]'
        raw_image_urls = response.xpath(images_xpath).re("large.*new\sArray\((.*?)\)")
        image_urls = raw_image_urls[0].split(",")

        image_urls = [url.replace('\"', '') for url in image_urls]
        return self.clean(image_urls)

    def skus(self, response):
        raw_skus = response.css('script:contains(vcaption1)').re("vdata1\[\d+\]=.*?\(.*?\((.*?)\);")
        skus = []
        length_exist, size_exist = self.verify_length_size(response)

        for raw_sku in raw_skus:
            raw_sku = raw_sku.replace(")", "").replace("'", "")
            if 'length' in raw_sku or 'Size' in raw_sku:
                continue

            refined_sku = raw_sku.split(",")[:-10]

            if length_exist:
                colour, size, length, price = refined_sku

                main_price, previous_price = self.product_pricing(price)
                size_values, out_of_stock = self.product_stock_check(size)
                length, out_of_stock = self.product_stock_check(length)
                sku = {'colour': colour,
                       'size': "{0}/{1}".format(size_values, length),
                       'price': main_price,
                       'sku_id': "{0}_{1}/{2}".format(colour, size_values, length),
                       'previous_prices': previous_price}
                if out_of_stock:
                    sku['out_of_stock'] = out_of_stock

                skus.append(sku)
            elif size_exist:
                colour, size, price = refined_sku

                main_price, previous_price = self.product_pricing(price)
                size_values, out_of_stock = self.product_stock_check(size)

                sku = {'colour': colour,
                       'size': "{0}".format(size_values),
                       'price': main_price,
                       'sku_id': "{0}_{1}".format(colour, size_values),
                       'previous_prices': previous_price}
                if out_of_stock:
                    sku['out_of_stock'] = out_of_stock

                skus.append(sku)
            else:
                colour, price = refined_sku
                size = "One Size"
                main_price, previous_price = self.product_pricing(price)
                sku = {'colour': colour,
                       'size': "{0}".format(size),
                       'price': main_price,
                       'sku_id': "{0}_{1}".format(colour, size),
                       'previous_prices': previous_price}

                skus.append(sku)
        return skus

    def product_stock_check(self, measurement):
        size = ''.join(measurement.split("-")[:-1] if 'stock' in measurement else [measurement]).strip()
        return size, 'out of stock' in measurement

    def product_pricing(self, price):
        raw_prices = re.findall("([\d.\d]+)", price)
        prices = [int(float(raw_price) * 100) for raw_price in raw_prices]
        prices.sort()

        current_price = prices.pop(0)
        return current_price, prices

    def verify_length_size(self, response):
        raw_script = response.css('script:contains("var vcaption1")').extract_first()
        return 'Choose Length' in raw_script, 'Choose Size' in raw_script

    def clean(self, to_clean):
        cleaned = [per_entry.strip() for per_entry in to_clean] if to_clean else ""
        return list(filter(None, cleaned))
