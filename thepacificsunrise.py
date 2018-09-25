import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinSunrise(BaseMixinPPE):
    name = property_slug = 'pacific-sunrise'
    allowed_domains = [
        'pacificsunrise.prospectportal.com',
        'thepacificsunrise.com'
    ]

    login_domain = 'https://pacificsunrise.prospectportal.com/'
    site_domain = 'http://thepacificsunrise.com/'

    property_name = 'Pacific Sunrise'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderSunrise(PPBaseParseSpiderE, MixinSunrise):
    name = MixinSunrise.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        if "Studio" in name:
            return name
        room_name = re.sub('(\d+\.?\d?)x(\d+\.?\d?)\s?(.*)', '\\1 Bedroom/\\2 Bathroom \\3', name)
        return room_name


class CrawlSpiderSunrise(MixinSunrise, PPBaseCrawlSpiderE):
    name = MixinSunrise.name + '-crawl'
    parse_spider = ParseSpiderSunrise()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
