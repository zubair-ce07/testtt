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


class CrawlSpiderCampusView(MixinCampusView, PPBaseCrawlSpiderE):
    name = MixinCampusView.name + '-crawl'
    parse_spider = ParseSpiderCampusView()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
