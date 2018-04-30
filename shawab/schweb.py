import json

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from schwab.items import SchwabItem
from w3lib.url import add_or_replace_parameter
import math
# import urllib.request


class Schwab(CrawlSpider):
    name = 'schwab'
    allowed_domain = ['https://www.schwab.de/']
    start_urls = ['https://www.schwab.de/index.php?cl=oxwCategoryTree&jsonly=true&staticContent=true&cacheID=1525066940']
    pages = ['section.mainnav--top a']
    products = ['div.product__top a']

    # def start_requests(self):
    #     scrapy_request = Request(self.start_urls[0])
    #     return scrapy_request

        # web_url = urllib.request.urlopen(self.start_urls[0])
        # data = web_url.read()
        # encoding = web_url.info().get_content_charset('utf-8')
        # json_response = json.loads(data.decode(encoding))
        # pages_urls = []
        # pages_requests = []
        #
        # for json in json_response:
        #         pages_urls.append(json['url'])
        #         for inner_cat in json['sCat']:
        #             pages_urls.append(inner_cat['url'])
        #
        # for page in pages_urls:
        #     pages_requests.append(Request(page, self.pagination))
        #
        # return pages_requests

    def parse_start_url(self, response):
        json_data = json.loads(response.text)
        pages_urls = []
        pages_requests = []

        for json_url in json_data:
            pages_urls.append(json_url['url'])
            for inner_cat in json_url['sCat']:
                pages_urls.append(inner_cat['url'])

        for page in range(len(pages_urls)):
            pages_requests.append(Request(pages_urls[page], self.pagination, dont_filter=True))
        return pages_requests

    rules = (
        Rule(LinkExtractor(restrict_css=products), callback='product_scraper'),
    )

    def pagination(self, response):
        total_items = response.css('.pl__headline__count::text').re_first(r'(\d+)')
        items_per_page = 60

        if not total_items:
            return

        total_pages = math.ceil(int(total_items) / items_per_page)

        # 1 added for upper bound
        for page in range(int(total_pages) + 1):
            url = add_or_replace_parameter(
                response.url, '?pageNr=', page)
            yield Request(url, self.parse)

    def product_scraper(self, response):
        product = SchwabItem()
        product['product_name'] = self.product_name(response)
        product['product_detail'] = self.product_detail(response)
        product['product_brand'] = self.product_brand(response)
        product['product_price'] = self.product_price(response)
        product['product_quantity'] = self.product_quantity(response)
        product['product_currency'] = self.product_currency(response)
        product['product_images'] = self.product_images(response)
        product['product_retailer_sku'] = self.product_retailer_sku(response)
        product['product_description'] = self.product_description(response)
        product['product_url_origin'] = self.product_url_origin(response)
        product['retailer'] = "schwab"
        product['trail'] = self.product_trail(response)
        product['category'] = self.product_category(response)
        product['color'] = self.product_color(response)
        product['skus'] = self.product_skus(response)

        other_requests = self.additional_colors(response)
        return self.parse_additional_requests(other_requests, product)

    def product_skus(self, response):
        sizes = self.product_size(response)
        additional_colors = self.additional_colors_name(response)
        count = 0
        skus = {}

        for size in sizes:
            sku = {}
            sku["size"] = size
            sku["product_retailer_sku"] = self.product_retailer_sku(response)
            sku["product_retailer_sku"] = self.product_price(response)
            sku["product_currency"] = self.product_currency(response)
            sku["product_color"] = self.product_color(response)
            if additional_colors:
                sku["additional_product_color"] = additional_colors
            skus.update({count: sku})
            count = count + 1

        return skus

    def additional_colors(self, response):
        colors = response.css('a.colorspots__item::attr(title)').extract()
        items = {}

        items["sku"] = self.product_skus(response)
        items['images'] = self.product_images(response)
        additional_requests = []

        for color in colors:
            requests = add_or_replace_parameter(response.url, "?color={}", color)
            additional_requests.append(Request(requests, self.extra_color_images))

        return additional_requests

    def extra_color_images(self, response):
        # https://doc.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments
        product = response.meta['product']
        addl_requests = response.meta['requests']
        product['skus'].update({"18": self.product_skus(response)})
        product['product_images'].append(self.product_images(response))
        return self.parse_additional_requests(addl_requests, product)

    @staticmethod
    def parse_additional_requests(addl_requests, data):
        if not addl_requests:
            yield data
        for request in addl_requests:
            request.meta['product'] = data
            request.meta['requests'] = addl_requests
            yield request

    @staticmethod
    def product_name(response):
        name = response.css('h1.details__title span::text').extract_first()
        return name

    @staticmethod
    def product_detail(response):
        detail = response.css('ul.l-outsp-bot-5 li::text').extract()
        return detail

    @staticmethod
    def product_brand(response):
        brand = response.css('meta.at-dv-brand::attr(content)').extract_first()
        return brand

    @staticmethod
    def product_price(response):
        price = response.css('.js-detail-price::text').extract_first()
        return price

    @staticmethod
    def product_quantity(response):
        quantity = response.css(
            '.js-current-variant-name::attr(value)').extract_first()
        return quantity

    @staticmethod
    def product_currency(response):
        currency = response.css(
            'meta[itemprop="priceCurrency"]::attr(content)').extract_first()
        return currency

    @staticmethod
    def product_images(response):
        images = response.css('#thumbslider a::attr(href)').extract()
        for image in range(len(images)):
            images[image] = str("https:") + images[image]
        return images

    @staticmethod
    def product_retailer_sku(response):
        id = response.css('.js-current-artnum::attr(value)').extract_first()
        return id

    @staticmethod
    def product_description(response):
        desc = response.css('div.l-outsp-bot-10 li::text').extract()
        return desc

    @staticmethod
    def product_url_origin(response):
        url_origin = response.css('link[rel="canonical"]::attr(href)').extract_first()
        return url_origin

    @staticmethod
    def product_trail(response):
        trails = response.css('ul.breadcrumb a::attr(href)').extract()
        trail_dict = {}
        count = 0

        for trail in trails:
            trail_dict[str(count)] = trail
            count = count + 1

        return trail_dict

    @staticmethod
    def product_category(response):
        categories = response.css('ul.breadcrumb span[itemprop="name"]::text').extract()
        category_dict = {}
        count = 0

        for category in categories:
            category_dict[str(count)] = category
            count = count + 1

        return category_dict

    @staticmethod
    def product_color(response):
        color = response.css('.js-current-color-name::attr(value)').re_first(r'(\w+)')
        return color

    @staticmethod
    def product_size(response):
        sizes = response.css('.js-sizeSelector button::text').re(r'(\d+)')
        return sizes

    @staticmethod
    def additional_colors_name(response):
        colors = response.css('a.colorspots__item::attr(title)').extract()
        return colors
