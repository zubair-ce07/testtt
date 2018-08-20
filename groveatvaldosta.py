import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveValdosta(BaseMixinPPE):
    name = property_slug = 'grove-at-valdosta'
    allowed_domains = [
        'groveatvaldosta.prospectportal.com',
        'groveatvaldosta.com'
    ]

    login_domain = 'https://groveatvaldosta.prospectportal.com/'
    site_domain = 'http://groveatvaldosta.com/'

    property_name = 'Grove at Valdosta'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveValdosta(PPBaseParseSpiderE, MixinGroveValdosta):
    name = MixinGroveValdosta.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveValdosta(MixinGroveValdosta, PPBaseCrawlSpiderE):
    name = MixinGroveValdosta.name + '-crawl'
    parse_spider = ParseSpiderGroveValdosta()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
