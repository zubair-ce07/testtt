from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCooperBeech(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-columbia'
    allowed_domains = [
        'copperbeechcolumbia.prospectportal.com',
        'livecbeechcomo.com'
    ]

    login_domain = 'https://copperbeechcolumbia.prospectportal.com/'
    site_domain = 'http://livecbeechcomo.com/'

    property_name = 'Copper Beech at Columbia, MO'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCooperBeech(PPBaseParseSpiderE, MixinCooperBeech):
    name = MixinCooperBeech.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        return room_name


class CrawlSpiderCooperBeech(MixinCooperBeech, PPBaseCrawlSpiderE):
    name = MixinCooperBeech.name + '-crawl'
    parse_spider = ParseSpiderCooperBeech()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
