from json import loads

from scrapy import Spider, Request
from w3lib.url import add_or_replace_parameter

from ..items import BannerItemLoader
from swiggy.spiders.location_reader import read, test_locations


class SwiggyBannerSpider(Spider):
    name = 'swiggy-banner'
    allowed_domains = ['www.swiggy.com']

    restaurent_base_url = "https://www.swiggy.com"
    thumbnail_url = "https://res.cloudinary.com/swiggy/image/upload/" \
                    "fl_lossy,f_auto,q_auto,w_165,h_165,c_fill/{}"
    banner_base_url = "https://www.swiggy.com/dapi/restaurants/list/v5"
    autocomplete_base_url = "https://www.swiggy.com/dapi/misc/places-autocomplete"
    geocode_base_url = "https://www.swiggy.com/dapi/misc/reverse-geocode"

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "DOWNLOAD_DELAY": 0.5
    }

    def start_requests(self):
        locations = test_locations

        requests = []
        for loc in locations:
            url = add_or_replace_parameter(self.autocomplete_base_url, "input", loc.postal_code.replace(" ", ""))
            requests.append(Request(url=url, callback=self.place_search,
                                    meta={"postal_code": loc.postal_code, "locality": loc.locality,
                                          "city": loc.city}))

        return requests

    def place_search(self, response):
        search_results = loads(response.text)["data"]
        for location in search_results:
            url = add_or_replace_parameter(self.geocode_base_url, "place_id", location["place_id"])
            yield Request(url=url, callback=self.geocode_search, meta=response.meta)

    def geocode_search(self, response):
        geocodes = loads(response.text)["data"]
        for geocode in geocodes:
            location = geocode["geometry"]["location"]
            url = add_or_replace_parameter(self.banner_base_url, "lat", location["lat"])
            url = add_or_replace_parameter(url, "lng", location["lng"])
            yield Request(url=url, callback=self.parse_banner, meta=response.meta)

    def parse_banner(self, response):
        raw_cards = loads(response.text)["data"]["cards"]
        city_url = response.xpath('//text()').re_first('"city":"(\w+)"')
        banner_url = "{}/{}/restaurants".format(self.restaurent_base_url, city_url)
        banner_il = BannerItemLoader(response=response)
        banner_il.add_value("pincode", response.meta["postal_code"])
        banner_il.add_value("url", banner_url)
        banner_il.add_value("city", response.meta["city"])
        return self.process_cards(raw_cards, banner_il.load_item())

    def process_cards(self, raw_cards, banner_item):
        for card in raw_cards:

            if not card["data"]["subtype"] == "topCarousel":
                continue

            for rank, banner_card in enumerate(card["data"]["data"]["cards"]):
                banner_il = BannerItemLoader(item=banner_item.copy())
                banner_il.add_value("rank", rank+1)
                banner_il.add_value("thumbnail", self.thumbnail_url.format(banner_card["data"]["creativeId"]))

                if banner_card["data"]["type"] == "restaurant":
                    redirect_url = "{}/{}/{}".format(self.restaurent_base_url,
                                                     banner_card["data"]["restaurantSlug"]["city"],
                                                     banner_card["data"]["restaurantSlug"]["restaurant"])
                    banner_il.add_value("redirect_url", redirect_url)
                    banner_il.add_value("restaurant_field", banner_card["data"]["restaurantSlug"]["restaurant"])

                elif banner_card["data"]["type"] == "collection":
                    redirect_url = "{}/collections/{}".format(self.restaurent_base_url, banner_card["data"]["link"])
                    banner_il.add_value("redirect_url", redirect_url)
                elif banner_card["data"]["type"] == "static":
                    redirect_url = "https://www.swiggy.com/pop/listing"
                    banner_il.add_value("redirect_url", redirect_url)

                yield banner_il.load_item()
