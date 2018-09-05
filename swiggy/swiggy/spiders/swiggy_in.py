from json import loads

from scrapy import Spider, Request
from w3lib.url import add_or_replace_parameter, url_query_parameter

from ..items import McDonaldsItemLoader


class SwiggyInSpider(Spider):
    name = 'swiggy-in'
    allowed_domains = ['www.swiggy.com']

    search_base_url = "https://www.swiggy.com/dapi/restaurants/search"
    restaurent_base_url = "https://www.swiggy.com"

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    }

    locations = [
        {
            "lat": "19.1185712",
            "lng": "72.9113962"
        }
    ]

    restaurents = ["KFC", "McDonald's", "Burger King", "Domino's"]

    def start_requests(self):
        def add_location(url, loc, restaurent):
            url = add_or_replace_parameter(url, "str", restaurent)
            url = add_or_replace_parameter(url, "lat", loc["lat"])
            url = add_or_replace_parameter(url, "lng", loc["lng"])
            return url

        request_urls = [add_location(self.search_base_url, loc, restaurent)
                        for loc in self.locations for restaurent in self.restaurents]

        search_requests = [Request(url=url, callback=self.parse) for url in request_urls]
        return search_requests

    def parse(self, response):
        restaurant_name = url_query_parameter(response.url, "str")
        search_results = loads(response.text)
        restaurants = search_results["data"]["restaurants"][0]["restaurants"]
        for restaurant in restaurants:
            if restaurant_name in restaurant["name"]:
                url = "{}/{}/{}".format(self.restaurent_base_url, restaurant["slugs"]["city"]
                                        , restaurant["slugs"]["restaurant"])
                if restaurant_name == "KFC":
                    meta = {"city": restaurant["city"], "locality": restaurant["locality"],
                            "restaurant_name": restaurant_name,
                            "restaurant_id": restaurant["id"]}
                    yield Request(url=url, callback=self.parse_mcdonalds, meta=meta)

    def parse_mcdonalds(self, response):
        il = McDonaldsItemLoader(response=response)
        il.add_xpath("offer", "//*[contains(@class, '_3AwL7')]/text()")
        il.add_xpath("average_rating", "//*[contains(@class, '_2b42o')]/div[1]//span[1]/text()")
        il.add_xpath("num_of_ratings", "//*[@class='_1De48']/span/text()")
        il.add_value("city", response.meta["city"])
        il.add_value("locality", response.meta["locality"])
        il.add_value("source", "swiggy")
        il.add_value("restaurant", response.meta["restaurant_name"])
        il.add_value("store_id", response.meta["restaurant_id"])
        il.add_value("url", response.url)

        return self.mcd_category(il.load_item(), response)

    def mcd_category(self, item, response):
        categoires = response.xpath("//*[contains(@class, '_2dS-v')]")

        for category in categoires:
            il = McDonaldsItemLoader(item=item, selector=category)
            il.add_xpath("category", "h2/text()")
            sub_categoires = category.xpath("descendant-or-self::div[@class='_1Jgt5']")

            if sub_categoires:
                for sub_category in sub_categoires:
                    il_sub = McDonaldsItemLoader(item=il.load_item(), selector=sub_category)
                    il_sub.add_xpath("subcategory", "h3/text()")
                    menu_items = sub_category.xpath("descendant-or-self::div[@itemtype]")

                    for menu_item in menu_items:
                        il_menu_item = McDonaldsItemLoader(il_sub.load_item(), selector=menu_item)
                        il_menu_item.add_xpath("title", "descendant-or-self::*[@itemprop='name']/text()")
                        il_menu_item.add_xpath("thumbnail", "descendant-or-self::*[@itemprop='image']/@content")
                        il_menu_item.add_xpath("price", "descendant-or-self::*[@class='bQEAj']/text()")
                        il_menu_item.add_xpath("description",
                                               "descendant-or-self::*[@class='_2aOqz _1d7fc']/text()")

                        if il_menu_item.get_xpath("descendant-or-self::*[contains(@class, '_3x58u') or "
                                                  "contains(@class, '_1xb2E')]"):
                            il_menu_item.add_value("veg", True)
                        else:
                            il_menu_item.add_value("veg", False)

                        if il_menu_item.get_xpath("descendant-or-self::*[contains(@class, '_22D_E')]"):
                            il_menu_item.add_xpath("promotion",
                                                   "descendant-or-self::*[contains(@class, '_22D_E')]/text()")
                        else:
                            il_menu_item.add_value("promotion", "None")

                        yield il_menu_item.load_item()

            else:
                il.add_xpath("subcategory", "h2/text()")
                menu_items = category.xpath("descendant-or-self::div[@itemtype]")

                for menu_item in menu_items:
                    il_menu_item = McDonaldsItemLoader(il.load_item(), selector=menu_item)
                    il_menu_item.add_xpath("title", "descendant-or-self::*[@itemprop='name']/text()")
                    il_menu_item.add_xpath("thumbnail", "descendant-or-self::*[@itemprop='image']/@content")
                    il_menu_item.add_xpath("price", "descendant-or-self::*[@class='bQEAj']/text()")
                    il_menu_item.add_xpath("description",
                                           "descendant-or-self::*[@class='_2aOqz _1d7fc']/text()")
                    if il_menu_item.get_xpath("descendant-or-self::*[contains(@class, '_3x58u')]"):
                        il_menu_item.add_value("veg", True)
                    else:
                        il_menu_item.add_value("veg", False)

                    if il_menu_item.get_xpath("descendant-or-self::*[contains(@class, '_22D_E')]"):
                        il_menu_item.add_xpath("promotion",
                                               "descendant-or-self::*[contains(@class, '_22D_E')]/text()")
                    else:
                        il_menu_item.add_value("promotion", "None")

                    yield il_menu_item.load_item()

    def mcd_sub_category(self, item, sub_categories):
        for sub_category in sub_categories:
            il = McDonaldsItemLoader(item=item, selector=sub_category)
            il.add_xpath("subcategory", "h3/text()")

            yield il.load_item()
