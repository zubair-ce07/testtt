# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from mutualartproject.items import BaseItem, BaseItemLoader


class MutualartSpider(scrapy.Spider):
    name = "mutualart"
    allowed_domains = ["mutualart.com"]
    start_urls = ["https://www.mutualart.com/"]

    def parse(self, response):
        url = "https://www.mutualart.com/Ajax/LogIn/UserControlLogin"
        payload = '''mail=muhammad.haseeb%40arbisoft.com&txtUserPassword=root%3Apanic5&backwardPath='''
        data_headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cache-Control": "no-cache",
            "X-Requested-With": "XMLHttpRequest"
            }

        yield Request(url=url, callback=self.parse_main_page, method='POST',
                      headers=data_headers,
                      body=payload)

    def parse_main_page(self, response):
        urls = ["https://www.mutualart.com/ArtistsIndex/Category/Asian-Modern---Contemporary/F12F8284994400BD",
                "https://www.mutualart.com/ArtistsIndex/Category/Postwar---Contemporary/054412460E1796B5"]

        for url in urls:
            yield Request(url=url, callback=self.parse_artists_listings)

    def parse_artists_listings(self, response):
        for url in self.get_next_pages(response):
            yield Request(url=url, callback=self.parse_artists_listings)

        artists_urls = self.get_artists_urls(response)

        for url in artists_urls:
            yield Request(url=url, callback=self.parse_artists)

    def parse_artists(self, response):
        common_fields = {
            "artist": response.css("h1.name::text").extract(),
            "biography": response.css("p.bio::text").extract(),
            "artist_image": response.css("div.artist-image-block img::attr(src)").extract()
        }

        yield Request(url=self.get_arts_list(response), callback=self.parse_arts_listings,
                      meta={"common_fields": common_fields})

    def parse_arts_listings(self, response):
        for url in self.get_next_pages(response):
            yield Request(url=url, callback=self.parse_arts_listings, meta={"common_fields": response.meta['common_fields']})

        urls = self.get_art_urls(response)

        for url in urls:
            yield Request(url=url, callback=self.parse_art,
                          meta={"common_fields": response.meta['common_fields']})

    def parse_art(self, response):
        l = BaseItemLoader(item=BaseItem(), response=response)

        for key in response.meta['common_fields'].keys():
            l.add_value(key, response.meta['common_fields'][key])

        l.add_css("title", "h1.v2__artwork-detail__title ::text")
        l.add_css("size", "div.v2__artwork-detail__section p::text")
        l.add_css("type", "div.v2__artwork-detail__section p span::text")
        l.add_css("image_urls", "div.v2__artwork-detail__img-block img::attr(src)")
        return l.load_item()

    def get_artists_urls(self, response):
        urls = response.css(".img-block::attr(href)").extract()
        return [response.urljoin(url) for url in urls]

    def get_arts_list(self, response):
        return "{}/Artworks".format(response.url)

    def get_art_urls(self, response):
        urls = response.css("div.grid-item a::attr(href)").extract()
        return [response.urljoin(url) for url in urls]

    def get_next_pages(self, response):
        urls = response.css("ul.pagination li a::attr(href)").extract()
        return [response.urljoin(url) for url in urls]
