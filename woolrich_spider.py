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
    url_api = "http://www.woolrich.com/woolrich/prod/fragments/productDetails.jsp"


class WoolRichParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = "//span[@itemprop='price']/@content | //span[contains(@class, 'strikethrough')]/text()"
    care_x = "//div[@class='span4']//div[@class='text']//li/text()"
    description_x = "//span[@itemprop='description']/text()"

    def parse(self, response):
        product_id = self.product_id(response)
        garment = self.new_unique_garment(product_id)
        if not garment:
            return
        self.boilerplate_normal(garment, response)
        garment['gender'] = self.gender(response)
        garment['image_urls'] = []
        garment['skus'] = {}
        garment['meta'] = {'requests_queue': self.colors_request(response)}
        return self.next_request_or_garment(garment)

    @staticmethod
    def product_id(response):
        xpath = "//span[@itemprop='productID']/text()"
        return response.xpath(xpath).extract_first()

    @staticmethod
    def product_name(response):
        xpath = "//div[@class='pdp_title']//h1/text()"
        return clean(response.xpath(xpath).extract_first())[0]

    @staticmethod
    def image_urls(response):
        xpath = "//a[contains(@class,'selected')and contains(@class,' link  ')]//img/@src | " \
                "//div[@id='prod-detail__slider-nav']//img/@src"
        return [response.urljoin(u) for u in clean(response.xpath(xpath))]

    @staticmethod
    def product_category(response):
        xpath = "//div[contains(@class,'wrap') and " \
                "contains(@class,'breadcrumb')]//a/text()"
        return clean(response.xpath(xpath).extract())

    def gender(self, response):
        xpath = "//div[@class='pdp_title']//h1/text()"
        gender = self.gender_lookup(response.xpath(xpath).extract_first())
        if not gender:
            return 'uni-sex'
        return gender

    def colors_request(self, response):
        colour_requests = []
        xpath = "//div[@id='productDetails']//a[not(@disabled)]//img/@colorid"
        for colorid in response.xpath(xpath).extract():
            form_data = {
                'productId': self.product_id(response),
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
        for size_selector in response.xpath(xpath):
            form_data = dict(parse_qsl(response.request.body.decode()))
            size = size_selector.xpath("text()").extract_first()
            form_data['selectedSize'] = size
            form_data['skuId'] = size_selector.xpath("@id").extract_first()
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
        garment['image_urls'] += self.image_urls(response)
        garment['meta']['requests_queue'] += self.size_request(response)
        return self.next_request_or_garment(garment)

    def skus(self, response):
        color_xpath = "//ul[@class='colorlist']//li//a[contains(@class, 'selected')]/@title"
        size_xpath = "//select[contains(@class,'sizelist')]//option[@selected]/text()"
        fiting_xpath = "//select[contains(@class, 'dimensionslist')]//option[@selected]/text()"
        common_sku = self.product_pricing_common(response)
        sku = common_sku.copy()
        size = clean(response.xpath(size_xpath))[0]
        colour = response.xpath(color_xpath).extract_first()
        fit = response.xpath(fiting_xpath).extract_first(default='').strip()
        sku_id = "{}_{}".format(colour, size)
        sku['size'] = "{}_{}".format(size, fit)
        sku['colour'] = colour
        return {sku_id: sku}


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
