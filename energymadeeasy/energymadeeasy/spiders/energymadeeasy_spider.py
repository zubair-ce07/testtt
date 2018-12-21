# -*- coding: utf-8 -*-
import csv
import datetime
import json
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.shell import inspect_response

import logging

from ..items import EnergymadeeasyItem


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    @staticmethod
    def fetch_numerical(value):
        if value:
            r = re.findall(r'\d*\.?\d+', value[0])

            if r:
                return r[0]

    solar_meter_fee_in = fetch_numerical
    supply_in = fetch_numerical
    peak_rate_in = fetch_numerical
    block_type_in = fetch_numerical
    peak_step_1_in = fetch_numerical
    peak_rate_2_in = fetch_numerical
    peak_step_2_in = fetch_numerical
    peak_rate_3_in = fetch_numerical
    peak_step_3_in = fetch_numerical
    peak_rate_4_in = fetch_numerical
    off_peak_rate_in = fetch_numerical
    shoulder_in = fetch_numerical
    minimum_monthly_demand_charged_in = fetch_numerical
    fit_in = fetch_numerical
    guaranteed_discount_off_usage_in = fetch_numerical
    guaranteed_discount_off_bill_in = fetch_numerical
    pot_discount_off_usage_in = fetch_numerical
    pot_discount_off_bill_in = fetch_numerical
    dd_discount_off_bill_in = fetch_numerical
    dd_discount_off_usage_in = fetch_numerical
    e_bill_discount_off_bill_in = fetch_numerical
    e_bill_discount_off_usage_in = fetch_numerical
    online_signup_discount_off_bill_in = fetch_numerical
    online_signup_discount_off_usage_in = fetch_numerical
    dual_fuel_discount_off_bill_in = fetch_numerical
    dual_fuel_discount_off_usage_in = fetch_numerical
    contract_length_in = fetch_numerical
    approx_incentive_value_in = fetch_numerical
    single_rate_in = fetch_numerical
    controlled_load_1_in = fetch_numerical
    controlled_load_2_in = fetch_numerical
    demand_usage_rate_in = fetch_numerical

    raw_discount_and_incentives_out = Identity()
    raw_restrictions_out = Identity()
    raw_usage_rates_out = Identity()
    raw_controlled_loads_out = Identity()


class EnergymadeeasySpiderElectricity(scrapy.Spider):
    name = 'energymadeeasy_e'
    allowed_domains = ['energymadeeasy.gov.au']
    start_urls = ['https://www.energymadeeasy.gov.au/']
    filename = 'electricity.csv'

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'COOKIES_ENABLED': False,
        'HTTPCACHE_ENABLED': True
    }

    def start_requests(self):
        customer_type = 'S'
        pool = 'N'
        gas_heater = 'N'

        with open(self.filename) as f:
            reader = csv.DictReader(f)
            readings = list(reader)

        for reading in readings:
            if reading['type'] == 'E':
                url = 'https://www.energymadeeasy.gov.au/results.html?' \
                    'postcode={}&fuelType={}&customerType={}&pool={}'.format(
                        reading['zipcode'], reading['type'], customer_type, pool)
            elif reading['type'] == 'G':
                url = 'https://www.energymadeeasy.gov.au/results.html?' \
                    'postcode={}&fuelType={}&customerType={}&gasHeater={}'.format(
                        reading['zipcode'], reading['type'], customer_type, gas_heater)
            else:
                url = 'https://www.energymadeeasy.gov.au/results.html?' \
                    'postcode={}&fuelType={}&customerType={}&pool={}' \
                    '&gasHeater={}'.format(reading['zipcode'], reading['type'], customer_type, pool,
                                           gas_heater)

            request = scrapy.Request(url, callback=self.parse)
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
            request = response.follow(url, callback=self.parse_product)
            request.meta['type'] = response.meta['type']
            yield request

    def parse_product(self, response):
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

        loader.add_value('energy_plan', response.meta['type'])
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
        loader.add_xpath('fit', '//*[@id="pricing"]//*[@class="icon-aer-solar-feed"]//'
                                'following::div[contains(@class, "panel__list")][1]//'
                                'strong/text()')
        loader.add_xpath('minimum_monthly_demand_charged',
                         '//*[@id="pricing"]//*[contains(text(), "Demand charges")]/'
                         '../..//*[contains(text(), "minimum demand")]/text()')
        loader.add_xpath('demand_usage_rate', '//*[@id="pricing"]//*[contains(text(), '
                                              '"Demand usage rate")]/../../td[contains(text(),'
                                              ' "cents")]/text()')

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
            rates = []
            for rate_tables in response.css('[id^="pricing"] .panel__item--chartular'):
                raw_usage_rates = []
                raw_rates = rate_tables.css('.panel__item--chartular th')
                title = rate_tables.css('.panel__item--chartular '
                                        '.panel__chart-title strong::text').extract_first()
                for raw_rate in raw_rates:
                    raw_text = raw_rate.css('th::text').extract()
                    rate = raw_rate.css('strong::text').extract_first()
                    raw_usage_rates.append({
                        'name': raw_text[0],
                        'rates': [{'price': rate + raw_text[-1]}]
                    })

                rates.append({title: {'blocks': raw_usage_rates}})

            fields = self.calculate_single_rates(rates)

            if fields:
                for f in fields.keys():
                    loader.add_value(f, fields[f])

            loader.add_value('raw_usage_rates', rates)

        raw_discounts = []

        for discount in response.xpath('//*[text()="Discounts"]//../../section//li'):
            raw_discounts.append({
                'name': discount.css('.panel__list-item::text').extract_first(),
                'description': discount.css('.panel__list-subtext::text').extract_first(),
                'description_values': discount.css('.panel__list-subtext::text').re(r'\d+\.?\d*%?'),
                'value': discount.css('.panel__list-value::text').extract_first(),
            })

        loader.add_css('block_type',
                       '[id^="pricing"] .panel__item--chartular .panel__subnote strong::text')

        discounts = self.fetch_discounts(raw_discounts)

        for d in discounts.keys():
            loader.add_value(d, discounts[d])

        loader.add_value('raw_discount_and_incentives', raw_discounts)
        controlled_loads = self.fetch_controlled_loads(response)
        load_flag = True
        loader.add_value('raw_controlled_loads', controlled_loads)
        item = loader.load_item()

        # yield {response.url: controlled_loads}

        for load in controlled_loads:
            # print(load)
            if not load['name']:
                continue

            if re.findall(r'Controlled Load\s*1', load['name'], re.IGNORECASE) or \
                    re.findall(r'Tariff\s*31', item['name'], re.IGNORECASE) or \
                    re.findall(r'Controlled Load\s*1', item['name'], re.IGNORECASE) or \
                    re.findall(r'CL\s*1', item['name'], re.IGNORECASE):
                load_item = item.copy()
                load_item['controlled_load_1'] = load['rate']
                load_flag = False
                yield load_item

            if re.findall(r'Controlled Load\s*2', load['name'], re.IGNORECASE) or \
                    re.findall(r'Tariff\s*33', item['name'], re.IGNORECASE) or \
                    re.findall(r'Controlled Load\s*2', item['name'], re.IGNORECASE) or \
                    re.findall(r'CL\s*2', item['name'], re.IGNORECASE):
                load_item = item.copy()
                load_item['controlled_load_2'] = load['rate']
                load_flag = False
                yield load_item

        if load_flag:
            forced_items = self.enforce_controlled_loads(item)

            if not forced_items:
                yield item
            else:
                yield from (i for i in forced_items)

    @staticmethod
    def enforce_controlled_loads(item):
        items = []

        cl1_conditions = ["Tariff 31", "Controlled load 1", "EA010EA030",
                          "BLNN2AUBLNC1AU", "N70N50", "84009000"]

        cl2_conditions = ["Tariff 33", "Controlled load 2", "EA010EA040", "BLNN2AUBLNC2AU",
                          "N70N54", "84009100"]

        for load in item.get('raw_controlled_loads', []):
            for cl1_condition in cl1_conditions:
                if cl1_condition.lower() in json.dumps(load).lower() or \
                        item['db'] == 'SA Power Networks':
                    load_item = item.copy()
                    load_item['controlled_load_1'] = load['rate']
                    items.append(load_item)
                    break

            for cl2_condition in cl2_conditions:
                if cl2_condition.lower() in json.dumps(load).lower():
                    load_item = item.copy()
                    load_item['controlled_load_2'] = load['rate']
                    items.append(load_item)
                    break

        return items

    @staticmethod
    def calculate_single_rates(rates):
        fields = {}
        if len(rates) != 1:
            return

        raw_rates = list(rates[0].values())[0]

        for i, rates in enumerate(raw_rates['blocks']):
            if i == 3:
                fields['peak_rate_{}'.format(
                    i + 1)] = rates['rates'][0]['price']
                break

            if i == 0:
                fields['single_rate'] = rates['rates'][0]['price']
                if len(raw_rates['blocks']) > 1:
                    fields['peak_step_{}'.format(i + 1)] = rates['name']
                continue

            fields['peak_rate_{}'.format(i + 1)] = rates['rates'][0]['price']

            if i + 1 != len(raw_rates['blocks']):
                fields['peak_step_{}'.format(i + 1)] = rates['name']

        return fields

    def fetch_controlled_loads(self, response):
        controlled_loads = []
        raw_controlled_loads = []

        headers = []
        raw_table = response.xpath('//*[@class="flex-primary"]//*[contains(text(), '
                                   '"Controlled load charges")]//following::table[1]')

        if raw_table:
            for i, header in enumerate(raw_table.css('table > tr td')):
                headers.append(header.css(
                    'td strong::text').extract_first() or i)

            for row in raw_table.css('tbody tr'):
                row_data = []
                for column in row.css('td'):
                    row_data.append(self.clean(
                        ''.join(column.css(' ::text').extract())))

                raw_controlled_loads.append(dict(zip(headers, row_data)))

        # print(raw_controlled_loads)
        # print(response.url)

        for load in raw_controlled_loads:
            if load.get('Controlled load usage'):
                # if not self.fetch_load_name(load):
                #     print(load)
                #     inspect_response(response, self)

                name, step = self.fetch_load_name(load)

                controlled_loads.append({
                    'name': name,
                    'rate': load['Controlled load usage'],
                    'step': step
                })

        # print(controlled_loads)

        # if response.url == 'https://www.energymadeeasy.gov.au/offer/575437?postcode=2600':
        #     inspect_response(response, self)

        return controlled_loads

    @staticmethod
    def fetch_load_name(load):
        name_key = None
        name = None
        step = None

        for key in load.keys():
            load[key] = re.sub(r'two', '2', load[key], flags=re.IGNORECASE)
            load[key] = re.sub(r'one', '1', load[key], flags=re.IGNORECASE)
            name_find = re.findall(r'Controlled Load\s*\d', load[key], re.IGNORECASE)
            if name_find:
                name_key = key
                name = name_find[0]
                break

        load_copy = load.copy()

        if name_key is not None:
            del load_copy[name_key]

        if load_copy.get('Daily supply charge'):
            del load_copy['Daily supply charge']

        del load_copy['Controlled load usage']

        for v in load_copy.values():
            if not v.strip():
                continue

            if not step:
                step = ''

            step = '{} {}'.format(step, v).strip()

        return name, step

    @staticmethod
    def clean(value):
        return re.sub(r'\s+', ' ', value).strip()

    @staticmethod
    def fetch_discounts(raw_discounts):
        discounts = {}

        for raw_discount in raw_discounts:
            if not raw_discount['name']:
                continue

            name = raw_discount['name'].lower()
            value = raw_discount['value']

            if not value and raw_discount['description_values']:
                value = raw_discount['description_values'][0]

            if 'guaranteed discount' in name:
                if 'usage' in name:
                    discounts['guaranteed_discount_off_usage'] = value
                elif 'bill' in name:
                    discounts['guaranteed_discount_off_bill'] = value
            elif 'pay on time' in name:
                if 'usage' in name:
                    discounts['pot_discount_off_usage'] = value
                elif 'bill' in name:
                    discounts['pot_discount_off_bill'] = value
            elif 'direct debit' in name:
                if 'usage' in name:
                    discounts['dd_discount_off_usage'] = value
                elif 'bill' in name:
                    discounts['dd_discount_off_bill'] = value
            elif re.findall(r'e.?bill', name):
                if 'usage' in name:
                    discounts['e_bill_discount_off_usage'] = value
                elif 'bill' in name:
                    discounts['e_bill_discount_off_bill'] = value
            elif 'dual' in name or 'bundling' in name:
                if 'usage' in name:
                    discounts['dual_fuel_discount_off_usage'] = value
                elif 'bill' in name:
                    discounts['dual_fuel_discount_off_bill'] = value
            elif 'online' in name:
                if 'usage' in name:
                    discounts['online_signup_discount_off_usage'] = value
                elif 'bill' in name:
                    discounts['online_signup_discount_off_bill'] = value

        return discounts


class EnergymadeeasySpiderGas(EnergymadeeasySpiderElectricity):
    name = 'energymadeeasy_g'
    filename = 'gas.csv'


class EnergymadeeasySpiderDual(EnergymadeeasySpiderElectricity):
    name = 'energymadeeasy_d'
    filename = 'dual.csv'
