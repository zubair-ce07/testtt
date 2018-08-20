import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinDakotaRanch(BaseMixinPPE):
    name = property_slug = 'dakota-ranch'
    allowed_domains = [
        'dakotaranch.prospectportal.com',
        'dakotaranchapartments.com'
    ]

    login_domain = 'https://dakotaranch.prospectportal.com/'
    site_domain = 'http://dakotaranchapartments.com/'

    property_name = 'Dakota Ranch'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderDakotaRanch(PPBaseParseSpiderE, MixinDakotaRanch):
    name = MixinDakotaRanch.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '|')
        if "0 Bedroom" in room_name:
            return "Studio"
        return f"{name} {room_name}"


class CrawlSpiderDakotaRanch(MixinDakotaRanch, PPBaseCrawlSpiderE):
    name = MixinDakotaRanch.name + '-crawl'
    parse_spider = ParseSpiderDakotaRanch()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
