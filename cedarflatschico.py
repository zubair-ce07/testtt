from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCedarFlats(BaseMixinPPE):
    name = property_slug = 'cedar-flats'
    allowed_domains = [
        'cedarflats.prospectportal.com',
        'cedarflatschico.com'
    ]

    login_domain = 'https://cedarflats.prospectportal.com/'
    site_domain = 'http://cedarflatschico.com/'

    property_name = 'Cedar Flats'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCedarFlats(PPBaseParseSpiderE, MixinCedarFlats):
    name = MixinCedarFlats.name + '-parse'


class CrawlSpiderCedarFlats(MixinCedarFlats, PPBaseCrawlSpiderE):
    name = MixinCedarFlats.name + '-crawl'
    parse_spider = ParseSpiderCedarFlats()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
