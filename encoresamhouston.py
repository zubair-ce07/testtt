import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinSamHouston(BaseMixinPPE):
    name = property_slug = 'encore-at-sam-houston'
    allowed_domains = [
        'encoreatsamhouston.prospectportal.com',
        'encoresamhouston.com'
    ]

    login_domain = 'https://encoreatsamhouston.prospectportal.com/'
    site_domain = 'http://encoresamhouston.com/'

    property_name = 'Encore at Sam Houston'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderSamHouston(PPBaseParseSpiderE, MixinSamHouston):
    name = MixinSamHouston.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)x(\d+)\s?(.?)', '\\1 Bedroom \\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderSamHouston(MixinSamHouston, PPBaseCrawlSpiderE):
    name = MixinSamHouston.name + '-crawl'
    parse_spider = ParseSpiderSamHouston()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
