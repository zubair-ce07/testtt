import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinDomainCleveland(BaseMixinPPE):
    name = property_slug = 'domain-at-cleveland'
    allowed_domains = [
        'domainatcleveland.prospectportal.com',
        'domainatcleveland.com'
    ]

    login_domain = 'https://domainatcleveland.prospectportal.com/'
    site_domain = 'http://domainatcleveland.com/'

    property_name = 'Domain at Cleveland'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderDomainCleveland(PPBaseParseSpiderE, MixinDomainCleveland):
    name = MixinDomainCleveland.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', ',')
        if "0 Bedroom" in room_name:
            return f"Studio {name}"
        return f"{room_name} {name}"


class CrawlSpiderDomainClevelandh(MixinDomainCleveland, PPBaseCrawlSpiderE):
    name = MixinDomainCleveland.name + '-crawl'
    parse_spider = ParseSpiderDomainCleveland()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
