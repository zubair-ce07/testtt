import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinIndigo(BaseMixinPPE):
    name = property_slug = 'indigo-at-110'
    allowed_domains = [
        'indigo110.prospectportal.com',
        'indigoat110.com'
    ]

    login_domain = 'https://indigo110.prospectportal.com/'
    site_domain = 'http://indigoat110.com/'

    property_name = 'Indigo at 110'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderIndigo(PPBaseParseSpiderE, MixinIndigo):
    name = MixinIndigo.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)x(\d+)\s?(.*)', '\\1 Bedroom \\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderIndigo(MixinIndigo, PPBaseCrawlSpiderE):
    name = MixinIndigo.name + '-crawl'
    parse_spider = ParseSpiderIndigo()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
