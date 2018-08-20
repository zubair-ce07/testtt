import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveMoscow(BaseMixinPPE):
    name = property_slug = 'grove-at-moscow'
    allowed_domains = [
        'groveatmoscow.prospectportal.com',
        'groveatmoscow.com'
    ]

    login_domain = 'https://groveatmoscow.prospectportal.com/'
    site_domain = 'http://groveatmoscow.com/'

    property_name = 'Grove at Moscow'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveMoscow(PPBaseParseSpiderE, MixinGroveMoscow):
    name = MixinGroveMoscow.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveMoscow(MixinGroveMoscow, PPBaseCrawlSpiderE):
    name = MixinGroveMoscow.name + '-crawl'
    parse_spider = ParseSpiderGroveMoscow()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
