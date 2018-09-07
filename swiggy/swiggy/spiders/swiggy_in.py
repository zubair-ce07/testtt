from csv import DictReader
from json import loads
from collections import namedtuple

from scrapy import Spider, Request
from w3lib.url import add_or_replace_parameter, url_query_parameter

from ..items import MenuItemLoader


class SwiggyInSpider(Spider):
    name = 'swiggy-in'
    allowed_domains = ['www.swiggy.com']

    search_base_url = "https://www.swiggy.com/dapi/restaurants/search"
    restaurent_base_url = "https://www.swiggy.com"
    menu_base_url = "https://www.swiggy.com/dapi/menu/v4/full"
    meal_base_url = "https://www.swiggy.com/meals/"
    thumbnail_url = "https://res.cloudinary.com/swiggy/image/upload/" \
                    "fl_lossy,f_auto,q_auto,w_165,h_165,c_fill/{}"

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    }

    special_categories = ["Recommended", "What's New", "Sharing Packs"]

    Location = namedtuple('Location', ['lng', 'lat'])

    test_locations = [
        Location("77.659309", "12.83957"),
        #Location("80.1842321", "13.0205017"),
        #Location("77.251741", "28.551441")
    ]

    restaurents = ["KFC", "McDonald's", "Burger King", "Domino's"]

    @staticmethod
    def is_valid_reading(reading):
        required_fields = ['Latitude', 'Longitude']
        return all(reading[field] for field in required_fields)

    def read(self, file_name):
        with open(file_name, 'r') as f:
            return [self.Location(r['Longitude'], r['Latitude']) for r in DictReader(f)
                    if self.is_valid_reading(r)]

    def start_requests(self):
        def add_location(url, loc, restaurent):
            url = add_or_replace_parameter(url, "str", restaurent)
            url = add_or_replace_parameter(url, "lat", loc.lat)
            url = add_or_replace_parameter(url, "lng", loc.lng)
            return url

        locations = self.read('locations.csv')
        request_urls = [add_location(self.search_base_url, loc, restaurent)
                        for loc in self.test_locations for restaurent in self.restaurents]

        search_requests = [Request(url=url, callback=self.parse) for url in request_urls]
        return search_requests

    def parse(self, response):
        restaurant_name = url_query_parameter(response.url, "str")
        search_results = loads(response.text)
        restaurants = search_results["data"]["restaurants"][0]["restaurants"]

        for restaurant in restaurants:
            if restaurant_name in restaurant["name"]:
                restaurant_url = "{}/{}/{}".format(self.restaurent_base_url, restaurant["slugs"]["city"],
                                                   restaurant["slugs"]["restaurant"])

                if restaurant_name == "Domino's":
                    lng = url_query_parameter(response.url, "lng")
                    lat = url_query_parameter(response.url, "lat")
                    url = add_or_replace_parameter(self.menu_base_url, "slug",
                                                   restaurant["slugs"]["restaurant"])
                    url = add_or_replace_parameter(url, "lng", lng)
                    url = add_or_replace_parameter(url, "lat", lat)

                    yield Request(url=url, callback=self.parse_dominos, meta={"url": restaurant_url})

                elif restaurant_name in self.restaurents:
                    meta = {"city": restaurant["city"], "locality": restaurant["locality"],
                            "restaurant_name": restaurant_name,
                            "restaurant_id": restaurant["id"]}

                    yield Request(url=restaurant_url, callback=self.parse_restaurant, meta=meta)

    def parse_restaurant(self, response):
        il = MenuItemLoader(response=response)
        il.add_xpath("offer", "//*[contains(@class, '_3AwL7')]/text()")
        il.add_xpath("average_rating", "//*[contains(@class, '_2b42o')]/div[1]//span[1]/text()")
        il.add_xpath("num_of_ratings", "//*[@class='_1De48']/span/text()")
        il.add_value("city", response.meta["city"])
        il.add_value("locality", response.meta["locality"])
        il.add_value("source", "swiggy")
        il.add_value("restaurant", response.meta["restaurant_name"])
        il.add_value("store_id", response.meta["restaurant_id"])
        il.add_value("url", response.url)

        return self.restaurant_category(il.load_item(), response)

    def parse_dominos(self, response):
        il = MenuItemLoader(response=response)
        raw_menu = loads(response.text)["data"]
        il.add_value("average_rating", raw_menu["avgRatingString"])
        il.add_value("num_of_ratings", raw_menu["totalRatingsString"])
        il.add_value("city", raw_menu["city"])
        il.add_value("locality", raw_menu["locality"])
        il.add_value("source", "swiggy")
        il.add_value("url", response.meta["url"])
        il.add_value("restaurant", raw_menu["name"])
        il.add_value("store_id", raw_menu["id"])

        return self.parse_dominos_categories(il.load_item(), response)

    def process_entity(self, il, menu_item):
        il.add_value("title", menu_item["name"])
        il.add_value("description", menu_item["description"])
        thumbnail_url = self.thumbnail_url.format(menu_item["cloudinaryImageId"])
        il.add_value("thumbnail", thumbnail_url)

        if menu_item["isVeg"]:
            il.add_value("veg", True)
        else:
            il.add_value("veg", False)

        if menu_item["price"]:
            il.add_value("price", str(menu_item["price"]))

        if menu_item.get("ribbon"):
            il.add_value("promotion", menu_item["ribbon"]["text"])

        return il

    def process_variant(self, il, variant):
        il.add_value("size", variant["name"])
        il.add_value("price", str(variant["price"]))
        return il

    def parse_dominos_categories(self, item, response):

        raw_menu = loads(response.text)["data"]

        categories = raw_menu["menu"]["widgets"]
        raw_items = raw_menu["menu"]["items"]

        for category in categories:
            cat_il = MenuItemLoader(item=item.copy(), response=response)
            cat_il.add_value("category", category["name"])

            if category["name"] == "Everyday Value Offers":
                cat_item = cat_il.load_item()

                for entitie in category["entities"]:
                    entity_il = MenuItemLoader(item=cat_item.copy(), response=response)
                    entity_il.add_value("subcategory", entitie["text"])
                    entity_il.add_value("subcategory_description", entitie["subText"])
                    url = "{}{}".format(self.meal_base_url, entitie["id"])
                    url = add_or_replace_parameter(url, "restId", raw_menu["id"])
                    yield Request(url=url, callback=self.process_meal, meta={"item": entity_il.load_item()})

                continue

            if not category["type"] == "category":
                cat_il.add_value("special_category", "Y")

            if category["entities"]:
                cat_il.add_value("subcategory", category["name"])
                cat_item = cat_il.load_item()

                for entitie in category["entities"]:
                    menu_il = MenuItemLoader(item=cat_item.copy(), response=response)
                    menu_item = raw_items[str(entitie["id"])]
                    menu_il = self.process_entity(menu_il, menu_item)

                    variants = menu_item.get("variantsV2")
                    if not variants:
                        yield menu_il.load_item()
                    else:
                        entity_item = menu_il.load_item()
                        for variant in variants["variant_groups"]:
                            if not variant["name"] == "Size":
                                continue

                            for variation in variant["variations"]:
                                variant_il = MenuItemLoader(item=entity_item.copy(), response=response)
                                variant_il = self.process_variant(variant_il, variation)

                                yield variant_il.load_item()

            if category["widgets"]:
                cat_item = cat_il.load_item()

                for sub_cat in category["widgets"]:
                    sub_cat_il = MenuItemLoader(cat_item.copy(), response=response)
                    sub_cat_il.add_value("subcategory", sub_cat["name"])
                    sub_cat_item = sub_cat_il.load_item()

                    for entitie in sub_cat["entities"]:
                        menu_il = MenuItemLoader(item=sub_cat_item.copy(), response=response)
                        menu_item = raw_items[str(entitie["id"])]
                        menu_il = self.process_entity(menu_il, menu_item)

                        variants = menu_item.get("variantsV2")
                        if not variants:
                            yield menu_il.load_item()
                        else:
                            entity_item = menu_il.load_item()
                            for variant in variants["variant_groups"]:

                                if not variant["name"] == "Size":
                                    continue

                                for variation in variant["variations"]:
                                    variant_il = MenuItemLoader(item=entity_item.copy(), response=response)
                                    variant_il = self.process_variant(variant_il, variation)

                                    yield variant_il.load_item()

    def process_meal(self, response):

        raw_meals_xpath = "//script[contains(text(), 'INITIAL_STATE')]"
        raw_meals_re = "INITIAL_STATE__ = (.*);   window"
        raw_meals = loads(response.xpath(raw_meals_xpath).re_first(raw_meals_re))
        meal_groups = raw_meals["meals"]["groups"]

        for meal_group in meal_groups:
            for item in meal_group["group"]["items"]:
                menu_il = MenuItemLoader(item=response.meta["item"].copy(), response=response)
                menu_il = self.process_entity(menu_il, item)

                variants = item.get("variantsV2")

                if not variants:
                    yield menu_il.load_item()
                else:
                    entity_item = menu_il.load_item()
                    for variant in variants["variant_groups"]:
                        if not variant["name"] == "Size":
                            continue
                        for variation in variant["variations"]:
                            variant_il = MenuItemLoader(item=entity_item.copy(), response=response)
                            variant_il = self.process_variant(variant_il, variation)

                            yield variant_il.load_item()

    def restaurant_category(self, item, response):
        categoires = response.xpath("//*[contains(@class, '_2dS-v')]")

        def process_menu_item(il):
            il.add_xpath("title", "descendant-or-self::*[@itemprop='name']/text()")
            il.add_xpath("thumbnail", "descendant-or-self::*[@itemprop='image']/@content")
            il.add_xpath("price", "descendant-or-self::*[@class='bQEAj']/text()")
            il.add_xpath("description",
                         "descendant-or-self::*[@class='_2aOqz _1d7fc' or "
                         "@class='_2aOqz _1xb2E']/text()")

            if il.get_xpath("descendant-or-self::*[contains(@class, '_3x58u') or "
                            "contains(@class, '_1xb2E')]"):
                il.add_value("veg", True)
            else:
                il.add_value("veg", False)

            il.add_xpath("promotion", "descendant-or-self::*[contains(@class, '_22D_E')]/text()")

            return il

        for category in categoires:
            il = MenuItemLoader(item=item.copy(), selector=category)
            category_name = il.get_xpath("h2/text()")

            if category_name[0] in self.special_categories:
                il.add_value("special_category", "Y")

            il.add_xpath("category", "h2/text()")
            sub_categoires = category.xpath("descendant-or-self::div[@class='_1Jgt5']")

            if sub_categoires:
                cat_item = il.load_item()

                for sub_category in sub_categoires:
                    il_sub = MenuItemLoader(item=cat_item.copy(), selector=sub_category)
                    il_sub.add_xpath("subcategory", "h3/text()")
                    menu_items = sub_category.xpath("descendant-or-self::div[@itemtype]")
                    sub_cat_item = il_sub.load_item()

                    for menu_item in menu_items:
                        il_menu_item = MenuItemLoader(sub_cat_item.copy(), selector=menu_item)
                        il_menu_item = process_menu_item(il_menu_item)
                        yield il_menu_item.load_item()

            else:
                il.add_xpath("subcategory", "h2/text()")
                menu_items = category.xpath("descendant-or-self::div[@itemtype]")
                cat_item = il.load_item()

                for menu_item in menu_items:
                    il_menu_item = MenuItemLoader(cat_item.copy(), selector=menu_item)
                    il_menu_item = process_menu_item(il_menu_item)
                    yield il_menu_item.load_item()
