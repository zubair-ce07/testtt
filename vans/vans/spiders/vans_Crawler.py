import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import urllib.parse
import re
from vans.spiders.vans_parser import VansParser


class VansCrawler(CrawlSpider):
    name = "vans_crawler"
    start_urls = ["https://www.vans.co.uk/"]
    parser = VansParser()
    base_url = "https://www.vans.co.uk/"
    products_api = "https://fsm-vfc.attraqt.com/zones-js.aspx?"

    rules = [
        Rule(LinkExtractor(restrict_xpaths='.//a[@class="sub-category-header"]'),
             callback='parse_sub_categories')
    ]

    def form_data_details(self, response):
        return response.xpath('//script[contains(text(),"categorytree")]/text()').extract_first()

    def page_url(self, response):
        return response.xpath('//meta[@property="og:url"]/@content').extract_first()

    def form_data_zones(self, response):
        return response.xpath('//section//div/@lmzone').extract()

    def site_id(self, response):
        site_id_text = response.xpath('//script[contains(text(),"WCS_CONFIG.ATTRAQT")]/text()').extract_first()
        return re.findall('/zones/[a-z0-9-]+', site_id_text)[0][7:]

    def category_tree_id(self, response):
        return re.findall('tree : "(.+)\"', self.form_data_details(response))[0]

    def config_category(self, response):
        return re.findall('category : "(.+)\"', self.form_data_details(response))[0]

    def collection_id(self, response):
        return re.findall('collection : "(.+)\"', self.form_data_details(response))[0]

    def language(self, response):
        return re.findall('title : "(.+)\"', self.form_data_details(response))[0]

    def form_data_lang(self, response):
        return response.xpath('//meta[@name="locale"]/@content').extract_first()

    def language_id(self, response):
        return response.xpath('//meta[@name="langId"]/@content').extract_first()

    def store_id(self, response):
        return response.xpath('//meta[@name="storeId"]/@content').extract_first()

    def parse_sub_categories(self, response):
        form_data = {
            'pageurl': self.page_url(response),
            'zone0': self.form_data_zones(response)[0],
            'zone1': self.form_data_zones(response)[1],
            'siteId': self.site_id(response),
            'config_categorytree': self.category_tree_id(response),
            'config_category': self.config_category(response),
            'config_collection': self.collection_id(response),
            'config_category_title': self.language(response),
            'culture': self.form_data_lang(response),
            'currency': 'GBP_GB',
            'language': self.form_data_lang(response),
            'region': self.form_data_lang(response),
            'config_currency': 'GBP_GB',
            'config_country': 'GB',
            'config_culture': self.form_data_lang(response),
            'config_language': self.form_data_lang(response),
            'config_languageid': self.language_id(response),
            'config_storeid': self.store_id(response),
            'config_region': self.form_data_lang(response),
            'config_currencysymbol': response.xpath('//span[@class="country-currency"]/text()').extract_first()[0],
        }
        request_url = self.products_api+urlencode(form_data)
        return scrapy.Request(url=request_url, meta={"form_data": form_data}, dont_filter=True,
                              callback=self.next_pages)

    def next_pages(self, response):
        form_data = response.meta["form_data"]
        html_content = re.findall('"html":"(.+)",', response.text)[0].replace('\\', '')
        new_response = HtmlResponse(url="", body=html_content, encoding='utf-8')
        product_urls = new_response.xpath('//a[@class="product-block-pdp-url pdp-url-js"]/@href').extract()
        if not product_urls:
            return
        for product_url in product_urls:
            yield scrapy.Request(url=urllib.parse.urljoin(self.base_url, product_url), dont_filter=True,
                                 callback=self.parser.parse_product)
        next_page_url = new_response.xpath('//a[@title="Go to next page"]/@href').extract_first()
        if not next_page_url:
            return
        form_data["pageurl"] = urllib.parse.urljoin(self.base_url, next_page_url)
        request_url = self.products_api+urlencode(form_data)
        yield scrapy.Request(url=request_url, dont_filter=True, meta={"form_data": form_data}, callback=self.next_pages)
