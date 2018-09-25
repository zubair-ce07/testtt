from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinNacogdoches(BaseMixinPPE):
    name = property_slug = 'legends-at-nacogdoches'
    allowed_domains = [
        'legendsatnacogdoches.prospectportal.com',
        'liveatlegends.com'
    ]

    login_domain = 'https://legendsatnacogdoches.prospectportal.com/'
    site_domain = 'http://liveatlegends.com/'

    property_name = 'Legends at Nacogdoches'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderNacogdoches(PPBaseParseSpiderE, MixinNacogdoches):
    name = MixinNacogdoches.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        if "0 Bedroom" in room_name:
            return f"Studio {name}"
        return f"{room_name[0]} {name}"


class CrawlSpiderNacogdoches(MixinNacogdoches, PPBaseCrawlSpiderE):
    name = MixinNacogdoches.name + '-crawl'
    parse_spider = ParseSpiderNacogdoches()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
