import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGroveHighland(BaseMixinPPE):
    name = property_slug = 'highland-quarters'
    allowed_domains = [
        'highlandquarters.prospectportal.com',
        'highlandquarters.com'
    ]

    login_domain = 'https://highlandquarters.prospectportal.com/'
    site_domain = 'http://highlandquarters.com/'

    property_name = 'Highland Quarters'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGroveHighland(PPBaseParseSpiderE, MixinGroveHighland):
    name = MixinGroveHighland.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return f"Studio {name}"
        return f"{room_name}-{name}"


class CrawlSpiderGroveHighland(MixinGroveHighland, PPBaseCrawlSpiderE):
    name = MixinGroveHighland.name + '-crawl'
    parse_spider = ParseSpiderGroveHighland()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
