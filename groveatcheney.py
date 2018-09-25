import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveCheney(BaseMixinPPE):
    name = property_slug = 'grove-at-cheney'
    allowed_domains = [
        'groveatcheney.prospectportal.com',
        'groveatcheney.com'
    ]

    login_domain = 'https://groveatcheney.prospectportal.com/'
    site_domain = 'http://groveatcheney.com/'

    property_name = 'Grove at Cheney'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveCheney(PPBaseParseSpiderE, MixinGroveCheney):
    name = MixinGroveCheney.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveCheney(MixinGroveCheney, PPBaseCrawlSpiderE):
    name = MixinGroveCheney.name + '-crawl'
    parse_spider = ParseSpiderGroveCheney()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
