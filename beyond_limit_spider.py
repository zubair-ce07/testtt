import scrapy
from scrapy.item import Item
from scrapy.spiders import Spider


class Product(Item):
    retailer_sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    care = scrapy.Field()
    gender = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()
    skus = scrapy.Field()


class BeyondLimitSpider(Spider):
    name = "beyond_limit"
    allowed_domains = ["beyondlimits.com"]
    start_urls = ["https://www.beyondlimits.com"]
    gender_terms = [
        "Men",
        "Women",
    ]
    care_terms = [
        "Care tips",
        "Material",
    ]

    def parse(self, response):
        base_category_links = response.css(".ft_cloned--inner .bb_mainmenu--item "
                                           "::attr(data-bbfwhref)").getall()
        yield from [response.follow(base_category_link, callback=self.parse_category)
                    for base_category_link in base_category_links]

    def parse_category(self, response):
        sub_category_links = response.css(".bb_subcat--list ::attr(href)").getall()
        yield from [response.follow(sub_category_link, callback=self.parse_sub_category)
                    for sub_category_link in sub_category_links]

    def parse_sub_category(self, response):
        item_links = response.css(".bb_product--link::attr(href)").getall()
        yield from [response.follow(item_link, callback=self.parse_item) for item_link in
                    item_links]

    def parse_item(self, response):
        item = Product()
        item["url"] = response.url
        item["brand"] = self.extract_brand_name()
        item["name"] = self.extract_item_name(response)
        item["retailer_sku"] = self.extract_retailer_sku(response)
        item["description"] = self.extract_description(response)
        item["image_urls"] = self.extract_image_urls(response)
        item["care"] = self.extract_care(response)
        item["gender"] = self.extract_gender(response)
        item["category"] = self.extract_category(response)
        item["skus"] = self.extract_skus(response)

        return item

    def extract_item_name(self, response):
        return response.css("[itemprop=name]::text").extract_first()

    def extract_retailer_sku(self, response):
        return response.css("[itemprop=productID]::text").get()

    def extract_brand_name(self):
        return "BeyondLimits"

    def extract_gender(self, response):
        raw_genders = response.css("[itemprop=title]::text").getall()
        raw_genders = self.remove_unwanted_spaces(raw_genders)
        return [gender for gender in raw_genders if any(gender_term in gender
                                                        for gender_term in self.gender_terms)]

    def extract_category(self, response):
        raw_category = response.css("[itemprop=title]::text").getall()
        raw_category = self.remove_unwanted_spaces(raw_category)
        return [raw_category_item for raw_category_item in raw_category]

    def extract_care(self, response):
        raw_cares = response.css("#description li::text, #description "
                                 ".MsoNormal span::text").getall()
        return [care_item for care_item in raw_cares if any(care_term in care_item
                                                            for care_term in self.care_terms)]

    def extract_image_urls(self, response):
        return response.css(".bb_pic--navlink::attr(data-bbzoompicurl)").getall()

    def extract_description(self, response):
        raw_description = response.css("#description p::text, #description ::text").get()
        return [description for description in raw_description.split(".") if description]

    def extract_colour(self, response):
        return response.css("#description li::text, .MsoNormal span::text").get()

    def extract_currency(self, response):
        return response.css("[itemprop=priceCurrency]::attr(content)").get()

    def extract_current_price(self, response):
        return response.css("[itemprop=price]::text").get()

    def extract_previous_prices(self, response):
        return response.css(".oldPrice del::text").getall()

    def extract_skus(self, response):
        skus = []
        for item_size in response.css(".bb_form--select [value!=\"\"]::text").getall():
            sku = {
                "colour": self.extract_colour(response),
                "price": self.extract_current_price(response),
                "currency": self.extract_currency(response),
                "previous_prices": self.extract_previous_prices(response),
                "size": item_size,
                "sku_id": f"{self.extract_colour(response)}_{item_size}"
            }
            skus.append(sku)

        return skus

    def remove_unwanted_spaces(self, raw_list):
        return [list_item.strip() for list_item in raw_list if list_item]
