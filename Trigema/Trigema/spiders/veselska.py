# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
from re import findall
from Trigema.items import TrigemaItem
import datetime


class VeselskaSpider(Spider):
    name = 'veselska'
    download_delay = 2.0
    # allowed_domains = ['rezidenceveselska.cz/']
    start_urls = ['https://www.rezidenceveselska.cz/nabidka-bytu/']

    def parse(self, response):
        parking_price = self.get_parking_price(response)
        locality = self.get_locality(response)
        for link in LinkExtractor(allow=(), restrict_css=('div>table a',), ).extract_links(response):
            request = Request(link.url, callback=self.parse_item)
            if parking_price:
                request.meta['parking'] = {
                    'price_including_VAT': float(extract_float_from_str(parking_price))
                }
            if locality:
                request.meta['locality'] = locality
            yield request

    def parse_item(self, response):
        item = TrigemaItem()
        item['finished'] = False
        item['ownership'] = 'private'
        item['energy_class'] = 'B'
        item['project'] = 'Rezidence Veselská'
        item['developer'] = 'Odien Real Estate, a.s.'
        item['type'] = 'flat'
        item_details = self.compile_item_details_dict(response)
        if 'parking' in response.meta:
            item['parking'] = response.meta['parking']
        if 'locality' in response.meta:
            item['locality'] = response.meta['locality']
        item['number'] = self.get_unique_id(response)
        item['local_id'] = self.get_unique_id(response)
        item['orientation'] = self.get_orientation(item_details)
        item['usable_area'] = self.get_usable_area(item_details)
        item['disposition'] = self.get_disposition(item_details)
        item['floor'] = self.get_floor(item_details)
        item['price'] = self.get_price(item_details)
        item['state'] = self.get_status(item_details)
        item['cellar'] = self.get_cellar(item_details)
        item['terrace'] = self.get_terrace(item_details)
        item['building'] = self.get_building(item_details)
        item['timestamp'] = datetime.datetime.now()
        yield item

    def compile_item_details_dict(self, response):
        item_details = dict()
        for row in response.css('table.table tr'):
            row_details = row.css('td')
            if len(row_details) == 2:
                item_details[row_details[0].css('::text').extract_first()] = row_details[1].css('::text').extract_first()
        if response.css('span.stav-volny'):
            item_details[u'Status'] = 'free'
        elif response.css('span.stav-rezervovano'):
            item_details[u'Status'] = 'reserved'
        return item_details

    def get_orientation(self, details):
        parser = {'S': 'N', 'V': 'E', 'J': 'S', 'Z': 'W'}
        if u'Orientace' in details:
            res_str = details[u'Orientace']
            orientation = ''
            for alphabet in res_str:
                orientation += parser.get(alphabet)
            if orientation:
                return orientation

    def get_usable_area(self, details):
        if u'Plocha' in details:
            result = extract_float_from_str(details[u'Plocha'])
            if result:
                return float(result)

    def get_disposition(self, details):
        if u'Dispozice' in details:
            return details[u'Dispozice']

    def get_floor(self, details):
        if u'Podlaží' in details:
            # noinspection PyTypeChecker
            return ''.join(findall(r'([0-9])', details[u'Podlaží']))

    def get_terrace(self, details):
        if u'Balkon/Terasa/Lodžie' in details:
            result = extract_float_from_str(details[u'Balkon/Terasa/Lodžie'])
            if result:
                return [float(result)]

    def get_cellar(self, details):
        if u'Sklep' in details:
            result = extract_float_from_str(details[u'Sklep'])
            if result:
                return {'area': float(result)}

    def get_status(self, details):
        if u'Status' in details:
            return details[u'Status']

    def get_price(self, details):
        if u'Cena vč. DPH' in details:
            return float(extract_float_from_str(details[u'Cena vč. DPH']))

    def get_building(self, details):
        if u'Etapa' in details:
            return details[u'Etapa'].strip('.')

    def get_unique_id(self, response):
        return response.css('title::text').re_first('\d+')

    def get_parking_price(self, response):
        return response.css('div[itemprop="breadcrumb"]+p::text').re_first(r' (\d.*?) K')

    def get_locality(self, response):
        return ' '.join(
            [line.strip() for line in response.css('div.row.paticka_spodek>div:first_child p ::text').extract()])

def extract_float_from_str(input_str):
    return ''.join(findall(r'([0-9.,])', input_str)).replace(',', '.')