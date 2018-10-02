# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy import Request
from PokemonProject.items import PokemonItem


class PokemonSpider(scrapy.Spider):
    name = 'pokemon'
    allowed_domains = ['db.pokemongohub.net']
    start_urls = ["https://db.pokemongohub.net"]
    handle_httpstatus_list = [404]

    def parse(self, response):
        data_headers = {
            "accept": "application/json, text/plain, */*"
        }
        for i in range(1, 764):
            yield Request(url=response.urljoin("api/pokemon/{}".format(i)),
                          headers=data_headers, callback=self.parse_pokemon)

    def parse_pokemon(self, response):
        pokemon_item = PokemonItem()
        pokemon_item['pokemon'] = json.loads(response.text)
        pokemon_item['cp_chart'] = self.get_cps(pokemon_item)

        p_id = self.get_pokemon_id(pokemon_item)
        url = "https://db.pokemongohub.net/api/pokemon/{}/sprites".format(p_id)
        yield Request(url=url,
                      callback=self.parse_images, meta={"pokemon_item": pokemon_item})

    def parse_images(self, response):
        pokemon_item = response.meta['pokemon_item']
        if response.status != 404:
            pokemon_item['image_urls'] = self.get_image_urls(response)

        base_url = "https://db.pokemongohub.net/api/moves/with-pokemon/"
        p_id = self.get_pokemon_id(pokemon_item)
        yield Request(url="{}{}".format(base_url, p_id), callback=self.parse_moves,
                      meta={"pokemon_item": pokemon_item})

    def parse_moves(self, response):
        pokemon_item = response.meta['pokemon_item']
        if response.status != 404:
            pokemon_item['moves'] = json.loads(response.text)

        base_url = "https://db.pokemongohub.net/api/pokemon/counters/"
        p_id = self.get_pokemon_id(pokemon_item)
        yield Request(url="{}{}".format(base_url, p_id), callback=self.parse_counters,
                      meta={"pokemon_item": pokemon_item})

    def parse_counters(self, response):
        pokemon_item = response.meta['pokemon_item']
        if response.status != 404:
            pokemon_item['counters'] = json.loads(response.text)

        yield pokemon_item

    def get_cps(self, pokemon_item):
        return pokemon_item['pokemon']['CPs']['perLevel']

    def get_image_urls(self, response):
        images_raw = json.loads(response.text)
        if images_raw:
            base_url = "https://db.pokemongohub.net/images/ingame/normal/"
            return ["{}{}".format(base_url, img['sprite'])for img in images_raw[0]['sprites']]
        return None

    def get_pokemon_id(self, pokemon_item):
        return pokemon_item['pokemon']['id']
