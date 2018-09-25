import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveSlipperyRock(BaseMixinPPE):
    name = property_slug = 'grove-at-slippery-rock'
    allowed_domains = [
        'groveatslipperyrock.prospectportal.com',
        'groveatslipperyrock.com'
    ]

    login_domain = 'https://groveatslipperyrock.prospectportal.com/'
    site_domain = 'http://groveatslipperyrock.com/'

    property_name = 'Grove at Slippery Rock'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderSlipperyRock(PPBaseParseSpiderE, MixinGroveSlipperyRock):
    name = MixinGroveSlipperyRock.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?.*', '\\1 Bed/\\2 Bath', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderSlipperyRock(MixinGroveSlipperyRock, PPBaseCrawlSpiderE):
    name = MixinGroveSlipperyRock.name + '-crawl'
    parse_spider = ParseSpiderSlipperyRock()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
