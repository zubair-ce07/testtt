import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinBowlingGreen(BaseMixinPPE):
    name = property_slug = 'copper-beech-bowling-green'
    allowed_domains = [
        'copperbeechbowlinggreen.prospectportal.com',
        'livecbeechbowlinggreen.com'
    ]

    login_domain = 'https://copperbeechbowlinggreen.prospectportal.com/'
    site_domain = 'http://www.livecbeechbowlinggreen.com/'

    property_name = 'Copper Beech Bowling Green'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderBowlingGreen(PPBaseParseSpiderE, MixinBowlingGreen):
    name = MixinBowlingGreen.name + '-parse'
    room_name_map = ['Furnished', 'Unfurnished']

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        for room in self.room_name_map:
            if room in name[0]:
                return f"{room_name}-{room}"
        return room_name


class CrawlSpiderBowlingGreen(MixinBowlingGreen, PPBaseCrawlSpiderE):
    name = MixinBowlingGreen.name + '-crawl'
    parse_spider = ParseSpiderBowlingGreen()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
