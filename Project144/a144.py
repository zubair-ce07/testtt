# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from project144.items import Item, ItemLoader


class A144Spider(scrapy.Spider):
    name = '144'
    allowed_domains = ['144.at']
    start_urls = ['https://www.144.at/defi/']

    def parse(self, response):
        params = "load_defi=load_defi&handynummer=0&permission=0"
        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Cache-Control': "no-cache"
        }
        url = "https://www.144.at/defi/config.php"
        yield Request(url=url, callback=self.parse_modals,
                      method='POST', headers=headers,
                      body=params)

    def parse_modals(self, response):
        item_ids = self.get_item_ids(response)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'text/html, */*; q=0.01',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
        }
        url = "https://www.144.at/defi/config.php"

        for item_id in item_ids:
            params = '''load_marker=load_marker&id={}&handynummer=0&permission=0'''.format(item_id)
            yield Request(url=url, callback=self.parse_item,
                          method='POST', headers=headers,
                          body=params, dont_filter=True)

    def parse_item(sefl, response):
        l = ItemLoader(item=Item(), response=response)
        l.add_css('Type', 'h4::text')
        l.add_css('zip_code', '#table_out th::text')
        l.add_css('address', '#table_out th::text')
        l.add_css('Zugangszeiten', '#table_out td::text')
        l.add_css('Wegbeschreibung', '#table_out td::text')
        l.add_css('Wo_genau_ist_der_Defi_angebracht', '#table_out td::text')
        l.add_css('Erreichbarkeit_von_der_Straße', '#table_out td::text')
        return l.load_item()

    def get_item_ids(self, response):
        modals_data = json.loads(response.text)
        return [modal.get('id') for modal in modals_data]
