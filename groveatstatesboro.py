import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveStatesboro(BaseMixinPPE):
    name = property_slug = 'grove-at-statesboro'
    allowed_domains = [
        'groveatstatesboro.prospectportal.com',
        'groveatstatesboro.com'
    ]

    login_domain = 'https://groveatstatesboro.prospectportal.com/'
    site_domain = 'http://groveatstatesboro.com/'

    property_name = 'Grove at Statesboro'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveStatesboro(PPBaseParseSpiderE, MixinGroveStatesboro):
    name = MixinGroveStatesboro.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveStatesboro(MixinGroveStatesboro, PPBaseCrawlSpiderE):
    name = MixinGroveStatesboro.name + '-crawl'
    parse_spider = ParseSpiderGroveStatesboro()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
