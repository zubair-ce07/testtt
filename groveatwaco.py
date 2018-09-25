import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveWaco(BaseMixinPPE):
    name = property_slug = 'grove-at-waco'
    allowed_domains = [
        'groveatwaco.prospectportal.com',
        'groveatwaco.com'
    ]

    login_domain = 'https://groveatwaco.prospectportal.com/'
    site_domain = 'http://groveatwaco.com/'

    property_name = 'Grove at Waco'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveWaco(PPBaseParseSpiderE, MixinGroveWaco):
    name = MixinGroveWaco.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveWaco(MixinGroveWaco, PPBaseCrawlSpiderE):
    name = MixinGroveWaco.name + '-crawl'
    parse_spider = ParseSpiderGroveWaco()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
