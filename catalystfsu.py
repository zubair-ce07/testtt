from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCatalyst(BaseMixinPPE):
    name = property_slug = 'catalyst'
    allowed_domains = [
        'catalyst.prospectportal.com',
        'catalystfsu.com'
    ]

    login_domain = 'https://catalyst.prospectportal.com/'
    site_domain = 'http://catalystfsu.com/'

    property_name = 'Catalyst'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCatalyst(PPBaseParseSpiderE, MixinCatalyst):
    name = MixinCatalyst.name + '-parse'


class CrawlSpiderCatalyst(MixinCatalyst, PPBaseCrawlSpiderE):
    name = MixinCatalyst.name + '-crawl'
    parse_spider = ParseSpiderCatalyst()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
