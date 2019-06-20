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

    def parse(self, response):
        base_category_links = response.css("div.ft_cloned--inner li.bb_mainmenu--item "
                                           "a::attr(data-bbfwhref)").extract()
        yield from [response.follow(base_category_link, callback=self.parse_base_category_links)
                    for base_category_link in base_category_links]

    def parse_base_category_links(self, response):
        sub_category_links = response.css("ul.bb_subcat--list a::attr(href)").extract()
        yield from [response.follow(sub_category_link, callback=self.parse_sub_category_links)
                    for sub_category_link in sub_category_links]

    def parse_sub_category_links(self, response):
        item_links = response.css("li.productData a.bb_product--link::attr(href)").extract()
        item_links = self.remove_duplicate_links(item_links)
        yield from [response.follow(item_link, callback=self.parse_item) for item_link in
                    item_links]

    def parse_item(self, response):
        item = Product()
        selector = response.css(".bb_art--content")
        item["url"] = response.url
        item["brand"] = "BeyondLimits"
        item["name"] = self.extract_item_name(selector)
        item["retailer_sku"] = self.extract_retailer_sku(selector)
        item["description"] = self.extract_description(response)
        item["image_urls"] = self.extract_image_urls(response)
        item["care"] = self.extract_care(response)
        item["gender"] = self.extract_gender(response)
        item["category"] = self.extract_category(response)
        item["skus"] = self.extract_skus(response)
        return item

    def remove_duplicate_links(self, item_links):
        return list(set(item_links))

    def extract_item_name(self, selector):
        return selector.css("[itemprop=name]::text").extract_first()

    def extract_retailer_sku(self, selector):
        return selector.css("[itemprop=productID]::text").extract_first()

    def extract_gender(self, response):
        return response.css("div#breadCrumb [itemprop=title]::text").extract()[1].strip()

    def extract_category(self, response):
        raw_category = response.css("div#breadCrumb [itemprop=title]::text").extract()
        return [raw_category_item.strip() for raw_category_item in raw_category]

    def extract_care(self, response):
        raw_care = response.css("div#description ul > li::text").extract()
        if not raw_care:
            raw_care = response.css("div#description ul > li.MsoNormal span::text").extract()
        if raw_care:
            raw_care.pop(0)

        return raw_care

    def extract_image_urls(self, response):
        return response.css("ul.bb_pic--nav a.bb_pic--navlink::attr(data-bbzoompicurl)").extract()

    def extract_description(self, response):
        raw_description = response.css("div#description p::text").extract_first()
        if not raw_description:
            raw_description = response.css("div#description::text").extract_first()

        return [description.rstrip() for description in raw_description.split(".") if description]

    def extract_color(self, response):
        raw_color = response.css("div#description li::text").extract_first()
        if not raw_color:
            raw_color = response.css("div#description li.MsoNormal span::text").extract_first()
        if raw_color:
            raw_color = raw_color.split(":")[1].strip().rstrip()

        return raw_color

    def extract_currency(self, response):
        return response.css("[itemprop=priceCurrency]::attr(content)").extract_first()

    def extract_current_price(self, response):
        return response.css("[itemprop=price]::text").extract_first()

    def extract_previous_prices(self, response):
        return response.css("span.oldPrice del::text").extract()

    def extract_sizes(self, response):
        return response.css("select.bb_form--select option[value!=\"\"]::text").extract()

    def extract_skus(self, response):
        skus = []
        for item_size in self.extract_sizes(response):
            sku = {
                "colour": self.extract_color(response),
                "price": self.extract_current_price(response),
                "currency": self.extract_currency(response),
                "previous_prices": self.extract_previous_prices(response),
                "size": item_size,
                "sku_id": f"{self.extract_color(response)}_{item_size}"
            }
            skus.append(sku)

        return skus
