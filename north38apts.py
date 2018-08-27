import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinNorth38(BaseMixinPPE):
    name = property_slug = 'north-38-apartments'
    allowed_domains = [
        'north38.prospectportal.com',
        'north38apts.com'
    ]

    login_domain = 'https://north38.prospectportal.com/'
    site_domain = 'http://north38apts.com/'

    property_name = 'North 38 Apartments'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderNorth38(PPBaseParseSpiderE, MixinNorth38):
    name = MixinNorth38.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('.*(\d+)x(\d+)\s?.?', '\\1 Bedroom / \\2 Bath', name[0])
        return room_name


class CrawlSpiderNorth38(MixinNorth38, PPBaseCrawlSpiderE):
    name = MixinNorth38.name + '-crawl'
    parse_spider = ParseSpiderNorth38()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
