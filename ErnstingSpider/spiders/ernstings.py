import json
from datetime import datetime

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ErnstingSpiderItem


class ErnstingsSpider(CrawlSpider):
    name = "ernstings"
    allowed_domains = ["ernstings-family.de"]
    start_urls = ["https://ernstings-family.de/"]
    rules = [
        Rule(LinkExtractor(restrict_css=".main-navigation-holder"), follow=True),
        Rule(LinkExtractor(restrict_css="#subnavi-"), callback="parse_product_link",)
    ]

    def parse_product_link(self, response):
        profile_name = "EF_findProductsBySearchTerm_Details"
        category_id = response.css("meta[name='pageId']::attr(content)").get()
        store_id = response.css("script::text").re('"storeId": "(.+)",')
        store_id = "".join(store_id)
        url = f"https://www.ernstings-family.de/search/resources/store/10151/productview/" \
            f"bySearchTerm/*?&categoryId={category_id}&profileName={profile_name}"
        parameters = {
            "meta": {
                "category_id": category_id,
                "store_id": store_id
            }
        }
        yield Request(url, callback=self.parse_product, **parameters)

    def parse_product(self, response):
        item = ErnstingSpiderItem()
        color = []
        category_id = response.meta["category_id"]
        store_id = response.meta["store_id"]
        results = json.loads(response.text)

        for result in results["catalogEntryView"]:
            product_id = result["uniqueID"]
            parent_category = result["xcatentry_categoryname"]
            sub_category = result["shortDescription"]
            name = result["name"]

            for attribute in result["attributes"]:
                if "Farbe" in attribute["name"]:
                    color = [value["value"] for value in attribute["values"]]
                    break

            is_sale = bool(int(result["issale"]))
            product_price = result["productPrice"]
            skus = self.extract_skus(result["sKUs"], is_sale, color, product_price)
            product_url = f"https://www.ernstings-family.de/ProductDisplay?categoryId" \
                f"={category_id}&productId={product_id}&storeId={store_id}"
            item["id"] = product_id
            item["name"] = name
            item["category"] = f"{parent_category}/{sub_category}"
            item["url"] = product_url
            item["date"] = datetime.now().timestamp()
            item["skus"] = skus
            yield Request(product_url, callback=self.parse_gender, meta={"item": item})

    def parse_gender(self, response):
        item = response.meta["item"]
        gender = response.css(".breadcrumb-list li span[property='name']::text").get()
        gender = self.map_gender(gender)
        description = response.css(".product-detail-information-contents p::text").get()
        description_bullets = response.css(".product-detail-information-contents li::text").get()
        description = [description, description_bullets]
        care_css = ".product-detail-information-icon-list .care-icon-text-wrapper img::attr(alt)"
        care = response.css(care_css).extract()
        img_urls = response.css("img.product-view-slide-thumb::attr(src)").getall()
        brand = response.css("title::text").re("Ernsting's family")
        lang = response.css("html::attr(lang)").get()
        market = response.css("script::text").re('"googleMapsCountry": "(.+)",')
        item["gender"] = gender
        item["description"] = description
        item["care"] = care
        item["img_urls"] = img_urls
        item["brand"] = brand
        item["lang"] = lang
        item["market"] = market
        yield item

    @staticmethod
    def extract_skus(skus, is_sale, color, product_price):
        product_skus = []
        for sku in skus:
            actual_price = product_price
            offer_price = []
            currency = []
            size = []
            if is_sale:
                offer_price = [price["value"] for price in sku["price"] if price["usage"] == "Offer"]

            for price in sku["price"]:
                currency = price["currency"]
                break

            for attribute in sku["attributes"]:
                if "Größe" in attribute["name"]:
                    size = [value["value"] for value in attribute["values"]]
                    break

            out_of_stock = True
            if sku["xsku_inventoryStatus"] == "Available":
                out_of_stock = False

            product_sku = {
                "size": size,
                "color": color,
                "previous_price": actual_price,
                "offer_price": offer_price,
                "currency": currency,
                "out_of_stock": out_of_stock
            }
            product_skus.append(product_sku)
        return product_skus
    @staticmethod
    def map_gender(gender):
        if "Mädchen" in gender:
            return "girls"

        elif "Jungen" in gender:
            return "boys"

        elif "Damen" in gender:
            return "women"

        return "unisex-kids"

