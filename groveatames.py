import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveAmes(BaseMixinPPE):
    name = property_slug = 'grove-at-ames'
    allowed_domains = [
        'groveatames.prospectportal.com',
        'groveatames.com'
    ]

    login_domain = 'https://groveatames.prospectportal.com/'
    site_domain = 'http://groveatames.com/'

    property_name = 'Grove at Ames'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveAmes(PPBaseParseSpiderE, MixinGroveAmes):
    name = MixinGroveAmes.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom \\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveAmes(MixinGroveAmes, PPBaseCrawlSpiderE):
    name = MixinGroveAmes.name + '-crawl'
    parse_spider = ParseSpiderGroveAmes()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
