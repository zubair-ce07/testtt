from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinKingsville(BaseMixinPPE):
    name = property_slug = 'legends-at-kingsville'
    allowed_domains = [
        'legendsatkingsville.prospectportal.com',
        'legendsatkingsville.com'
    ]

    login_domain = 'https://legendsatkingsville.prospectportal.com/'
    site_domain = 'http://legendsatkingsville.com/'

    property_name = 'Legends at Kingsville'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderKingsville(PPBaseParseSpiderE, MixinKingsville):
    name = MixinKingsville.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '|')
        if "0 Bedroom" in room_name:
            return f"{name}||Studio"
        return f"{name}||{room_name}"


class CrawlSpiderKingsville(MixinKingsville, PPBaseCrawlSpiderE):
    name = MixinKingsville.name + '-crawl'
    parse_spider = ParseSpiderKingsville()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
