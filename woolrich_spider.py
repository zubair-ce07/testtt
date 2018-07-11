from scrapy import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from urllib.parse import urljoin, parse_qsl
from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    retailer = 'woolrich'
    market = 'CA'
    allowed_domains = ['woolrich.com']
    start_urls = ['http://www.woolrich.com/woolrich/?countryCode=CA']


class WoolRichParseSpider(BaseParseSpider, Mixin):
    url_api = "http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp"
    price_x = "//span[@itemprop='price']/@content"
    care_x = "//div[@class='span4']//div[@class='text']//li/text()"
    description_x = "//span[@itemprop='description']/text()"

    def __init__(self):
        self.xpath_productid = "//span[@itemprop='productID']/text()"
        self.xpath_previous_price = "//span[contains(@class, 'strikethrough')]/text()"

    def parse(self, response):
        product_id = response.xpath(self.xpath_productid).extract_first()
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.gender_lookup(self.gender(response))
        garment['image_urls'] = self.image_urls(response)
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.colors_request(response)}
        return self.next_request_or_garment(garment)

    @staticmethod
    def product_name(response):
        xpath = "//div[@class='pdp_title']//h1/text()"
        title = response.xpath(xpath).extract_first()
        return title.strip()

    @staticmethod
    def image_urls(response):
        xpath = "//div[@id='prod-detail__slider-nav']//img/@src"
        image_urls = response.xpath(xpath).extract()
        return [response.urljoin(u) for u in image_urls]

    @staticmethod
    def product_category(response):
        xpath = "//div[contains(@class,'wrap') and " \
                "contains(@class,'breadcrumb')]//a/text()"
        category = response.xpath(xpath).extract()
        return category

    def gender(self, response):
        xpath = "//div[@class='pdp_title']//h1/text()"
        return response.xpath(xpath).extract_first()

    def colors_request(self, response):
        colour_requests = []
        xpath = "//div[@id='productDetails']//a[not(@disabled)]//img/@colorid"
        for colorid in response.xpath(xpath).extract():
            if colorid:
                form_data = {
                    'productId': response.xpath(self.xpath_productid).extract_first(),
                    'colorId': colorid
                }
                colour_requests += [FormRequest(url=self.url_api,
                                                formdata=form_data,
                                                callback=self.parse_colors,
                                                dont_filter=True
                                                )]
        return colour_requests

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

    def parse_fittings(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def parse_size(self, response):
        garment = response.meta['garment']
        requests = self.fitting_request(response)
        garment['meta']['requests_queue'] += requests
        if not requests:
            garment['skus'].update(self.skus(response))
        return self.next_request_or_garment(garment)

    def parse_colors(self, response):
        garment = response.meta['garment']
        garment['image_urls'].append(self.color_image_urls(response))
        garment['meta']['requests_queue'] += self.size_request(response)
        return self.next_request_or_garment(garment)

    @staticmethod
    def color_image_urls(response):
        xpath = "//a[contains(@class,'selected')and contains(@class,' link  ')]//img/@src"
        img_url = response.xpath(xpath).extract_first(default='')
        if img_url:
            return urljoin('http:', img_url)

    def common_sku(self, response):
        sku = {}
        sku.update(self.product_pricing_common(response))
        return sku

    def skus(self, response):
        common_sku = self.common_sku(response)
        sku = common_sku.copy()
        # sku['previous_price'] = self.previous_prices(response, self.xpath_previous_price)
        size = self.size(response)
        colour = self.colour(response)
        fit = self.fitting(response)
        sku_id = "{}_{}".format(colour, size)
        sku['size'] = "{}/{}".format(size, fit)
        sku['colour'] = colour
        sku['currency'] = self.currency(response)
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


class WoolRichSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = WoolRichParseSpider()
    css_classes = [
        '.nav.navbar-nav .upper',
        '.nav.nav-list.nav-',
        '.clear.addMore'
    ]
    rules = (
        Rule(LinkExtractor(restrict_css=css_classes, tags=['a', 'div'], attrs=['href', 'nextpage'])
             ),
        Rule(
            LinkExtractor(restrict_css='.productCard'), callback='parse_item'
        )
    )
