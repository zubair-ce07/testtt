import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveHuntsville(BaseMixinPPE):
    name = property_slug = 'grove-at-huntsville'
    allowed_domains = [
        'groveathuntsville.prospectportal.com',
        'groveathuntsville.com'
    ]

    login_domain = 'https://groveathuntsville.prospectportal.com/'
    site_domain = 'http://groveathuntsville.com/'

    property_name = 'Grove at Huntsville'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveHuntsville(PPBaseParseSpiderE, MixinGroveHuntsville):
    name = MixinGroveHuntsville.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveHuntsville(MixinGroveHuntsville, PPBaseCrawlSpiderE):
    name = MixinGroveHuntsville.name + '-crawl'
    parse_spider = ParseSpiderGroveHuntsville()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
