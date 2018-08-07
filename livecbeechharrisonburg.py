from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLiveBeechHarrisonburg(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-harrisonburg'
    allowed_domains = [
        'copperbeechharrisonburg.prospectportal.com',
        'livecbeechharrisonburg.com'
    ]

    login_domain = 'https://copperbeechharrisonburg.prospectportal.com/'
    site_domain = 'http://livecbeechharrisonburg.com/'

    property_name = 'Copper Beech at Harrisonburg'
    landlord_name = 'Asset Campus Housing'



class ParseSpiderLiveBeechHarrisonburg(PPBaseParseSpiderE, MixinLiveBeechHarrisonburg):
    name = MixinLiveBeechHarrisonburg.name + '-parse'


class CrawlSpiderLiveBeechHarrisonburg(MixinLiveBeechHarrisonburg, PPBaseCrawlSpiderE):
    name = MixinLiveBeechHarrisonburg.name + '-crawl'
    parse_spider = ParseSpiderLiveBeechHarrisonburg()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
