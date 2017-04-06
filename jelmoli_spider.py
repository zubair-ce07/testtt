import json

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import add_or_replace_parameter

from JelmoliShop.items import JelmoliItem


class JelmoliSpider(CrawlSpider):
    name = "jelmoli_spider"
    allowed_domains = ["jelmoli-shop.ch"]
    start_urls = ["https://www.jelmoli-shop.ch/"]
    deny_r = ['geräte',
              'multimedia',
              'ausrüstung',
              'werkzeug',
              'maschinen',
              'heizen',
              'klima',
              'spielzeug',
              'küche',
              'elektronik']

    rules = [
        Rule(LinkExtractor(restrict_css=".link-product", deny=deny_r),
             callback="parse_product_details"),

        Rule(LinkExtractor(restrict_css=".nav-content", deny=deny_r),
             callback="parse_subcategory_details"),

        Rule(LinkExtractor(restrict_css="#nav-main-list", deny=deny_r)),
    ]

    image_url_t = "https://images.jelmoli-shop.ch/asset/mmo/formatz/{image_name}"
    genders = {'Damen': 'women', 'Herren': 'men', 'Kinder': 'unisex-kids'}

    @staticmethod
    def get_subcategory_pagination_url(category_url, page):
        return add_or_replace_parameter(category_url, "Page", page)

    def parse_subcategory_details(self, response):
        total_pages = response.xpath("(//div/@data-page)[last()]").extract_first(default='1')
        for page in range(int(total_pages)):
            subcategory_pagination_url = self.get_subcategory_pagination_url(response.url, "P{}".format(page))
            yield Request(url=subcategory_pagination_url, dont_filter=True)

    def parse_product_details(self, response):
        product_details_json = self.get_product_json(response)

        product = JelmoliItem()
        product["brand"] = self.get_brand(product_details_json)
        product["care"] = self.get_care(product_details_json)
        product["category"] = self.get_category(response)
        product["description"] = self.get_description(product_details_json)
        product["industry"] = self.get_industry(response)
        product["image_urls"] = self.get_image_urls(product_details_json)
        product["market"] = "CH"
        product["name"] = self.get_name(product_details_json)
        product["lang"] = self.get_lang(response)
        product["retailer"] = "jelmoli-ch"
        product["retailer_sku"] = self.get_retailer_sku(product_details_json)
        product["skus"] = self.get_skus(product_details_json)
        product["url"] = response.url

        if not product["industry"]:
            product["gender"] = self.get_gender(product["category"])

        print(product)

    @staticmethod
    def get_product_json(response):
        xpath = "//script[@class='data-product-detail']/text()"
        product_details = response.xpath(xpath).extract_first()
        return json.loads(product_details)

    @staticmethod
    def get_brand(product_json):
        product_variations = product_json["variations"]
        if product_variations:
            sku = next(iter(product_variations))
            return product_variations[sku]["manufacturerName"]

    @staticmethod
    def get_care(product_json):
        sel = Selector(text=product_json["tags"]["T0"])
        care = [sel.css("::text").extract_first()]

        product_details = Selector(text=product_json["tags"]["T2"])
        if product_details:
            xpath = "//td[contains(.,'Materialzusammensetzung') or " \
                    "contains(., 'Applikationen')]//following-sibling::td//text()"
            care.extend(product_details.xpath(xpath).extract())
        return care

    @staticmethod
    def get_category(response):
        xpath = "//li[contains(@typeof,'Breadcrumb')]//text()[normalize-space()]"
        return response.xpath(xpath).extract()

    @staticmethod
    def get_description(product_json):
        sel = Selector(text=product_json["tags"]["T0"])
        description = sel.css("::text").extract()

        product_details = Selector(text=product_json["tags"]["T2"])
        if product_details:
            description.extend(product_details.xpath("//td//following-sibling::td//text()").extract())

        return description

    def get_gender(self, categories):
        for category in categories:
            if category in self.genders:
                return self.genders[category]

        return 'unisex-adult'

    def get_industry(self, response):
        categories = self.get_category(response)
        if any(category in ['Wohnen', 'Baumarket'] for category in categories):
            return 'homeware'

    def get_image_urls(self, product_json):
        product_images = product_json["galleryImages"]
        return [self.image_url_t.format(image_name=image["image"]) for image in product_images]

    @staticmethod
    def get_lang(response):
        return response.xpath("//html/@lang").extract_first()

    @staticmethod
    def get_name(product_json):
        return product_json["nameWithoutManufacturer"]

    @staticmethod
    def get_retailer_sku(product_json):
        return product_json["sku"]

    @staticmethod
    def get_skus(product_json):
        skus = {}
        product_variations = product_json["variations"]
        product_skus = product_variations.keys()
        for sku in product_skus:
            sku_details = product_variations[sku]
            skus[sku] = {"colour": sku_details["variationValues"]["Var_Article"],
                         "currency": sku_details["currentPrice"]["currency"],
                         "price": sku_details["currentPrice"]["value"],
                         "size": sku_details["size"]}
        return skus
