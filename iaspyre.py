from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinAspyre(BaseMixinPPE):
    name = property_slug = 'aspyre-at-assembly-station'
    allowed_domains = [
        'aspyreapts.prospectportal.com',
        'iaspyre.com'
    ]

    login_domain = 'https://aspyreapts.prospectportal.com/'
    site_domain = 'http://iaspyre.com/'

    property_name = 'Aspyre'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderAspyre(PPBaseParseSpiderE, MixinAspyre):
    name = MixinAspyre.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderAspyre(MixinAspyre, PPBaseCrawlSpiderE):
    name = MixinAspyre.name + '-crawl'
    parse_spider = ParseSpiderAspyre()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
