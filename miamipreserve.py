import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinMiami(BaseMixinPPE):
    name = property_slug = 'miami-preserve'
    allowed_domains = [
        'miamipreserve.prospectportal.com',
        'miamipreserve.com'
    ]

    login_domain = 'https://miamipreserve.prospectportal.com/'
    site_domain = 'http://miamipreserve.com/'

    property_name = 'Miami Preserve'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderMiami(PPBaseParseSpiderE, MixinMiami):
    name = MixinMiami.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('.*(\d+)X(\d+)\s?.?', '\\1 Bedroom \\2 Bathroom', name[0])
        return room_name


class CrawlSpiderMiami(MixinMiami, PPBaseCrawlSpiderE):
    name = MixinMiami.name + '-crawl'
    parse_spider = ParseSpiderMiami()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
