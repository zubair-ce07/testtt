from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinConection(BaseMixinPPE):
    name = property_slug = 'connection-at-lawrence'
    allowed_domains = [
        'connectionatlawrence.prospectportal.com',
        'connectionatlawrence.com'
    ]

    login_domain = 'https://connectionatlawrence.prospectportal.com/'
    site_domain = 'http://www.connectionatlawrence.com/'

    property_name = 'connection at lawrence'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderConection(PPBaseParseSpiderE, MixinConection):
    name = MixinConection.name + '-parse'


class CrawlSpiderConection(MixinConection, PPBaseCrawlSpiderE):
    name = MixinConection.name + '-crawl'
    parse_spider = ParseSpiderConection()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
