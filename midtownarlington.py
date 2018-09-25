import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinMidtown(BaseMixinPPE):
    name = property_slug = 'midtown'
    allowed_domains = [
        'liveatmidtownarlington.prospectportal.com',
        'midtownarlington.com'
    ]

    login_domain = 'https://liveatmidtownarlington.prospectportal.com/'
    site_domain = 'http://midtownarlington.com/'

    property_name = 'Midtown'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderMidtown(PPBaseParseSpiderE, MixinMidtown):
    name = MixinMidtown.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('.*(\d+)x(\d+)\s?.?', '\\1 Bedroom / \\2 Bath', name[0])
        return room_name


class CrawlSpiderMidtown(MixinMidtown, PPBaseCrawlSpiderE):
    name = MixinMidtown.name + '-crawl'
    parse_spider = ParseSpiderMidtown()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
