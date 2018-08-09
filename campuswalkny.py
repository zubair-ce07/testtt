import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusWalkny(BaseMixinPPE):
    name = property_slug = 'campus-walk-buffalo'
    allowed_domains = [
        'campuswalkone.prospectportal.com',
        'campuswalkny.com'
    ]

    login_domain = 'https://campuswalkone.prospectportal.com/'
    site_domain = 'http://campuswalkny.com/'

    property_name = 'Campus Walk Buffalo'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusWalkny(PPBaseParseSpiderE, MixinCampusWalkny):
    name = MixinCampusWalkny.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        if re.search('(C2)|(D2)|(D1)', name[0]):
            room_name = clean(c_sel.css('.sub-title ::text'))
            room_name = room_name[0].replace('/', '')
            return f"{room_name}-{name[0]}"
        return name[0]


class CrawlSpiderCampusWalkny(MixinCampusWalkny, PPBaseCrawlSpiderE):
    name = MixinCampusWalkny.name + '-crawl'
    parse_spider = ParseSpiderCampusWalkny()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
