import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCambridge(BaseMixinPPE):
    name = property_slug = 'cambridge-at-college-station'
    allowed_domains = [
        'cambridgeatcollegestation.prospectportal.com',
        'cambridgeatcollegestation.com'
    ]

    login_domain = 'https://cambridgeatcollegestation.prospectportal.com/'
    site_domain = 'http://www.cambridgeatcollegestation.com/'

    property_name = 'Cambridge at College Station'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCambridge(PPBaseParseSpiderE, MixinCambridge):
    name = MixinCambridge.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_types = clean(sel.css('.type-col ::text'))
        name = clean(c_sel.css('.title ::text'))
        if re.search('(Bedroom)|(\d+x\d+)', name[0]):
            room_name = clean(c_sel.css('.sub-title ::text'))
            room_name = room_name[0].replace('/', '')
            return self.format_name(room_name, room_types, ' ')

        return self.format_name(name[0], room_types, ' - ')

    def format_name(self, name, r_types, sep):
        if set(r_types) & {'Single', 'Double', 'Tripple'}:
            return f'{name}{sep}{r_types[0]} Occupancy'
        return name


class CrawlSpiderCambridge(MixinCambridge, PPBaseCrawlSpiderE):
    name = MixinCambridge.name + '-crawl'
    parse_spider = ParseSpiderCambridge()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
