import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveLubbock(BaseMixinPPE):
    name = property_slug = 'grove-at-lubbock'
    allowed_domains = [
        'groveatlubbock.prospectportal.com',
        'groveatlubbock.com'
    ]

    login_domain = 'https://groveatlubbock.prospectportal.com/'
    site_domain = 'http://groveatlubbock.com/'

    property_name = 'Grove at Lubbock'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveLubbock(PPBaseParseSpiderE, MixinGroveLubbock):
    name = MixinGroveLubbock.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveLubbock(MixinGroveLubbock, PPBaseCrawlSpiderE):
    name = MixinGroveLubbock.name + '-crawl'
    parse_spider = ParseSpiderGroveLubbock()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
