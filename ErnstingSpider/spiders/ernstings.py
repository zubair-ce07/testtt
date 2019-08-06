import json
import re
from datetime import datetime
from math import ceil

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ErnstingSpiderItem


GENDER_MAP = {
    "Mädchenkleidung": "girls",
    "Jungenkleidung": "boys",
    "Babykleidung": "unisex-kids",
    "Damenmode": "women",
    "Herren": "men"
}


class ErnstingsSpider(CrawlSpider):
    name = "ernstings"
    allowed_domains = ["ernstings-family.de"]
    start_urls = ["https://ernstings-family.de/"]
    rules = [
        Rule(LinkExtractor(restrict_css=".main-navigation-holder")),
        Rule(LinkExtractor(restrict_css="#subnavi-"), callback="parse_sub_category", )
    ]

    def parse_sub_category(self, response):
        profile_name = "EF_findProductsBySearchTerm_Details"
        category_id = response.css("meta[name='pageId']::attr(content)").get()
        total_products = self.get_products_count(response)
        total_pages = ceil(total_products / 24) + 1
        for page_no in range(1, total_pages):
            url = f"https://www.ernstings-family.de/search/resources/store/10151/productview/bySearchTerm/*?" \
                  f"pageNumber={page_no}&pageSize=24&categoryId={category_id}&profileName={profile_name}"
            yield Request(url, callback=self.parse_products_api, meta={"category_id": category_id})

    def parse_products_api(self, response):
        category_id = response.meta["category_id"]
        results = json.loads(response.text)

        for result in results["catalogEntryView"]:
            product_id = result["uniqueID"]
            product_url = f"https://www.ernstings-family.de/ProductDisplay?categoryId" \
                          f"={category_id}&productId={product_id}&storeId=10151"
            yield Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        item = ErnstingSpiderItem()
        item["product_id"] = response.css("meta[name='pageId']::attr(content)").get()
        item["name"] = self.clean(response.css(".product-name::text").get())
        item["category"] = response.css(".breadcrumb-list li span[property='name']::text").getall()
        item["url"] = response.url
        item["date"] = datetime.now().timestamp()
        gender = self.map_gender(response.css(".breadcrumb-list li span[property='name']::text").get())
        item["gender"] = gender
        item["description"] = self.get_product_description(response)
        item["care"] = self.get_product_care(response)
        item["img_urls"] = response.css("img.product-view-slide-thumb::attr(src)").getall()
        item["brand"] = response.css(".teaser-brand img::attr(src)").re("(\w+).png")
        item["lang"] = "de"
        item["market"] = "De"
        item["skus"] = self.extract_skus(response)
        yield item

    def extract_skus(self, response):
        skus = {}
        color = self.clean(response.css(".product-detail-product-color::text").get())
        currency = response.css("script::text").re('"commandContextCurrency": "(.+)",')

        size_options = response.css("#select-size-product-detail option")
        for option in size_options:
            out_of_stock = False
            if option.css("[disabled]").get():
                out_of_stock = True

            size = option.css("::text").get()
            sku_key = f"{color}_{size}"
            offer_price = self.clean(response.css(".offer-price::text").get())
            previous_price = self.clean(response.css(".product-price::text").get())
            skus[sku_key] = {
                "size": size,
                "color": color,
                "previous_price": previous_price,
                "offer_price": offer_price,
                "currency": currency,
                "out_of_stock": out_of_stock
            }

        return skus

    @staticmethod
    def get_product_care(response):
        material_xpath = "//div[@class='product-detail-information-contents']" \
                         "//span[contains(.,'Material')]/../.."
        material = response.xpath(material_xpath).css("p::text").extract()
        care_css = ".product-detail-information-icon-list .care-icon-text-wrapper img::attr(alt)"
        care = response.css(care_css).extract()
        return [care, material]

    def get_product_description(self, response):
        description = self.clean(response.css(".product-detail-information-contents p::text").get())
        description_bullets = response.css(".product-detail-information-contents li::text").getall()
        return [description, description_bullets]

    @staticmethod
    def get_products_count(response):
        total_products = response.css("#product-list-load-more-products .btn-label::text").re("\d")
        total_products = "".join(total_products)
        if total_products:
            total_products = int(total_products) + 24
            return total_products
        return 1

    @staticmethod
    def clean(raw_text):
        if raw_text:
            return re.sub('\s+', '', raw_text)

    @staticmethod
    def map_gender(gender):
        if gender in GENDER_MAP:
            return GENDER_MAP[gender]
        return "unisex-adults"

