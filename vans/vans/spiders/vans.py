import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import urllib.parse
import json
from vans.items import VansItem
import re


class VansSpider(CrawlSpider):
    name = "vans_crawler"
    start_urls = ["https://www.vans.co.uk/"]
    base_url = "https://www.vans.co.uk/"
    products_api = "https://fsm-vfc.attraqt.com/zones-js.aspx?"
    skus_api = "https://www.vans.co.uk/webapp/wcs/stores/servlet/VFAjaxProductAvailabilityView?"

    rules = [
        Rule(LinkExtractor(restrict_xpaths='.//a[@class="sub-category-header"]'),
             callback='parse_sub_categories')
    ]
    genders = {
        "WOMEN": "Women",
        "MEN": "Men",
        "KIDS": "Kids",
    }

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
                                 callback=self.parse_product)
        next_page_url = new_response.xpath('//a[@title="Go to next page"]/@href').extract_first()
        if not next_page_url:
            return
        form_data["pageurl"] = urllib.parse.urljoin(self.base_url, next_page_url)
        request_url = self.products_api+urlencode(form_data)
        yield scrapy.Request(url=request_url, dont_filter=True, meta={"form_data": form_data}, callback=self.next_pages)

    def product_id(self, response):
        return response.xpath('//div[@id="product-imgs"]/@data-product-id').extract_first()

    def attribute_id(self, response):
        return response.xpath('//section/@data-attribute-id').extract_first()

    def product_info(self, response):
        product_info = response.xpath('//script[contains(text(),"itemPrices")]/text()').extract_first()
        return json.loads(re.findall('Prices = (.+);', product_info)[0])

    def available_color(self, response):
        return response.css('.attr-selected-color-js ::text').extract_first()

    def sku_ids_url(self, response):
        params = {
            'storeId': self.store_id(response),
            'langId': self.language_id(response),
            'productId': self.product_id(response),
            'requesttype': 'ajax',
        }
        return self.skus_api+urlencode(params)

    def skus(self, response):
        size_ids = response.xpath('//option/@data-attribute-value').extract()
        skus = {}
        sku = self.product_info(response)[self.product_id(response)]["pricing"][self.attribute_id(response)]
        for size_id in size_ids:
            sku_id = sku[size_id]["sku"][0]
            skus[sku_id] = {
                "price": sku[size_id]["lowPrice"],
                "previous_price": sku[size_id]["highPrice"],
                "color": self.available_color(response),
                "size": size_id,
            }
        return skus

    def gender(self, response):
        gender_info = response.xpath('//script[contains(text(),"pageName")]/text()').extract_first()
        category = re.findall('Name":"[A-Z]+', gender_info)[0][7:]
        return self.genders.get(category) or 'Adults'

    def parse_product(self, response):
        item = VansItem()
        item["title"] = response.xpath('//h1[@class="product-info-js"]/text()').extract()
        item["description"] = response.css('.desc-container::text').extract()[0]
        item["composition"] = response.css('.desc-container::text').extract()[1:]
        item["retailer_id"] = self.product_id(response)
        item["url"] = response.url
        item["images_url"] = response.css('.selected-view-js img::attr(src)').extract()
        item["gender"] = self.gender(response)

        yield scrapy.Request(url=self.sku_ids_url(response), meta={"item": item, "skus": self.skus(response)},
                             dont_filter=True, callback=self.parse_sku_ids)

    def parse_sku_ids(self, response):
        item = response.meta["item"]
        skus = response.meta["skus"]
        available_sku_ids = []
        if response.text:
            sku_ids_content = json.loads(response.text)
            available_stock = sku_ids_content["stock"]
            if available_stock:
                for sku_key, sku_value in available_stock.items():
                    if sku_value != 0:
                        available_sku_ids.append(sku_key)
                for sku_id in skus:
                    if str(sku_id) in available_sku_ids:
                        skus[sku_id].update({"stock": "available"})
                    else:
                        skus[sku_id].update({"stock": "out_of_stock"})
        item["skus"] = skus
        yield item



