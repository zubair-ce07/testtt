import re

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
        name = clean(c_sel.css('.title ::text'))
        name = name[0].replace('R', '- R')
        room_name = re.sub('(\d+)x(\d+)\s?(.?)', '\\1 Bedroom \\2 Bathroom \\3', name)
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderCampusCourtApartments(MixinCampusCourtApartments, PPBaseCrawlSpiderE):
    name = MixinCampusCourtApartments.name + '-crawl'
    parse_spider = ParseSpiderCampusCourtApartments()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
