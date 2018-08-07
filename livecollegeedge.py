from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCollegeEdge(BaseMixinPPE):
    name = property_slug = 'college-edge'
    allowed_domains = [
        'collegeedge.prospectportal.com',
        'livecollegeedge.com'
    ]

    login_domain = 'https://collegeedge.prospectportal.com/'
    site_domain = 'http://www.livecollegeedge.com/'

    property_name = 'College Edge'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCollegeEdge(PPBaseParseSpiderE, MixinCollegeEdge):
    name = MixinCollegeEdge.name + '-parse'


class CrawlSpiderCollegeEdge(MixinCollegeEdge, PPBaseCrawlSpiderE):
    name = MixinCollegeEdge.name + '-crawl'
    parse_spider = ParseSpiderCollegeEdge()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
