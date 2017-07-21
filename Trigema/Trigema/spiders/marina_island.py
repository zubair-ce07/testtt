# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy import Request, FormRequest
from Trigema.items import TrigemaItem
import datetime
import re


class MarinaIslandSpider(Spider):
    name = 'marina-island'
    allowed_domains = ['marinaisland.cz']
    start_urls = [
        'http://www.marinaisland.cz/en/byty',
    ]

    def parse(self, response):
        request = FormRequest('http://www.marinaisland.cz/cs/vyhledavani', dont_filter=True, formdata={
            'stav': "1"}, callback=self.parse_lists)
        request.headers.update({
             'Cookie': 'ci_session={};'.format(re.findall(r'ci_session=(.*?);', response.headers['Set-Cookie'])[0])})
        return request

    def parse_lists(self, response):
        unsold = self.get_unsold_products(response)
        sold = self.get_sold_products(response)
        parking_cellar_price = self.get_parking_price(response)
        if unsold:
            for unsold_prop in unsold:
                url = self.get_url(unsold_prop)
                item = self.compile_common_item_details(unsold_prop, parking_cellar_price, url)
                request = Request(url, callback=self.parse_item)
                request.meta['item'] = item
                yield request
        if sold:
            for sold_item in sold:
                yield self.compile_common_item_details(sold_item, parking_cellar_price, response.url)

    def parse_item(self, response):
        item = response.meta['item']
        item['price'] = self.get_price(response)
        item['room'] = self.get_rooms(response)
        item['floor_area'] = self.get_floor_area(response)
        item['garden'] = self.get_garden_details(response)
        item['orientation'] = self.get_orientation(response)
        yield item

    def compile_common_item_details(self, response, parking_price, url):
        item = TrigemaItem()
        results = response.css('td::text').extract()
        if results:
            item['locality'] = u'Bubenské nábř 17000 Praha 7 Czechia'
            item['gps'] = {"latitude": "50.106281", "longitude": "14.458883"}
            item['finished'] = False
            item['energy_class'] = 'B'
            item['cellar'] = True
            item['ownership'] = 'private'
            item['project'] = 'Marina Island'
            item['developer'] = 'Marina Island inc.'
            item['type'] = 'flat'
            item['number'] = results[1]
            item['local_id'] = results[1]
            item['detail_url'] = url
            item['timestamp'] = datetime.datetime.now()
            item['building'] = results[0]
            item['floor'] = results[2]
            item['disposition'] = results[3]
            item['usable_area'] = self.get_usable_area(results[4])
            item['terrace'] = self.get_terrace(results[5])
            item['storeroom'] = self.get_storeroom(response)
            item['state'] = self.get_state(response)
            item['parking'] = self.get_parking(parking_price)
            return item

    def get_sold_products(self, response):
        return response.css('div.table-responsive tr:not([onclick])')

    def get_unsold_products(self, response):
        return response.css('div.table-responsive tr[onclick]')

    def get_parking_price(self, response):
        parking_cellar_price = response.css('div.byty-paticka.nemobil>div :nth-child(1)::text').re(r'\(od (.*?) K')
        return parking_cellar_price[0].replace(' ', '') if parking_cellar_price else None

    def get_url(self, response):
        return response.css('::attr(onclick)').re(r"'(.*?)'")[0]

    def get_usable_area(self, data):
        data = extract_float_from_str(data)
        if data:
            return float(data)

    def get_terrace(self, data):
        data = extract_float_from_str(data)
        if data:
            return [float(data)]

    def get_state(self, response):
        state_parser = {
            u'Prodáno': 'sold',
            u'Předrezervovaný': 'reserved',
            u'Rezervovaný': 'reserved',
            u'Dostupný': 'free'
        }
        state = response.css('td')[7].css('span::text').extract_first()
        if state in state_parser:
            return state_parser.get(state)

    def get_storeroom(self, response):
        return True if response.css('td')[6].css('.komora_ano') else False

    def get_parking(self, parking_price):
        if parking_price:
            return {'price_excluding_vat': float(parking_price)}

    def get_floor_area(self, response):
        floor_area = extract_float_from_str(response.css('div.sumaradek>div.sumacislo::text').extract()[-1])
        if floor_area:
            return float(floor_area)

    def get_garden_details(self, response):
        for detail in response.css('div.sumaradek'):
            if u'Zahrádka:' in detail.css('div.sumapopis::text').extract_first():
                return {
                    'area': float(extract_float_from_str(detail.css('div.sumacislo::text').extract_first()))
                        }

    def get_rooms(self, response):
        rooms = []
        for room in response.css('div.radek'):
            area = extract_float_from_str(room.css('div.radek-cislo::text').extract_first())
            if area:
                rooms.append({
                    'description': room.css('div.radek-popis::text').extract_first(),
                    'area': float(area)
                })
        return rooms

    def get_price(self, response):
        price = extract_float_from_str(response.css('div.cena-bytu span::text').extract_first())
        if price:
            return float(price)

    def get_orientation(self, response):
        parser = {'S': 'N', 'V': 'E', 'J': 'S', 'Z': 'W'}
        res_str = response.css('span.kompas::text').extract_first().strip()
        orientation = ''
        for alphabet in res_str:
            orientation += parser.get(alphabet)
        if orientation:
            return orientation


def extract_float_from_str(input_str):
    return ''.join(re.findall(r'([0-9.])', input_str))
