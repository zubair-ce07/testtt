import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinTroy(BaseMixinPPE):
    name = property_slug = 'pointe-at-troy'
    allowed_domains = [
        'pointetroy.prospectportal.com',
        'pointetroy.com'
    ]

    login_domain = 'https://pointetroy.prospectportal.com/'
    site_domain = 'http://pointetroy.com/'

    property_name = 'Pointe at Troy'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderTroy(PPBaseParseSpiderE, MixinTroy):
    name = MixinTroy.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '|')
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderTroy(MixinTroy, PPBaseCrawlSpiderE):
    name = MixinTroy.name + '-crawl'
    parse_spider = ParseSpiderTroy()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
