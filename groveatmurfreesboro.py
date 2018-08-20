import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveMurfreesboro(BaseMixinPPE):
    name = property_slug = 'grove-at-murfreesboro'
    allowed_domains = [
        'groveatmurfreesboro.prospectportal.com',
        'groveatmurfreesboro.com'
    ]

    login_domain = 'https://groveatmurfreesboro.prospectportal.com/'
    site_domain = 'http://groveatmurfreesboro.com/'

    property_name = 'Grove at Murfreesboro'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveMurfreesboro(PPBaseParseSpiderE, MixinGroveMurfreesboro):
    name = MixinGroveMurfreesboro.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)X(\d+)\s?(.?)', '\\1 Bedroom/\\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderGroveMurfreesboro(MixinGroveMurfreesboro, PPBaseCrawlSpiderE):
    name = MixinGroveMurfreesboro.name + '-crawl'
    parse_spider = ParseSpiderGroveMurfreesboro()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
