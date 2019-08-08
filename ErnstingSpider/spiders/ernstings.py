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


def clean(raw_text):
    if not raw_text:
        return None

    if type(raw_text) is list:
        return [re.sub('\s+', '', raw_text) for raw_text in raw_text if raw_text.strip()]

    return re.sub('\s+', '', raw_text)


class ErnstingsSpider(CrawlSpider):
    name = "ernstings"
    allowed_domains = ["ernstings-family.de"]
    start_urls = ["https://ernstings-family.de/"]
    product_api_url_t = "https://www.ernstings-family.de/search/resources/store/10151/" \
                        "productview/bySearchTerm/*?pageNumber={page_no}&pageSize=24&" \
                        "categoryId={category_id}&profileName=EF_findProductsBySearchTerm_Details"
    product_url_t = "https://www.ernstings-family.de/ProductDisplay?categoryId" \
                    "={category_id}&productId={product_id}&storeId=10151"
    rules = [
        Rule(LinkExtractor(restrict_css=".main-navigation-holder")),
        Rule(LinkExtractor(restrict_css="#subnavi-"), callback="parse_sub_category")
    ]

    def parse_sub_category(self, response):
        category_id = response.css("meta[name='pageId']::attr(content)").get()

        total_pages = self.get_pages_count(response)
        for page_no in range(1, total_pages):
            url = self.product_api_url_t.format(page_no=page_no, category_id=category_id)
            yield Request(url, callback=self.parse_products_api)

    def parse_products_api(self, response):
        results = json.loads(response.text)
        url = results["resourceId"]
        pattern = re.compile("categoryId=(\d+)")
        category_id = pattern.search(url).group(1)

        for result in results["catalogEntryView"]:
            product_id = result["uniqueID"]
            product_url = self.product_url_t.format(category_id=category_id, product_id=product_id)
            yield Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        item = ErnstingSpiderItem()
        item["product_id"] = response.css("meta[name='pageId']::attr(content)").get()
        item["name"] = clean(response.css(".product-name::text").get())
        item["category"] = response.css(".breadcrumb-list li span[property='name']::text").getall()
        item["url"] = response.url
        item["date"] = datetime.now().timestamp()
        item["gender"] = self.extract_gender(response)
        item["description"] = self.get_product_description(response)
        item["care"] = self.get_product_care(response)
        item["img_urls"] = response.css(".product-view-slide-holder a::attr(href)").getall()
        item["brand"] = response.css(".teaser-brand img::attr(src)").re("(\w+).png")
        item["lang"] = "de"
        item["market"] = "De"
        item["skus"] = self.extract_skus(response)
        yield item

    @staticmethod
    def get_pages_count(response):
        total_products = int(response.css(".product-count-holder::text").re_first("(\d+)"))
        return ceil(total_products / 24) + 1

    @staticmethod
    def extract_gender(response):
        gender = response.css(".breadcrumb-list li span[property='name']::text").get()
        return GENDER_MAP.get(gender, "unisex-adults")

    @staticmethod
    def get_product_description(response):
        description_xpath = "//div[@class='product-detail-information-contents']" \
                            "//span[contains(.,'Details')]/../.."
        return clean(response.xpath(description_xpath).css("p::text, li::text").getall())

    @staticmethod
    def get_product_care(response):
        material_xpath = "//div[@class='product-detail-information-contents']" \
                         "//span[contains(.,'Material')]/../.."
        material = clean(response.xpath(material_xpath).css("p::text, li::text").getall())
        care = clean(response.css(".care-icon-text-wrapper img::attr(alt)").getall())
        return material + care

    @staticmethod
    def extract_skus(response):
        skus = {}
        color = clean(response.css(".product-detail-product-color::text").get())
        currency = response.css("script::text").re('"commandContextCurrency": "(.+)",')
        price = clean(response.css(".offer-price::text").get())
        previous_price_css = "product-price" if not price else "strike-price"
        previous_price = clean(response.css(f".{previous_price_css}::text").getall())
        common_sku = {
            "color": color,
            "currency": currency,
            "previous_price": previous_price,
            "price": price,
        }

        size_options = response.css("#select-size-product-detail option")
        for option in size_options:
            sku = common_sku
            out_of_stock = True if option.css("[disabled]") else False
            size = option.css("::text").get()
            sku_key = f"{color}_{size}"
            sku["size"] = size
            sku["out_of_stock"] = out_of_stock
            skus[sku_key] = sku

        return skus
