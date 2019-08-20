import scrapy
import json
import urllib.parse

from datetime import datetime
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Softsurroundings(CrawlSpider):
    name = 'softsurroundingsspider'
    start_urls = ['https://www.softsurroundings.com/']
    listing_css = '.menuWrap .dropdown-menu .categories li a '
    product_css = '.container .flexWrap'

    rules = (
        Rule(LinkExtractor(restrict_css=listing_css)),
        Rule(LinkExtractor(restrict_css=product_css), callback='parse_item')
    )

    def parse(self, response):
        yield from super().parse(response)
        return self.parse_pagination(response)

    def parse_item(self, response):
        with_unit_price = response.css('.dtlForm .ctntPrice span:nth-child(n+2)::text').get()
        raw_prices = [str(elem) for elem in with_unit_price if elem.isdigit()]
        price = int(''.join(raw_prices))
        item = SoftRecord()
        item['skus'] = []
        item['requests'] = []
        item['name'] = self.get_name(response)
        item['description'] = self.get_product_description(response)
        item['care'] = self.get_product_care(response)
        item['crawl_start_time'] = self.get_crawl_start_time()
        item['url'] = self.get_url(response)
        item['category'] = self.get_product_category(response)
        item['brand'] = self.get_brand(response)
        if self.get_skus_requests(response, item):
            item['requests'].extend(self.get_skus_requests(response, item))
        else:
            return self.parse_skus(response, item, price)
        return self.get_item_or_request(item)

    def parse_pagination(self, response):
        all_page_requests = []
        values = response.css('.thumbscroll input[name="page"]::attr(value)').getall()
        for page_number in values:
            url = f'{response.url}/page-{page_number}/'
            headers = {
                'accept': "application/json, text/javascript, */*; q=0.01",
                'accept-encoding': "gzip, deflate, br",
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
                'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            }
            payload = "ajax=1"
            all_page_requests.append(scrapy.Request(url=url, method="POST", headers=headers, body=json.dumps(payload),
                                                    callback=self.parse))
        return all_page_requests

    def parse_category(self, response):
        item = response.meta['item']
        price = response.meta['price']
        item['requests'].extend(self.color_size_requests(response, item, price))
        return self.get_item_or_request(item)

    def parse_color_size(self, response):
        price = response.meta['price']
        item = response.meta['item']
        return self.parse_skus(response, item, price)

    def parse_skus(self, response, item, price):
        check_response = isinstance(response, HtmlResponse)
        if check_response == False:
            encoded_response = json.loads(response.body)['productBulk']
            convert_to_html_string = urllib.parse.unquote_plus(encoded_response)
            response = HtmlResponse(url="my HTML string", body=convert_to_html_string, encoding='utf-8')
        color = response.css('#color .sizetbs .basesize::text').get()
        size = response.css('#size .sizetbs .basesize::text').get()
        stock_availablity = response.css('.stockStatus .basesize::text').get()
        if stock_availablity == 'In Stock.':
            out_of_stock = False
        else:
            out_of_stock = True
        all_skus = [{'color': color, 'price': price, 'size': size, 'out_of_stock': out_of_stock}]
        item['skus'] = all_skus
        return self.get_item_or_request(item)

    def category_requests(self, response, item, price):
        all_parent_ids = []
        parent_id_bulk = response.css('.dtlFormBulk #sizecat a::attr(id)').getall()
        for one_parent_id in parent_id_bulk:
            split_parent_id = one_parent_id.split("_")[1]
            all_parent_ids.append(split_parent_id)
        all_requests = []
        for parent_id in all_parent_ids:
            category_req_url = f'https://www.softsurroundings.com/p/{parent_id}/'
            formdata = f'sku={parent_id}&ajax=1'
            headers = {
                'accept': "application/json, text/javascript, */*; q=0.01",
                'accept-encoding': "gzip, deflate, br",
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
                'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            }
            all_requests.append(scrapy.Request(url=category_req_url, method="POST", headers=headers,
                                               meta={'item': item, 'price': price}, callback=self.parse_category,
                                               body=json.dumps(formdata)))
        return all_requests

    def color_size_requests(self, response, item, price):
        check_response = isinstance(response, HtmlResponse)
        if check_response == False:
            encoded_response = json.loads(response.body)['productBulk']
            convert_to_html_string = urllib.parse.unquote_plus(encoded_response)
            response = HtmlResponse(url="my HTML string", body=convert_to_html_string, encoding='utf-8')
        if check_response == False:
            parent_id = response.css('input[type=hidden]::attr(value)').get()
        else:
            content_url = response.css("meta[property='og:image']::attr(content)").get()
            parent_id = content_url.split("/")[-1]
        all_color_ids = []
        if response.css('.swatchHover img').get():
            all_col_ids = response.css('#color img::attr(id)').getall()
            for one_col in all_col_ids:
                split_col_id = one_col.split("_")[-1]
                all_color_ids.append(split_col_id)
        else:
            color_id = response.css('.lbl1 input::attr(value)').get()
            all_color_ids.append(color_id)
        all_size_ids = []
        if len(response.css('#size a').getall()) > 1:
            size_chart = response.css('#size a::attr(id)').getall()
            all_sizes = size_chart[1:]
            for one_size in all_sizes:
                split_size_id = one_size.split("_")[-1]
                all_size_ids.append(split_size_id)
        else:
            size_one = response.css('.lbl1 input:nth-child(n+3)::attr(value)').get()
            all_size_ids.append(size_one)
        all_kind_requests = []
        for one_color_id in all_color_ids:
            for one_size_id in all_size_ids:
                size_req_url = f'https://www.softsurroundings.com/p/{parent_id}/{one_color_id}{one_size_id}/'
                formdata = f'sku={parent_id}{one_color_id}{one_size_id}&ajax=1'
                headers = {
                    'accept': "application/json, text/javascript, */*; q=0.01",
                    'accept-encoding': "gzip, deflate, br",
                    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
                    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                }
                all_kind_requests.append(scrapy.Request(url=size_req_url, method="POST", headers=headers,
                                                        meta={'item': item, 'price': price},
                                                        callback=self.parse_color_size,
                                                        body=json.dumps(formdata)))
        return all_kind_requests

    def get_item_or_request(self, item):
        if item['requests']:
            return item['requests'].pop()
        del item['requests']
        return item

    def get_skus_requests(self, response, item):
        with_unit_price = response.css('.dtlForm .ctntPrice span:nth-child(n+2)::text').get()
        raw_prices = [str(elem) for elem in with_unit_price if elem.isdigit()]
        price = int(''.join(raw_prices))
        if response.css('#sizecat').get():
            return self.category_requests(response, item, price)
        elif response.css('#color .swatchlink img').get():
            return self.color_size_requests(response, item, price)
        elif len(response.css('#size a').getall()) > 1:
            return self.color_size_requests(response, item, price)

    def get_name(self, response):
        return response.css('.dtlHeader h1 span::text').get()

    def get_brand(self, response):
        return response.css("meta[property='og:site_name']::attr(content)").get()

    def get_url(self, response):
        return response.url

    def get_product_details(self, response):
        return response.css('.productInfoDetails li::text').getall()

    def get_product_description(self, response):
        return response.css('.productInfo span ::text').getall()

    def get_product_care(self, response):
        return response.css('.moreProductInfo .tabContent::text').get()

    def get_crawl_start_time(self):
        return datetime.utcnow()

    def get_product_category(self, response):
        return response.css('.pagingBreadCrumb a::text').getall()


class SoftRecord(scrapy.Item):

    name = scrapy.Field()
    skus = scrapy.Field()
    description = scrapy.Field()
    care = scrapy.Field()
    image_urls = scrapy.Field()
    crawl_start_time = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    requests = scrapy.Field()
