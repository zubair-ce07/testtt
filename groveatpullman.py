import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGrovePullman(BaseMixinPPE):
    name = property_slug = 'grove-at-pullman'
    allowed_domains = [
        'groveatpullman.prospectportal.com',
        'groveatpullman.com'
    ]

    login_domain = 'https://groveatpullman.prospectportal.com/'
    site_domain = 'http://groveatpullman.com/'

    property_name = 'Grove at Pullman'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGrovePullman(PPBaseParseSpiderE, MixinGrovePullman):
    name = MixinGrovePullman.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGrovePullman(MixinGrovePullman, PPBaseCrawlSpiderE):
    name = MixinGrovePullman.name + '-crawl'
    parse_spider = ParseSpiderGrovePullman()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
