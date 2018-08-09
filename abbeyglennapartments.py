import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE



class MixinAbbeyGlenn(BaseMixinPPE):
    name = property_slug = 'abbey-glenn-apartments'
    allowed_domains = [
        'abbeyglenn.prospectportal.com',
        'abbeyglennapartments.com'
    ]

    login_domain = 'https://abbeyglenn.prospectportal.com/'
    site_domain = 'http://www.abbeyglennapartments.com/'

    property_name = 'Abbey Glenn Apartments'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderAbbeyGlenn(PPBaseParseSpiderE, MixinAbbeyGlenn):
    name = MixinAbbeyGlenn.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if name:
            return f"{room_name}-{name}"
        return room_name


class CrawlSpiderAbbeyGlenn(MixinAbbeyGlenn, PPBaseCrawlSpiderE):
    name = MixinAbbeyGlenn.name + '-crawl'
    parse_spider = ParseSpiderAbbeyGlenn()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
