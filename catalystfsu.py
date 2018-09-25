from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCatalyst(BaseMixinPPE):
    name = property_slug = 'catalyst'
    allowed_domains = [
        'catalyst.prospectportal.com',
        'catalystfsu.com'
    ]

    login_domain = 'https://catalyst.prospectportal.com/'
    site_domain = 'http://catalystfsu.com/'

    property_name = 'Catalyst'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCatalyst(PPBaseParseSpiderE, MixinCatalyst):
    name = MixinCatalyst.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        return room_name


class CrawlSpiderCatalyst(MixinCatalyst, PPBaseCrawlSpiderE):
    name = MixinCatalyst.name + '-crawl'
    parse_spider = ParseSpiderCatalyst()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
