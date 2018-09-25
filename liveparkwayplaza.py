import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinParkway(BaseMixinPPE):
    name = property_slug = 'parkway-plaza'
    allowed_domains = [
        'parkwayplazaapartments.prospectportal.com',
        'liveparkwayplaza.com'
    ]

    login_domain = 'https://parkwayplazaapartments.prospectportal.com/'
    site_domain = 'http://liveparkwayplaza.com/'

    property_name = 'Parkway Plaza'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderParkway(PPBaseParseSpiderE, MixinParkway):
    name = MixinParkway.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        if "Studio" in name:
            return "Studio"
        room_name = clean(c_sel.css('.sub-title ::text'))[0]
        return room_name


class CrawlSpiderParkway(MixinParkway, PPBaseCrawlSpiderE):
    name = MixinParkway.name + '-crawl'
    parse_spider = ParseSpiderParkway()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
