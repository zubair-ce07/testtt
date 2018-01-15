import scrapy.spider

from scrapy import FormRequest

from urllib.parse import urljoin, parse_qsl

from Woolrich.spiders.mixin import Mixin

from Woolrich.spiders.general import WoolGeneral


class Parser(scrapy.Spider, Mixin):
    name = 'woolrich-parser'
    url_api = "http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp"
    gender_map = [
        ('Women', 'women'),
        ('Men', 'men')

    ]

    def __init__(self):
        self.generic = WoolGeneral()
        self.xpath_productid = "//span[@itemprop='productID']/text()"
        self.xpath_price = "//span[@itemprop='price']/@content"
        self.xpath_previous_price = "//span[contains(@class, 'strikethrough')]/text()"

    def parse_product(self, response):
        product = self.generic.product(response, self.xpath_productid)
        if not product:
            return
        product['title'] = self.title(response)
        product['url'] = response.url
        product['img_urls'] = self.image_urls(response)
        product['category'] = self.category(response)
        product['gender'] = self.gender(response)
        product['care'] = self.care(response)
        product['skus'] = {}
        product['pending_requests'] = self.colors_request(product, response)
        return self.generic.next_action(product)

    @staticmethod
    def title(response):
        xpath = "//div[@class='pdp_title']//h1/text()"
        title = response.xpath(xpath).extract_first()
        return title.strip()

    @staticmethod
    def image_urls(response):
        xpath = "//div[@id='prod-detail__slider-nav']//img/@src"
        image_urls = response.xpath(xpath).extract()
        return [response.urljoin(u) for u in image_urls]

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

    def size_request(self, response):
        size_requests = []
        xpath = "//ul[@class='sizelist']//a[@stocklevel != 0]"
        for size_itrator in response.xpath(xpath):
            form_data = dict(parse_qsl(response.request.body.decode()))
            size = size_itrator.xpath("text()").extract_first()
            form_data['selectedSize'] = size
            skuid = size_itrator.xpath("@id").extract_first()
            if skuid != size:
                form_data['skuId'] = skuid
            size_requests += [FormRequest(url=self.url_api,
                                          formdata=form_data,
                                          callback=self.parse_size,
                                          dont_filter=True
                                          )]
        return size_requests

    def colors_request(self, product, response):
        colour_requests = []
        xpath = "//div[@id='productDetails']//a[not(@disabled)]//img/@colorid"
        for colorid in response.xpath(xpath).extract():
            if colorid:
                form_data = {
                    'productId': product['product_id'],
                    'colorId': colorid
                }
                colour_requests += [FormRequest(url=self.url_api,
                                                formdata=form_data,
                                                callback=self.parse_colors,
                                                dont_filter=True
                                                )]
        return colour_requests

    def fitting_request(self, response):
        fitting_requests = []
        xpath = "//ul[@class='dimensionslist']//a[@stocklevel != 0]/@id"
        for fitting in response.xpath(xpath).extract():
            form_data = dict(parse_qsl(response.request.body.decode()))
            form_data['skuId'] = fitting
            fitting_requests.append(FormRequest(url=self.url_api,
                                                formdata=form_data,
                                                callback=self.parse_fittings,
                                                dont_filter=True))
        return fitting_requests

    def parse_colors(self, response):
        product = response.meta['product']
        product['img_urls'].append(self.color_image_urls(response))
        product['pending_requests'] += self.size_request(response)
        return self.generic.next_action(product)

    @staticmethod
    def color_image_urls(response):
        xpath = "//a[contains(@class,'selected')and contains(@class,' link  ')]//img/@src"
        img_url = response.xpath(xpath).extract_first(default='')
        if img_url:
            return urljoin('http:', img_url)

    def parse_size(self, response):
        product = response.meta['product']
        requests = self.fitting_request(response)
        product['pending_requests'] += requests
        if not requests:
            product['skus'].update(self.skus(response))
        return self.generic.next_action(product)

    def parse_fittings(self, response):
        product = response.meta['product']
        product['skus'].update(self.skus(response))
        return self.generic.next_action(product)

    def skus(self, response):
        sku = dict()
        sku['previous_price'] = self.generic.previous_prices(response, self.xpath_previous_price)
        size = self.size(response)
        colour = self.colour(response)
        fit = self.fitting(response)
        sku_id = "{}_{}".format(colour, size)
        sku['size'] = "{}/{}".format(size, fit)
        sku['colour'] = colour
        sku['price'] = self.generic.price(response, self.xpath_price)
        sku['Currency'] = self.currency(response)
        return {sku_id: sku}

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
    def currency(response):
        xpath = "//span[@itemprop='priceCurrency']/@content"
        return response.xpath(xpath).extract_first(default='')
