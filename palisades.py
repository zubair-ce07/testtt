import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinPalisades(BaseMixinPPE):
    name = property_slug = 'palisades-at-jaguar-city'
    allowed_domains = [
        'palisadesatjaguarcityapartments.prospectportal.com',
        'palisades-subr.com'
    ]

    login_domain = 'https://palisadesatjaguarcityapartments.prospectportal.com/'
    site_domain = 'http://palisades-subr.com/'

    property_name = 'Palisades at Jaguar City'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderPalisades(PPBaseParseSpiderE, MixinPalisades):
    name = MixinPalisades.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderPalisades(MixinPalisades, PPBaseCrawlSpiderE):
    name = MixinPalisades.name + '-crawl'
    parse_spider = ParseSpiderPalisades()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
