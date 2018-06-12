import json
import re

from scrapy import Spider, Request


class CommunityosSpider(Spider):
    name = "commmunityos"
    start_urls = ['https://211-idaho.communityos.org/']
    body = 'site%5Csite_addressus%5Csite_addressus=%7B%7D&service%5Cservice_geotagus%5Cservice_geotagus=%7B%22' \
           'operator%22%3A%5B%22serves_array%22%5D%7D&service%5Cservice_system%5Cawtsv_keyword=%7B%22operator%' \
           '22%3A%5B%22fulltext%22%5D%7D&service%5Cservice_taxonomy%5Cmodule_servicepost=%7B%22value%22%3A%5B%' \
           '7B%22taxonomy_id%22%3A{0}%2C%22__react_key%22%3A%22ta_id_{1}-INTERM_PROP_taxonomy_link_id%22%7D%5D' \
           '%2C%22operator%22%3A%5B%22contains_array%22%5D%7D&service%5Cservice_option%5Cstatus=%7B%22min%22%3A' \
           '%5B77%5D%2C%22max%22%3A%5B77%5D%2C%22value%22%3A%5B77%5D%2C%22operator%22%3A%5B%22contains_array%22%' \
           '5D%7D&service%5Cservice_site%5Cservice_site=%7B%22operator%22%3A%5B%22contains_array%22%5D%7D&revision' \
           '%5Brevision%5D%5Bid%5D=&revision%5Brevision%5D%5Brecord_name%5D=agency&revision%5Brevision%5D%5Btoken%5D='
            # NOQA

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    record_url = (
        'https://211-idaho.communityos.org/apssreadonly'
        '/render/id/%s/form/site/record_id/%s'
    )

    def parse(self, response):
        ids = re.findall(
            r'taxonomy_id%22%3A(.*?)%7D', response.body_as_unicode()
        )
        ids = set(ids)
        for _id in ids:
            yield Request(
                'https://211-idaho.communityos.org/guided_search/results/',
                method='POST',
                body=self.body.format(_id, _id),
                headers=self.headers,
                callback=self.parse_agencies,
            )

    def parse_agencies(self, response):
        data = json.loads(response.body)
        for d in data['data']:
            yield Request(
                self.record_url % (d['sc_735'], d['sc_717_ids'][0]),
                callback=self.parse_agency_detail
            )

    def parse_agency_detail(self, response):
        data = response.xpath('//script[@id="initial-state"]/text()')
        data = json.loads(data.extract_first().strip())['data']

        service_system = data.get('entryset', {}).get('service', {}).get('service_system')
        service_geotagus = data.get('entryset', {}).get('service', {}).get('service_geotagus', {})
        service_option = data.get('entryset', {}).get('service', {}).get('service_option', {})

        if not service_system:
            service_system = data.get('entryset', {}).get('site', {}).get('site_system')

        item = {}
        item['url'] = response.url
        item['name'] = service_system.get('name')
        item['aka'] = service_system.get('aka')
        item['description'] = self._clean(service_system.get('description'))
        item['website'] = service_system.get('website_url_text', '')
        item['phone'] = service_system.get('main_phone_import') or service_system.get('site_phone_import')
        item['tdd_phone'] = service_system.get('tdd_phone_import')
        item['other_phone'] = service_system.get('other_phone_importtext')
        item['alternate_phone'] = service_system.get('alternate_phone_importtext')
        item['email'] = service_system.get('email_address', '')
        item['fax'] = service_system.get('fax_import', '') or service_system.get('site_fax_import', '')
        item['eligibility'] = service_system.get('eligibility_import', '')
        item['application_intake_process'] = service_system.get('applicationintake_process', '')
        item['hours_notes'] = self._clean(service_system.get('hours_notes_import'))
        item['languages_spoken'] = service_system.get('languages_spoken')

        if service_option.get('location_label'):
            item['location'] = " | ".join(service_option.get('location_label'))
            item['fee_amount'] = " | ".join(service_option.get('fee_amounts_import'))

        addressus = data['entryset']['site']['site_addressus']
        if addressus:
            address = addressus['site_addressus']
            address = "{} {} {} {}".format(
                address.get('address_1') or '',
                address.get('address_2') or '',
                '%s, %s' % (address.get('city', ''),
                            address.get('state', '')),
                address.get('zip', '')
            )
        else:
            address = ''
        item['street_physical_address'] = address

        geo_stats = self.extract_geostats(service_geotagus.get('service_geotagus'))
        if geo_stats:
            item['geo_stats'] = " | ".join(self.extract_geostats(service_geotagus.get('service_geotagus')))
        else:
            item['geo_stats'] = service_system.get('geographic_area_import')

        yield item

    def extract_geostats(self, raw_geostats):
        geostats = []
        if raw_geostats:
            for raw_geostat in raw_geostats:
                geostats.append("{0}, {1} {2}".format(raw_geostat.get('county'), raw_geostat.get('state_label'),
                                                      "County"))
            return geostats
        return geostats

    def _clean(self, value):
        return value.replace('\n', '')