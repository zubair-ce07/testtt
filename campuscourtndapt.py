from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusCourtApartments(BaseMixinPPE):
    name = property_slug = 'campus-court-apartments'
    allowed_domains = [
        'campuscourtapts.prospectportal.com',
        'campuscourtnd.com'
    ]

    login_domain = 'https://campuscourtapts.prospectportal.com/'
    site_domain = 'http://campuscourtnd.com/'

    property_name = 'Campus Court Apartments'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusCourtApartments(PPBaseParseSpiderE, MixinCampusCourtApartments):
    name = MixinCampusCourtApartments.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderCampusCourtApartments(MixinCampusCourtApartments, PPBaseCrawlSpiderE):
    name = MixinCampusCourtApartments.name + '-crawl'
    parse_spider = ParseSpiderCampusCourtApartments()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
