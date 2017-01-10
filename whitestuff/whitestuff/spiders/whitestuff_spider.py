import json
import re
import urllib

from scrapy import Selector
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.request import Request
from whitestuff.items import WhitestuffItem
from urllib import urlencode


class WhitestuffSpider(CrawlSpider):
    name = "whitestuff"
    allowed_domains = ["whitestuff.com", 'fsm.attraqt.com']
    start_urls = [
        "http://whitestuff.com/",
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=['#holder_UPPERNAVIGATION', 'div.leftNAVIGATION']),
             callback='parse_item_or_fetch_list'),
    )

    def parse_item_or_fetch_list(self, response):
        ajax_params = self.parse_ajax_params(response)

        if ajax_params['config_page'] == 'category listing':
            return self.fetch_category_listing(ajax_params)

        if ajax_params['config_page'] == 'product detail':
            is_sale = ajax_params['is_sale']
            return self.parse_item(response, is_sale)

    def fetch_category_listing(self, params):
        params['zone0'] = 'category'
        url = 'http://fsm.attraqt.com/zones-js.aspx?'
        url += urlencode(params)
        yield Request(url=url, callback=self.parse_category_listing)

    def parse_category_listing(self, response):
        json_raw = re.findall('LM.buildZone\((.*)\);', response.text).pop()
        json_obj = json.loads(json_raw)
        html = json_obj['html']
        selector = Selector(text=html)
        product_links = selector.css('ul[id*=prodListing] > li > span[id*=link]::text').extract()
        for link in product_links:
            yield Request(url='http://www.whitestuff.com' + link, callback=self.parse_item_or_fetch_list)
        pagination_links = response.css('div[class*=list-control-bar] a::attr(href)').extract()
        for link in pagination_links:
            yield Request(url = 'http://www.whitestuff.com' + link, callback=self.parse_item_or_fetch_list)

    def parse_ajax_params(self, response):
        params = {}
        script = response.css('script:contains("LM.config")')
        params['version'] = '16.6.15'
        params['config_region'] = script.re_first(r'LM.config\("region",\s*"(.*)"\)')
        params['config_currency'] = script.re_first(r'LM.config\("currency",\s*"(.*)"\)')
        params['config_page'] = script.re_first(r'LM.config\("page",\s*"(.*)"\)')
        params['config_categorytree'] = script.re_first(r'LM.config\("categorytree",\s*"(.*)"\)')
        params['config_category'] = script.re_first(r'LM.config\("category",\s*"(.*)"\)')
        params['useragent'] = script.re_first(r'LM.config\("useragent",\s*"(.*)"\)')
        params['siteid'] = response.css('script[src ^= "//fsm.attraqt.com/zones/"]::attr(src)').re_first(
            '.*/zones/(.*).js')
        params['sku'] = script.re_first(r'LM.Sku\s*=\s*\'([^\']*)\';?')
        params['pageurl'] = response.url
        is_sale = script.re_first(r'LM.config\("isSale",\s*"(.*)"\)')
        params['is_sale'] = int(is_sale) if is_sale else None
        return params

    def parse_item(self, response, is_sale):
        item = WhitestuffItem()
        item['retailer'] = 'whitestuff'
        item['market'] = 'UK'
        item['lang'] = 'en'
        item['gender'] = self.product_gender(response)
        item['name'] = self.product_name(response)
        item['brand'] = "whitestuff"
        item['description'] = self.product_description(response)
        item['category'] = self.product_category(response)
        item['url'] = response.url
        item['industry'] = None
        item['currency'] = self.product_currency(response)
        item['image_urls'] = self.product_images(response)
        item['spider_name'] = self.name
        item['price'] = self.product_price(response)
        if is_sale:
            item['previous_price'] = self.product_old_price(response)
        item['url_original'] = response.url
        item['care'] = self.product_care(response)
        item['skus'] = self.get_skus(response)
        item['retailer_sku'] = self.retailer_sku(response)
        return item

    def product_gender(self, response):
        return response.css('meta[property="product:gender"]::attr(content)') \
            .extract_first()

    def product_description(self, response):
        return response.css('div.content > div:first-child::text').extract()

    def product_currency(self, response):
        return response.css('meta[property="product:price:currency"]::attr(content)') \
            .extract_first()

    def product_price(self, response):
        return int(response
                    .css('meta[property="product:price:amount"]::attr(content)')
                    .extract_first().replace('.', ''))

    def product_old_price(self, response):
        return int(response
                   .css('meta[property="og:price:standard_amount"]::attr(content)')
                   .extract_first().replace('.', ''))

    def product_care(self, response):
        return response.css('div.content > div:first-child::text') \
            .re_first('^Care:[\s]*(.*)$')

    def product_color(self, response):
        return response.css('meta[itemprop="color"]::attr(content)').re_first('.+')

    def get_skus(self, response):
        script = response.css('script:contains("var variants")::text').extract_first()
        script = re.sub(r'[\s]', ' ', script)
        variants = re.findall(r'var variants = (\{.+\})\s*var img', script).pop()
        variants = json.loads(variants)
        currency = self.product_currency(response)
        skus = {}
        for variant in variants:
            sku = {}
            sku['color'] = variants[variant]['option1']
            sku['size'] = variants[variant]['option2']
            sku['price'] = int(variants[variant]['line_price'].replace('.', ''))
            sku['currency'] = currency
            sell = variants[variant]['sell']
            if not sell:
                sku['out_of_stock'] = True

            skus[variants[variant]['sku']] = sku
        return skus

    def retailer_sku(self, response):
        return response.css('script:contains("productId:")').re_first("productId:[\s]*'(.*)'")

    def product_images(self, response):
        script_elem = response.css('script:contains("var params")::text')
        script_text = re.sub('[\s]', ' ', script_elem.extract_first())
        json_obj = re.findall(r'var imgItems = (\{[^\}]*\})', script_text).pop()
        image_prefix = re.findall(r'\'large_img\'\),\s*\"prefix\":\"([\w.:\/-]*)\"', script_text).pop()
        json_obj = json.loads(json_obj)
        image_names = []
        for key in json_obj:
            image_names += json_obj[key].strip('#').split('#')

        return [image_prefix + name for name in image_names]

    def product_name(self, response):
        return response.css('meta[itemprop="name"]::attr(content)').re_first('.+')

    def product_category(self, response):
        return response.css('div#crumb > span:last-child meta[itemprop="title"]::attr(content)') \
            .extract()
