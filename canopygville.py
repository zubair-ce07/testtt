from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCanopyApartments(BaseMixinPPE):
    name = property_slug = 'canopy-apartments'
    allowed_domains = [
        'canopy.prospectportal.com',
        'canopygville.com'
    ]

    login_domain = 'https://canopy.prospectportal.com/'
    site_domain = 'http://www.canopygville.com/'

    property_name = 'Canopy Apartments'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCanopyApartments(PPBaseParseSpiderE, MixinCanopyApartments):
    name = MixinCanopyApartments.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = clean(c_sel.css('.sub-title ::text'))
        return f"{room_name[0]}-{name[0]}"


class CrawlSpiderCanopyApartments(MixinCanopyApartments, PPBaseCrawlSpiderE):
    name = MixinCanopyApartments.name + '-crawl'
    parse_spider = ParseSpiderCanopyApartments()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
