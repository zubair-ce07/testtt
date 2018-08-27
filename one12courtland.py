import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCourtland(BaseMixinPPE):
    name = property_slug = 'one12-courtland'
    allowed_domains = [
        'one12courtland.prospectportal.com',
        'one12courtland.com'
    ]

    login_domain = 'https://one12courtland.prospectportal.com/'
    site_domain = 'http://one12courtland.com/'

    property_name = 'One12 Courtland'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCourtland(PPBaseParseSpiderE, MixinCourtland):
    name = MixinCourtland.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        if "Studio" in name:
            return name
        room_name = re.sub('(\d+)x(\d+)\s?(.*)', '\\1 Bedroom-\\2 Bath\\3', name)
        return room_name


class CrawlSpiderCourtland(MixinCourtland, PPBaseCrawlSpiderE):
    name = MixinCourtland.name + '-crawl'
    parse_spider = ParseSpiderCourtland()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
