from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGrandMarc(BaseMixinPPE):
    name = property_slug = 'grand-marc-at-tallahassee'
    allowed_domains = [
        'grandmarctallahassee.prospectportal.com',
        'grandmarctallahassee.com'
    ]

    login_domain = 'https://grandmarctallahassee.prospectportal.com/'
    site_domain = 'http://grandmarctallahassee.com/'

    property_name = 'Grand Marc at Tallahassee'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGrandMarc(PPBaseParseSpiderE, MixinGrandMarc):
    name = MixinGrandMarc.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return f"Studio {name}"
        return f"{room_name}-{name}"


class CrawlSpiderGrandMarc(MixinGrandMarc, PPBaseCrawlSpiderE):
    name = MixinGrandMarc.name + '-crawl'
    parse_spider = ParseSpiderGrandMarc()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
