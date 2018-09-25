import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLofts(BaseMixinPPE):
    name = property_slug = 'lofts-nacogdoches'
    allowed_domains = [
        'loftsnacogdoches.prospectportal.com',
        'liveatthelofts.com'
    ]

    login_domain = 'https://loftsnacogdoches.prospectportal.com/'
    site_domain = 'http://liveatthelofts.com/'

    property_name = 'Lofts Nacogdoches'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLofts(PPBaseParseSpiderE, MixinLofts):
    name = MixinLofts.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)x(\d+)\s?(.?)', '\\1 Bedroom \\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderLofts(MixinLofts, PPBaseCrawlSpiderE):
    name = MixinLofts.name + '-crawl'
    parse_spider = ParseSpiderLofts()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
