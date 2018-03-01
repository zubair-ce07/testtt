import scrapy
import re
import json

from ..items import SweatBettyItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SweatyBetty(CrawlSpider):
    name = 'sweatybetty'
    allowed_domains = ['sweatybetty.com']
    start_urls = ['http://www.sweatybetty.com/']

    rules = (Rule(LinkExtractor(allow=(),
                                restrict_xpaths='//*[contains(@class, "megamenu")]',
                                ),
                  callback='parse_urls'),)

    def parse_urls(self, response):
        all_products_urls = response.xpath('//*[contains(@href, "page=all")]').css("a::attr(href)").extract_first()
        if all_products_urls:
            url = response.urljoin(all_products_urls)
            yield scrapy.Request(url, callback=self.parse_product_urls)
        else:
            yield scrapy.Request(
                response.url,
                callback=self.parse_product_urls)

    def parse_product_urls(self, response):
        product_path = response.xpath("//*[contains(@class, 'productname')]//a/@href").extract()
        for prod_url in product_path:
            url = response.urljoin(prod_url)
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        item = SweatBettyItem()
        html = response.text
        product_values = self.parse_schema(html)

        item['retailer_sku'] = product_values['product']['id'].split('_')[0]
        item['category'] = product_values['page']['breadcrumb']
        item['name'] = product_values['product']['name']
        item['url'] = product_values['product']['url']
        item['currency'] = product_values['product']['currency']

        item['brand'] = self.parse_brand(response)
        item['description'] = self.parse_description_item(response)
        item['care'] = self.parse_care_item(response)
        item['image_urls'] = self.get_image_urls(html)
        item['skus'] = self.parse_skus(response, html)

        return item

    def parse_schema(self, html):
        schema_container = re.findall('window\.universal\_variable = (\{\s+.*\s+.*\s+\})\s+\<\/script\>', html)
        corrected_schema_container = schema_container[0].replace(",]", "]") if schema_container else {}
        return json.loads(corrected_schema_container)

    def parse_brand(self, response):
        return response.xpath('//*[contains(@itemprop, "logo")]//@title').extract_first()

    def parse_skus(self, response, html):
        get_raw_data = response.css('script:contains(vcaption1)').re("vdata1\[\d+\]=.*?\(.*?\((.*?)\);")
        length_exist = True if 'Choose Length' in html else False
        size_exist = True if 'Choose Size' in html else False
        return self.get_skus(get_raw_data, length_exist, size_exist)

    def parse_care_item(self, response):
        care = response.xpath('//*[contains(@class, "fabricdesc")]//text()').extract()
        care = [care_values.rstrip() for care_values in care] if care else ""

        return list(filter(None, care)) if list(filter(None, care)) else ""

    def parse_description_item(self, response):
        description = response.xpath('//*[contains(@itemprop , "description")]//p//text()').extract()
        description.extend(response.xpath('//*[contains(@itemprop , "description")]//li//text()').extract())
        description = [description_values.rstrip() for description_values in description] if description else ""

        return list(filter(None, description)) if list(filter(None, description)) else ""

    def get_image_urls(self, html):
        image_raw_urls = re.findall("large.*new\sArray\((.*?)\)", html)
        if image_raw_urls:
            for per_image_url in image_raw_urls:
                image_urls = list(per_image_url.split(","))

        image_urls = [image_url_quote.replace('"', '') for image_url_quote in image_urls]
        return list(filter(None, image_urls))

    def get_skus(self, get_raw_data, length_exist, size_exist):
        skus = []
        for js_sku_value in get_raw_data:
            js_sku_value = js_sku_value.replace(")", "")
            js_sku_value = js_sku_value.replace("'", "")
            if not ('length' in js_sku_value or 'Size' in js_sku_value):
                parsed_sku_value = js_sku_value.split(",")
                if length_exist:
                    req_sku_schema = parsed_sku_value[:-10]
                    color, size, length, price = req_sku_schema

                    main_price, previous_price = self.populate_prices(price)
                    size_values, out_of_stock = self.parse_stock_values(size)
                    length, out_of_stock = self.parse_stock_values(length)

                    sub_sku = {'color': color, 'size': size_values + "/" + length, 'price': main_price,
                               'sku_id': color + "_" + size_values + "/" + length, 'out_of_stock': out_of_stock,
                               'previous_prices': previous_price}
                    skus.append(sub_sku)
                elif size_exist:
                    req_sku_schema = parsed_sku_value[:-10]
                    color, size, price = req_sku_schema

                    main_price, previous_price = self.populate_prices(price)
                    size_values, out_of_stock = self.parse_stock_values(size)

                    sub_sku = {'color': color, 'size': size_values, 'price': main_price,
                               'sku_id': color + "_" + size_values, 'out_of_stock': out_of_stock,
                               'previous_prices': previous_price}

                    skus.append(sub_sku)
                else:
                    req_sku_schema = parsed_sku_value[:-10]
                    color, price = req_sku_schema

                    main_price, previous_price = self.populate_prices(price)

                    sub_sku = {'color': color, 'size': "/", 'price': main_price,
                               'sku_id': color + "_" + "/", 'out_of_stock': False,
                               'previous_prices': previous_price}

                    skus.append(sub_sku)
        return skus

    def parse_stock_values(self, stock_values):
        if 'out' in stock_values and 'stock' in stock_values:
            stock_values = stock_values.split("-")[:-1]
            stock_values = ''.join(stock_values)
            out_of_stock = True
        elif 'stock' in stock_values:
            stock_values = stock_values.split("-")[:-1]
            stock_values = ''.join(stock_values)
            out_of_stock = False
        else:
            out_of_stock = False

        stock_values.strip()
        return stock_values, out_of_stock

    def populate_prices(self, price):
        fetched_prices = re.findall("([\d\d\d.\d\d]+)", price)
        current_price = int(float(fetched_prices[0]) * 100)
        if len(fetched_prices) > 1:
            previous_prices = fetched_prices[1:]
            previous_prices = [int(float(price_to_int) * 100) for price_to_int in previous_prices]
            return current_price, previous_prices
        return current_price, []
