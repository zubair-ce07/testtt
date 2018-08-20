from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinDomainTallahassee(BaseMixinPPE):
    name = property_slug = 'domain-at-tallahassee'
    allowed_domains = [
        'domainattallahasseeapts.prospectportal.com',
        'liveatdomain.com'
    ]

    login_domain = 'https://domainattallahasseeapts.prospectportal.com/'
    site_domain = 'http://liveatdomain.com/'

    property_name = 'Domain at Tallahassee'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderDomainTallahassee(PPBaseParseSpiderE, MixinDomainTallahassee):
    name = MixinDomainTallahassee.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return f"Studio {name}"
        return f"{room_name} {name}"


class CrawlSpiderDomainTallahassee(MixinDomainTallahassee, PPBaseCrawlSpiderE):
    name = MixinDomainTallahassee.name + '-crawl'
    parse_spider = ParseSpiderDomainTallahassee()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
