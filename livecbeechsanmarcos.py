from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLivecSanMarcos(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-san-marcos-tx'
    allowed_domains = [
        'copperbeechsanmarcos.prospectportal.com',
        'livecbeechsanmarcos.com'
    ]

    login_domain = 'https://copperbeechsanmarcos.prospectportal.com/'
    site_domain = 'http://livecbeechsanmarcos.com/'

    property_name = 'Copper Beech at San Marcos'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLivecSanMarcos(PPBaseParseSpiderE, MixinLivecSanMarcos):
    name = MixinLivecSanMarcos.name + '-parse'


class CrawlSpiderLivecSanMarcos(MixinLivecSanMarcos, PPBaseCrawlSpiderE):
    name = MixinLivecSanMarcos.name + '-crawl'
    parse_spider = ParseSpiderLivecSanMarcos()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
