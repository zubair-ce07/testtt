import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveAuburn(BaseMixinPPE):
    name = property_slug = 'grove-at-auburn'
    allowed_domains = [
        'groveatauburn.prospectportal.com',
        'groveatauburn.com'
    ]

    login_domain = 'https://groveatauburn.prospectportal.com/'
    site_domain = 'http://groveatauburn.com/'

    property_name = 'Grove at Auburn'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveAuburn(PPBaseParseSpiderE, MixinGroveAuburn):
    name = MixinGroveAuburn.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveAuburn(MixinGroveAuburn, PPBaseCrawlSpiderE):
    name = MixinGroveAuburn.name + '-crawl'
    parse_spider = ParseSpiderGroveAuburn()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
