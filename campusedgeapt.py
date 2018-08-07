from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusEdge(BaseMixinPPE):
    name = property_slug = 'campus-edge-fresno'
    allowed_domains = [
        'campusedgefresno.prospectportal.com',
        'campusedgeapt.com'
    ]

    login_domain = 'https://campusedgefresno.prospectportal.com/'
    site_domain = 'http://www.campusedgeapt.com/'

    property_name = 'Campus Edge - Fresno'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusEdge(PPBaseParseSpiderE, MixinCampusEdge):
    name = MixinCampusEdge.name + '-parse'


class CrawlSpiderCampusEdge(MixinCampusEdge, PPBaseCrawlSpiderE):
    name = MixinCampusEdge.name + '-crawl'
    parse_spider = ParseSpiderCampusEdge()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
