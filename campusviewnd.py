from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusView(BaseMixinPPE):
    name = property_slug = 'campus-view-apartments'
    allowed_domains = [
        'campusviewapartments.prospectportal.com',
        'ccampusviewnd.com'
    ]

    login_domain = 'https://campusviewapartments.prospectportal.com/'
    site_domain = 'http://campusviewnd.com/'

    property_name = 'Campus View Apartments'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusView(PPBaseParseSpiderE, MixinCampusView):
    name = MixinCampusView.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderCampusView(MixinCampusView, PPBaseCrawlSpiderE):
    name = MixinCampusView.name + '-crawl'
    parse_spider = ParseSpiderCampusView()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
