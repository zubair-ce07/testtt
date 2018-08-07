from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCambridge(BaseMixinPPE):
    name = property_slug = 'cambridge-at-college-station'
    allowed_domains = [
        'cambridgeatcollegestation.prospectportal.com',
        'cambridgeatcollegestation.com'
    ]

    login_domain = 'https://cambridgeatcollegestation.prospectportal.com/'
    site_domain = 'http://www.cambridgeatcollegestation.com/'

    property_name = 'Cambridge at College Station'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCambridge(PPBaseParseSpiderE, MixinCambridge):
    name = MixinCambridge.name + '-parse'


class CrawlSpiderCambridge(MixinCambridge, PPBaseCrawlSpiderE):
    name = MixinCambridge.name + '-crawl'
    parse_spider = ParseSpiderCambridge()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
