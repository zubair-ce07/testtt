import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinPointe(BaseMixinPPE):
    name = property_slug = 'pointe-at-san-marcos'
    allowed_domains = [
        'pointesanmarcos.prospectportal.com',
        'pointesanmarcos.com'
    ]

    login_domain = 'https://pointesanmarcos.prospectportal.com/'
    site_domain = 'http://pointesanmarcos.com/'

    property_name = 'Pointe at San Marcos'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderPointe(PPBaseParseSpiderE, MixinPointe):
    name = MixinPointe.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))[0]
        if "0 Bedroom" in room_name:
            return f"Studio-{name}"
        return f"{room_name}-{name}"


class CrawlSpiderPointe(MixinPointe, PPBaseCrawlSpiderE):
    name = MixinPointe.name + '-crawl'
    parse_spider = ParseSpiderPointe()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
