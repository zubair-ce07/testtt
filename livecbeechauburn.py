import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinAuburn(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-auburn'
    allowed_domains = [
        'copperbeechauburn.prospectportal.com',
        'livecbeechauburn.com'
    ]

    login_domain = 'https://copperbeechauburn.prospectportal.com/'
    site_domain = 'http://www.livecbeechauburn.com/'

    property_name = 'Copper Beech Auburn'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderAuburn(PPBaseParseSpiderE, MixinAuburn):
    name = MixinAuburn.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        return  re.sub('(\d.?\d?) Bedroom \/ (\d.?\d?) Bathroom', '\\1 Bed / \\2 Bath', room_name[0])


class CrawlSpiderAuburn(MixinAuburn, PPBaseCrawlSpiderE):
    name = MixinAuburn.name + '-crawl'
    parse_spider = ParseSpiderAuburn()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
