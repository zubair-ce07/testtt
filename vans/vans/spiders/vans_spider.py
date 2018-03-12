import html
import json
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse
import urllib.parse
from vans.items import VansItem
from w3lib.url import add_or_replace_parameter


class Mixin:
    start_urls = ["https://www.vans.co.uk/"]
    base_url = "https://www.vans.co.uk/"
    genders = {
        "WOMEN": "Women",
        "MEN": "Men",
        "KIDS": "Kids",
    }


class VansParser(CrawlSpider, Mixin):
    name = "vans_parser"
    skus_api = "https://www.vans.co.uk/webapp/wcs/stores/servlet/VFAjaxProductAvailabilityView?"

    def product_id(self, response):
        return response.xpath('//input[@name="catEntryId"]/@value').extract_first()

    def attribute_id(self, response):
        return response.xpath('//section/@data-attribute-id').extract_first()

    def product_info(self, response):
        product_info = response.xpath('//script[contains(text(),"itemPrices")]/text()').extract_first()
        return json.loads(re.findall('Prices = (.+);', product_info)[0])

    def colour(self, response):
        return response.css('.attr-selected-color-js ::text').extract_first()
    
    def store_id(self, response):
        return response.xpath('//meta[@name="storeId"]/@content').extract_first()
    
    def lang_id(self, response):
        return response.xpath('//meta[@name="langId"]/@content').extract_first()
    
    def sku_ids_url(self, response):
        sku_ids_url = add_or_replace_parameter(self.skus_api, "storeId", self.store_id(response))
        sku_ids_url = add_or_replace_parameter(sku_ids_url, "langId", self.lang_id(response))
        sku_ids_url = add_or_replace_parameter(sku_ids_url, "productId", self.product_id(response))
        sku_ids_url = add_or_replace_parameter(sku_ids_url, "requesttype", "ajax")
        return sku_ids_url

    def gender(self, response):
        gender_info = response.xpath('//script[contains(text(),"pageName")]/text()').extract_first()
        category = re.findall('"([A-Z]+)"', gender_info)[0]

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
        yield scrapy.Request(url=self.sku_ids_url(response), meta={"item": item, "colour": self.colour(response)},
                             dont_filter=True, callback=self.parse_skus)

    def price_text(self, skus_text):
        price_html = skus_text["productPriceHTML"]
        if not price_html:
            return
        unescaped_html = html.unescape(price_html)
        new_response = HtmlResponse(url="", body=unescaped_html, encoding='utf-8')
        return new_response

    def previous_price(self, new_response):
        previous_price = new_response.css('.product-block-price::text').extract_first()
        return previous_price.strip() if previous_price else "None"

    def stock_information(self, skus_text):
        available_sku_ids = []
        for sku_key, sku_value in skus_text["stock"].items():
            if sku_value != 0:
                available_sku_ids.append(sku_key)
        return available_sku_ids

    def price(self, new_response):
        return new_response.xpath('//span/text()').extract()[-1].strip()

    def skus(self, colour, skus_text):
        new_response = self.price_text(skus_text)
        sku_ids = skus_text["attributes"]["7000000000000013954"]
        skus = {}
        for sku_id in sku_ids:
            is_available = 'out_of_stock'
            if str(sku_id["catentryId"][0]) in self.stock_information(skus_text):
                is_available = 'available'
            skus[sku_id["catentryId"][0]] = {
                "size": sku_id["display"],
                "stock": is_available,
                "price": self.price(new_response),
                "previous_price": self.previous_price(new_response),
                "colour": colour,
            }
        return skus

    def parse_skus(self, response):
        item = response.meta["item"]
        colour = response.meta["colour"]
        if response.text:
            skus_text = json.loads(response.text)
            item["skus"] = self.skus(colour, skus_text)
        yield item


class VansCrawler(CrawlSpider, Mixin):
    name = "vans_crawler"
    parser = VansParser()
    products_api = "https://fsm-vfc.attraqt.com/zones-js.aspx?"

    rules = [
        Rule(LinkExtractor(restrict_xpaths='.//a[@class="sub-category-header"]'),
             callback='parse_sub_categories')
    ]

    def form_data_text(self, response):
        return response.xpath('//script[contains(text(),"categorytree")]/text()').extract_first()

    def page_url(self, response):
        return response.xpath('//meta[@property="og:url"]/@content').extract_first()

    def form_data_zones(self, response):
        return response.xpath('//section//div/@lmzone').extract()

    def site_id(self, response):
        site_id_text = response.xpath('//script[contains(text(),"WCS_CONFIG.ATTRAQT")]/text()').extract_first()
        return re.findall('/zones/[a-z0-9-]+', site_id_text)[0][7:]

    def cat_tree_id(self, form_data_text):
        return re.findall('tree : "(.+)\"', form_data_text)[0]

    def config_category(self, form_data_text):
        return re.findall('category : "(.+)\"', form_data_text)[0]

    def collection_id(self, form_data_text):
        return re.findall('collection : "(.+)\"', form_data_text)[0]

    def language(self, form_data_text):
        return re.findall('title : "(.+)\"', form_data_text)[0]

    def parse_sub_categories(self, response):
        form_data_text = self.form_data_text(response)
        sub_cat_url = add_or_replace_parameter(self.products_api, "pageurl", self.page_url(response))
        sub_cat_url = add_or_replace_parameter(sub_cat_url, "zone0", self.form_data_zones(response)[0])
        sub_cat_url = add_or_replace_parameter(sub_cat_url, "zone1", self.form_data_zones(response)[1])
        sub_cat_url = add_or_replace_parameter(sub_cat_url, "config_categorytree", self.cat_tree_id(form_data_text))
        sub_cat_url = add_or_replace_parameter(sub_cat_url, "config_category", self.config_category(form_data_text))
        sub_cat_url = add_or_replace_parameter(sub_cat_url, "config_collection", self.collection_id(form_data_text))
        sub_cat_url = add_or_replace_parameter(sub_cat_url, "siteId", self.site_id(response))
        sub_cat_url = add_or_replace_parameter(sub_cat_url, "config_category_title", self.language(form_data_text))
        sub_cat_url = add_or_replace_parameter(sub_cat_url, "config_country", "GB")
        return scrapy.Request(url=sub_cat_url, dont_filter=True, callback=self.parse_next_pages)

    def parse_next_pages(self, response):
        sku_ids_url = response.url
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
        request_url = add_or_replace_parameter(sku_ids_url, "pageurl",
                                               urllib.parse.urljoin(self.base_url, next_page_url))
        yield scrapy.Request(url=request_url, meta={"sku_id_url": sku_ids_url}, callback=self.parse_next_pages)
