# -*- coding: utf-8 -*-
import scrapy
from logging import warning
import json
import csv
# import termcolor
import datetime

from ..items import EnergymadeeasyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.shell import inspect_response


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()


class EnergymadeeasySpiderSpider(scrapy.Spider):
    name = 'energymadeeasy_spider'
    allowed_domains = ['energymadeeasy.gov.au']
    start_urls = ['https://www.energymadeeasy.gov.au/']

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_ENABLED': False
    }

    def start_requests(self):
        fuel_type = 'E'
        customer_type = 'S'
        pool = 'N'

        with open('data.csv') as f:
            reader = csv.DictReader(f)
            readings = list(reader)

        for reading in readings:
            url = 'https://www.energymadeeasy.gov.au/results.html?' \
                  'postcode={}&fuelType={}&customerType={}&pool={}'.format(
                      reading['zipcode'], fuel_type, customer_type, pool)

            request = scrapy.Request(
                url, callback=self.parse_results)
            request.meta['type'] = reading['type']
            request.meta['zipcode'] = reading['zipcode']
            yield request

    def parse_results(self, response):
        raw_results = response.xpath(
            '//script[contains(text(), "Drupal")]').re_first(r'{.+}')
        raw_results = json.loads(raw_results)

        if response.meta['type'] == 'E':
            for result in raw_results['acccResultsData']['E']:
                url = '{}?postcode={}'.format(
                    result['offer']['link'], response.meta['zipcode'])
                yield response.follow(url, callback=self.parse_product)

    def parse_product(self, response):
        raw_product = response.xpath(
            '//script[contains(text(), "Drupal")]').re_first(r'{.+}')
        raw_product = json.loads(raw_product)
        raw_tarrif = json.loads(raw_product.get('acccTouTariff', '{}'))

        loader = ProductLoader(item=EnergymadeeasyItem(), response=response)

        if raw_tarrif.get('seasons'):
            for block in raw_tarrif['seasons'][0]['blocks']:
                if block['name'] == 'Peak':
                    loader.add_value('peak_rate', block['rates'][0]['price'])

                if block['name'] == 'Shoulder':
                    loader.add_value('shoulder', block['rates'][0]['price'])

                if block['name'] == 'Off-Peak':
                    loader.add_value(
                        'off_peak_rate', block['rates'][0]['price'])

        green_panel = response.xpath(
            '//*[@id="pricing"]//*[@class="icon-aer-green-power"]//following::div[contains(@class, "panel__list")][1]')
        if green_panel:
            loader.add_value('green_note', ''.join(green_panel.css(
                'p::text, p strong::text').extract()))

        loader.add_value('source', response.url)
        loader.add_value('timestamp', str(datetime.datetime.utcnow()))
        loader.add_value('green', bool(response.css('.icon-aer-green-power')))
        loader.add_value('solar', bool(response.css('.icon-aer-solar-feed')))
        loader.add_value('etf', not bool(response.xpath(
            '//*[contains(@class, "icon-color-positive")]/..//strong[contains(text(), "exit fee")]')))

        loader.add_css('id', '.plan-id strong::text')
        loader.add_css('retailer', '.bp__provider-details .bp__title::text')
        loader.add_css('name', '.bp__summary-title::text')
        loader.add_css('meter_type', '.icon-aer-tariff + span strong::text')

        loader.add_xpath(
            'effective_from', '//*[@id="additional"]//*[contains(text(), "Effective from")]/../following::p[1]/text()')
        loader.add_xpath(
            'supply', '//*[contains(text(), "Daily supply charge")]/strong/text()', re=r'[\d\.]+')
        loader.add_xpath(
            'contract_length', '//*[@id="additional"]//*[contains(text(), "Contract Length")]/../following::p[1]/text()')
        loader.add_xpath(
            'solar_meter_fee', '//*[@id="pricing"]//*[@class="icon-aer-solar-feed"]//following::div[contains(@class, "panel__list")][1]//strong/text()')
        loader.add_xpath(
            'guaranteed_discount_off_usage', '//*[contains(text(), "Guaranteed discount on total usage")]/following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')

        # termcolor.cprint(json.dumps(
        #     dict(loader.load_item()), indent=2), color='yellow')

        # flag = False
        # for x in response.xpath('//*[text()="Discounts"]//../../section//li'):
        #     termcolor.cprint(
        #         ''.join(x.css('div::text').extract()), color='red')

        #     flag = True

        # if flag:
        #     self.analyze(response, 'discounts')

        return loader.load_item()

    def analyze(self, response, value):
        if value.lower() in response.text.lower():
            inspect_response(response, self)

    def analyze_css(self, response, value):
        if not response.css(value):
            inspect_response(response, self)
