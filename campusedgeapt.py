import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusEdge(BaseMixinPPE):
    name = property_slug = 'campus-edge-fresno'
    allowed_domains = [
        'campusedgefresno.prospectportal.com',
        'campusedgeapt.com'
    ]

    login_domain = 'https://campusedgefresno.prospectportal.com/'
    site_domain = 'http://www.campusedgeapt.com/'

    property_name = 'Campus Edge - Fresno'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusEdge(PPBaseParseSpiderE, MixinCampusEdge):
    name = MixinCampusEdge.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        if re.search('(Bedroom)|(\d+x\d+)', name[0]):
            room_name = clean(c_sel.css('.sub-title ::text'))
            room_name = room_name[0].replace('/', '')
            return room_name
        return name[0]


class CrawlSpiderCampusEdge(MixinCampusEdge, PPBaseCrawlSpiderE):
    name = MixinCampusEdge.name + '-crawl'
    parse_spider = ParseSpiderCampusEdge()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
