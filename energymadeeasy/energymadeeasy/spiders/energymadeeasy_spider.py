# -*- coding: utf-8 -*-
import csv
import datetime
import json

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity

from ..items import EnergymadeeasyItem

global_arr = set()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    raw_discount_and_incentives_out = Identity()
    raw_restrictions_out = Identity()


class EnergymadeeasySpiderSpider(scrapy.Spider):
    name = 'energymadeeasy_spider'
    allowed_domains = ['energymadeeasy.gov.au']
    start_urls = ['https://www.energymadeeasy.gov.au/']

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'COOKIES_ENABLED': False,
        'HTTPCACHE_ENABLED': True
    }

    def start_requests(self):
        customer_type = 'S'
        pool = 'N'
        gas_heater = 'N'

        with open('data.csv') as f:
            reader = csv.DictReader(f)
            readings = list(reader)

        for reading in readings[::-1]:
            if reading['type'] == 'E':
                url = 'https://www.energymadeeasy.gov.au/results.html?' \
                    'postcode={}&fuelType={}&customerType={}&pool={}'.format(
                        reading['zipcode'], reading['type'], customer_type, pool)
            else:
                url = 'https://www.energymadeeasy.gov.au/results.html?' \
                    'postcode={}&fuelType={}&customerType={}&gasHeater={}'.format(
                        reading['zipcode'], reading['type'], customer_type, gas_heater)

            request = scrapy.Request(
                url, callback=self.parse)
            request.meta['type'] = reading['type']
            request.meta['zipcode'] = reading['zipcode']
            yield request

    def parse(self, response):
        raw_results = response.xpath(
            '//script[contains(text(), "Drupal")]').re_first(r'{.+}')
        raw_results = json.loads(raw_results)

        if not raw_results.get('acccResultsData'):
            return

        for result in raw_results['acccResultsData'][response.meta['type']]:
            url = '{}?postcode={}'.format(
                result['offer']['link'], response.meta['zipcode'])
            yield response.follow(url, callback=self.parse_product)

    @staticmethod
    def parse_product(response):
        raw_product = response.xpath(
            '//script[contains(text(), "Drupal")]').re_first(r'{.+}')
        raw_product = json.loads(raw_product)
        raw_tariff = json.loads(raw_product.get('acccTouTariff', '{}'))

        loader = ProductLoader(item=EnergymadeeasyItem(), response=response)

        if raw_tariff.get('seasons'):
            for block in raw_tariff['seasons'][0]['blocks']:
                if block['name'] == 'Peak':
                    loader.add_value('peak_rate', block['rates'][0]['price'])

                if block['name'] == 'Shoulder':
                    loader.add_value('shoulder', block['rates'][0]['price'])

                if block['name'] == 'Off-Peak':
                    loader.add_value(
                        'off_peak_rate', block['rates'][0]['price'])

        green_panel = response.xpath('//*[@id="pricing"]//*[@class="icon-aer-green-power"]'
                                     '//following::div[contains(@class, "panel__list")][1]')
        if green_panel:
            loader.add_value('green_note', ''.join(green_panel.css(
                'p::text, p strong::text').extract()))

        loader.add_value('source', response.url)
        loader.add_value('timestamp', str(datetime.datetime.utcnow()))
        loader.add_value('green', bool(response.css('.icon-aer-green-power')))
        loader.add_value('solar', bool(response.css('.icon-aer-solar-feed')))
        loader.add_value('etf', not bool(
            response.xpath('//*[contains(@class, "icon-color-positive")]/..//'
                           'strong[contains(text(), "exit fee")]')))

        loader.add_css('id', '.plan-id strong::text')
        loader.add_css('retailer', '.bp__provider-details .bp__title::text')
        loader.add_css('name', '.bp__summary-title::text')
        loader.add_css('meter_type', '.icon-aer-tariff + span strong::text')

        loader.add_xpath('effective_from', '//*[@id="additional"]//*[contains(text(), "Effective '
                                           'from")]/../following::p[1]/text()')
        loader.add_xpath('db', '//*[@id="additional"]//*[contains(text(), "Distributor")]'
                               '/../following::p[1]/text()')
        loader.add_xpath('supply', '//*[contains(text(), "Daily supply charge")]/strong/text()',
                         re=r'[\d\.]+')
        loader.add_xpath('contract_length', '//*[@id="additional"]//*[contains(text(), "Contract'
                                            ' Length")]/../following::p[1]/text()')
        loader.add_xpath('solar_meter_fee', '//*[@id="pricing"]//*[@class="icon-aer-solar-feed"]//'
                                            'following::div[contains(@class, "panel__list")][1]//'
                                            'strong/text()')
        loader.add_xpath('guaranteed_discount_off_usage',
                         '//*[contains(text(), "Guaranteed discount on total usage")]/'
                         'following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('guaranteed_discount_off_bill',
                         '//*[contains(text(), "Guaranteed discount on total bill")]/'
                         'following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('pot_discount_off_usage',
                         '//*[contains(text(), "Pay on time discount on total usage")]/'
                         'following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('pot_discount_off_bill',
                         '//*[contains(text(), "Pay on time discount on total bill")]/'
                         'following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('dd_discount_off_usage',
                         '//*[contains(text(), "Direct debit discount on total usage")]/'
                         'following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('dd_discount_off_bill',
                         '//*[contains(text(), "Direct debit discount on total bill")]/'
                         'following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('minimum_monthly_demand_charged',
                         '//*[@id="pricing"]//*[contains(text(), "Demand charges")]/'
                         '../..//*[contains(text(), "minimum demand")]/text()')

        bill_c_incentive = response.xpath(
            '//*[contains(text(), "Incentives")]/following::div[@class="panel__list-item"]'
            '[contains(text(), "Bill Credit")][1]').re_first(r'[\d\.]+')

        if bill_c_incentive:
            loader.add_value('incentive_type', 'Bill Credit')
            loader.add_value('approx_incentive_value', bill_c_incentive)

        other_incentive = response.xpath(
            '//*[text()="Incentives"]/following::section[1]//'
            'li/div[@class="panel__list-item"]/text()').extract_first()

        if other_incentive:
            loader.add_value('incentive_type', 'Other')
            loader.add_value('approx_incentive_value', other_incentive)

        if response.xpath('//*[text()="Plan eligibility"]//../../section//li/'
                          'div[@class="panel__list-item"][text()="You have solar panels"]'):
            loader.add_value('restricted_eligibility', 'so')
        else:
            loader.add_value('restricted_eligibility', 'n')

        restrictions = response.xpath('//*[text()="Plan eligibility"]//../../section//li/'
                                      'div[@class="panel__list-item"]/text()').extract()
        loader.add_value('raw_restrictions', restrictions)

        if raw_tariff:
            loader.add_value('raw_usage_rates', raw_tariff)
        else:
            raw_usage_rates = []
            raw_rates = response.css('#pricing .panel__item--chartular th')
            for raw_rate in raw_rates:
                raw_text = raw_rate.css('th::text').extract()
                rate = raw_rate.css('strong::text').extract_first()
                raw_usage_rates.append({
                    'name': raw_text[0],
                    'rates': [{'price': rate + raw_text[-1]}]
                })

            loader.add_value('raw_usage_rates', {'blocks': raw_usage_rates})

        raw_discounts = []

        for discount in response.xpath('//*[text()="Discounts"]//../../section//li'):
            raw_discounts.append({
                'name': discount.css('.panel__list-item::text').extract_first(),
                'description': discount.css('.panel__list-subtext::text').extract_first(),
                'value': discount.css('.panel__list-value::text').extract_first(),
            })

        loader.add_value('raw_discount_and_incentives', raw_discounts)

        return loader.load_item()
