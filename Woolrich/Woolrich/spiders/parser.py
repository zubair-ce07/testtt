from Woolrich.spiders.mixin import Mixin
import scrapy.spider
from Woolrich.items import WoolrichItem
from scrapy import FormRequest
from urllib.parse import urljoin
from urllib.parse import parse_qsl
import re


class Parser(scrapy.Spider, Mixin):
    name = 'product_spider'
    url_api = "http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp"
    product_ids = []
    gender_map = [
        ('Women', 'women'),
        ('Men', 'men')

    ]

    def parse_product(self, response):
        product = WoolrichItem()
        product_id = self.product_id(response)
        if product_id in self.product_ids:
            return
        self.product_ids.append(product_id)
        product['product_id'] = product_id
        product['title'] = self.title(response)
        product['url'] = response.url
        product['img_urls'] = self.img_urls(response)
        product['category'] = self.category(response)
        product['gender'] = self.gender(response)
        product['care'] = self.care(response)
        product['skus'] = {}
        product['pending_requests'] = self.request_colors(product, response)
        return self.next_action(product)

    @staticmethod
    def title(response):
        xpath = "//div[@class='pdp_title']//h1/text()"
        title = response.xpath(xpath).extract_first()
        return title.strip()

    @staticmethod
    def product_id(response):
        xpath = "//span[@itemprop='productID']/text()"
        productid = response.xpath(xpath).extract_first()
        return productid

    @staticmethod
    def img_urls(response):
        xpath = "//div[@id='prod-detail__slider-nav']//img/@src"
        img_urls = response.xpath(xpath).extract()
        return [urljoin('http:', url) for url in img_urls]

    @staticmethod
    def category(response):
        xpath = "//div[contains(@class,'wrap') and " \
                "contains(@class,'breadcrumb')]//a/text()"
        category = response.xpath(xpath).extract()
        return category

    def gender(self, response):
        xpath = "//div[@class='pdp_title']//h1/text()"
        title = response.xpath(xpath).extract_first()
        for gender, l_gender in self.gender_map:
            if gender in title:
                return l_gender
        return "Unisex-Adults"

    @staticmethod
    def care(response):
        xpath = "//div[@class='span4']//div[@class='text']//li/text()"
        cares = response.xpath(xpath).extract()
        return [care.strip() for care in cares]

    def request_size(self, response):
        pendin_requests = []
        xpath = "//ul[@class='sizelist']//a[@stocklevel != 0]"
        for size_itrator in response.xpath(xpath):
            form_data = dict(parse_qsl(response.request.body.decode()))
            size = size_itrator.xpath("text()").extract_first()
            form_data['selectedSize'] = size
            skuidid = size_itrator.xpath("@id").extract_first()
            if id != size:
                form_data['skuId'] = skuidid
            pendin_requests += [FormRequest(url=self.url_api,
                                            formdata=form_data,
                                            callback=self.parse_size,
                                            dont_filter=True
                                            )]
        return pendin_requests

    def request_colors(self, product, response):
        pending_requests = []
        xpath = "//div[@id='productDetails']//li//a[not(@disabled)]//img/@colorid"
        for colorid in response.xpath(xpath).extract():
            if colorid:
                form_data = {
                    'productId': product['product_id'],
                    'colorId': colorid
                }
                pending_requests += [FormRequest(url=self.url_api,
                                                 formdata=form_data,
                                                 callback=self.parse_colors,
                                                 dont_filter=True
                                                 )]
        return pending_requests

    def request_fittings(self, response):
        pending_requests = []
        xpath = "//ul[@class='dimensionslist']//a[@stocklevel != 0]/@id"
        for fiting in response.xpath(xpath).extract():
            form_data = dict(parse_qsl(response.request.body.decode()))
            form_data['skuId'] = fiting
            pending_requests.append(FormRequest(url=self.url_api,
                                                formdata=form_data,
                                                callback=self.parse_fittings,
                                                dont_filter=True))
        return pending_requests

    def parse_colors(self, response):
        product = response.meta['product']
        product['img_urls'].append(self.color_img(response))
        product['pending_requests'] += self.request_size(response)
        return self.next_action(product)

    @staticmethod
    def color_img(response):
        xpath = "//a[contains(@class,'selected')and contains(@class,' link  ')]//img/@src"
        img_url = response.xpath(xpath).extract_first(default='')
        if img_url:
            return urljoin('http:', img_url)

    @staticmethod
    def next_action(product):
        if product['pending_requests']:
            request = product['pending_requests'].pop()
            request.meta['product'] = product
            return request
        return product

    def parse_size(self, response):
        product = response.meta['product']
        requests = self.request_fittings(response)
        product['pending_requests'] += requests
        if not requests:
            product['skus'].update(self.skus(response))
        return self.next_action(product)

    def parse_fittings(self, response):
        product = response.meta['product']
        product['skus'].update(self.skus(response))
        return self.next_action(product)

    def skus(self, response):
        item = dict()
        item['previous_price'] = self.previous_prices(response)
        size = self.size(response)
        colour = self.colour(response)
        fit = self.fitting(response)
        sku_id = "{}_{}".format(colour, size)
        item['size'] = "{}/{}".format(size, fit)
        item['colour'] = colour
        item['price'] = self.price(response)
        item['Currency'] = self.currency(response)
        return {sku_id: item}

    @staticmethod
    def previous_prices(response):
        xpath = "//span[contains(@class, 'strikethrough')]/text()"
        price = response.xpath(xpath).extract_first()
        if price:
            price = price.replace(',', '')
            return int(round(float(re.search(r'\d+.\d+', price).group(0)) * 100))
        return ''

    @staticmethod
    def colour(response):
        xpath = "//ul[@class='colorlist']//li//a[contains(@class, 'selected')]/@title"
        return response.xpath(xpath).extract_first()

    @staticmethod
    def size(response):
        xpath = "//select[contains(@class,'sizelist')]//option[@selected]/text()"
        return response.xpath(xpath).extract_first().strip()

    @staticmethod
    def fitting(response):
        xpath = "//select[contains(@class, 'dimensionslist')]//option[@selected]/text()"
        return response.xpath(xpath).extract_first(default='').strip()

    @staticmethod
    def price(response):
        xpath = "//span[@itemprop='price']/@content"
        price = response.xpath(xpath).extract_first(default='').replace(',', '')
        return int(round(float(price) * 100))

    @staticmethod
    def currency(response):
        xpath = "//span[@itemprop='priceCurrency']/@content"
        return response.xpath(xpath).extract_first(default='')
