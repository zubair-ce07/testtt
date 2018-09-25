import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveSanMarcos(BaseMixinPPE):
    name = property_slug = 'grove-at-san-marcos'
    allowed_domains = [
        'groveatsanmarcos.prospectportal.com',
        'groveatsanmarcos.com'
    ]

    login_domain = 'https://groveatsanmarcos.prospectportal.com/'
    site_domain = 'http://groveatsanmarcos.com/'

    property_name = 'Grove at San Marcos'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveSanMarcos(PPBaseParseSpiderE, MixinGroveSanMarcos):
    name = MixinGroveSanMarcos.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name[0]


class CrawlSpiderGroveSanMarcos(MixinGroveSanMarcos, PPBaseCrawlSpiderE):
    name = MixinGroveSanMarcos.name + '-crawl'
    parse_spider = ParseSpiderGroveSanMarcos()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
