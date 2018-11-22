# -*- coding: utf-8 -*-
import scrapy
from logging import warning
import json
import csv
# import termcolor
import datetime
import re

from ..items import EnergymadeeasyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.shell import inspect_response

global_arr = set()


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()


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
                url, callback=self.parse_results)
            request.meta['type'] = reading['type']
            request.meta['zipcode'] = reading['zipcode']
            yield request

    def parse_results(self, response):
        raw_results = response.xpath(
            '//script[contains(text(), "Drupal")]').re_first(r'{.+}')
        raw_results = json.loads(raw_results)

        for result in raw_results['acccResultsData'][response.meta['type']]:
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
            'db', '//*[@id="additional"]//*[contains(text(), "Distributor")]/../following::p[1]/text()')
        loader.add_xpath(
            'supply', '//*[contains(text(), "Daily supply charge")]/strong/text()', re=r'[\d\.]+')
        loader.add_xpath(
            'contract_length', '//*[@id="additional"]//*[contains(text(), "Contract Length")]/../following::p[1]/text()')
        loader.add_xpath(
            'solar_meter_fee', '//*[@id="pricing"]//*[@class="icon-aer-solar-feed"]//following::div[contains(@class, "panel__list")][1]//strong/text()')
        loader.add_xpath(
            'guaranteed_discount_off_usage', '//*[contains(text(), "Guaranteed discount on total usage")]/following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath(
            'guaranteed_discount_off_bill', '//*[contains(text(), "Guaranteed discount on total bill")]/following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('pot_discount_off_usage',
                         '//*[contains(text(), "Pay on time discount on total usage")]/following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('pot_discount_off_bill',
                         '//*[contains(text(), "Pay on time discount on total bill")]/following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('dd_discount_off_usage',
                         '//*[contains(text(), "Direct debit discount on total usage")]/following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('dd_discount_off_bill',
                         '//*[contains(text(), "Direct debit discount on total bill")]/following::div[@class="panel__list-value"][1]/text()', re=r'[\d\.]+')
        loader.add_xpath('minimum_monthly_demand_charged',
                         '//*[@id="pricing"]//*[contains(text(), "Demand charges")]/../..//*[contains(text(), "minimum demand")]/text()')

        bill_c_incentive = response.xpath(
            '//*[contains(text(), "Incentives")]/following::div[@class="panel__list-item"][contains(text(), "Bill Credit")][1]').re_first(r'[\d\.]+')

        if bill_c_incentive:
            loader.add_value('incentive_type', 'Bill Credit')
            loader.add_value('approx_incentive_value', bill_c_incentive)

        other_incentive = response.xpath(
            '//*[text()="Incentives"]/following::section[1]//li/div[@class="panel__list-item"]/text()').extract_first()

        if other_incentive:
            loader.add_value('incentive_type', 'Other')
            loader.add_value('approx_incentive_value', other_incentive)

        if response.xpath('//*[text()="Plan eligibility"]//../../section//li/div[@class="panel__list-item"][text()="You have solar panels"]'):
            loader.add_value('restricted_eligibility', 'so')
        else:
            loader.add_value('restricted_eligibility', 'n')
        # elif response.xpath('//*[text()="Plan eligibility"]//../../section//li/div[@class="panel__list-item"][text()="You have solar panels"]'):
        #     loader.add_value('restricted_eligibility', 'nso')

        # termcolor.cprint(json.dumps(
        #     dict(loader.load_item()), indent=2), color='yellow')

        flag = False
        discounts = response.xpath(
            '//*[text()="Discounts"]//../../section//li/div[@class="panel__list-item"]/text()').extract()
        restrictions = response.xpath(
            '//*[text()="Plan eligibility"]//../../section//li/div[@class="panel__list-item"]/text()').extract()

        old_disc = [
            'Guaranteed discount on total usage',
            'Pay on time discount on total usage',
            'Pay on time discount on total bill',
            'Guaranteed discount on total bill',
            'Direct debit discount on total usage',
            'Direct debit discount on total bill'
            # 'Bonus annual Velocity points',
            # 'Bonus sign-up Velocity points',
            # 'Direct debit discount',
            # 'Bill Credit',
            # 'Other discounts apply',
            # 'Double Up',
            # 'Amazon Echo',
            # 'Gift Card',
            # 'Online Credit',
            # 'Movies Plus Rewards',
            # 'AFL FREE Kick',
            # 'Promotional Offers',
            # 'Shopping Program',
            # 'One Free Move'
        ]

        old_resc = [
            'You have solar panels',
            'You purchase eligible solar PV system from Origin',
            'You do not receive a solar feed in tariff',
            'E-billing and correspondence',
            'Direct Debit and eBilling only'
        ]

        # for d in [disc for disc in discounts if not any(x for x in old_disc if x in disc)]:
        #     if 'on total usage' in d or 'on total till' in d:
        #         termcolor.cprint(d, color='red')
        #         flag = True

        # for r in restrictions:
        #     global_arr.add(r)

        # for d in discounts:
        #     global_arr.add(d)

        # for r in [resc for resc in restrictions if 'solar' in resc or 'dual' in resc or 'both' in resc or 'and' in resc]:
        #     if r in old_resc:
        #         continue

        #     termcolor.cprint(r, color='blue')
        #     flag = True

        # for r in [resc for resc in restrictions if 'solar' in resc or 'dual' in resc or 'both' in resc or 'and' in resc]:
        #     if r in old_resc:
        #         continue

        #     termcolor.cprint(r, color='blue')
        #     flag = True

        # if flag:
        #     self.analyze(response, 'discounts')
        #     self.analyze(response, 'eligibility')

        # self.analyze_multi(response, '#pricing *::text',
        #                    ['dual'])
        # self.analyze(response, 'dual')

        # for g in global_arr:
        #     termcolor.cprint(g, color='red')

        return loader.load_item()

    # def analyze_multi(self, response, target, value):
    #     source = ''.join(response.css(target).extract())
    #     if all(v.lower() in source.lower() for v in value):
    #         termcolor.cprint(value, color='magenta')
    #         inspect_response(response, self)

    # def analyze(self, response, value):
    #     if value.lower() in response.text.lower():
    #         termcolor.cprint(value, color='magenta')
    #         inspect_response(response, self)

    # def analyze_re(self, response, value):
    #     if re.findall(value, response.text):
    #         termcolor.cprint(value, color='magenta')
    #         inspect_response(response, self)

    # def analyze_sensitive(self, response, value):
    #     if value in response.text:
    #         termcolor.cprint(value, color='magenta')
    #         inspect_response(response, self)

    # def analyze_css(self, response, value):
    #     if not response.css(value):
    #         termcolor.cprint(value, color='magenta')
    #         inspect_response(response, self)
