from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLiveBeechMorganTown(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-morgantown'
    allowed_domains = [
        'copperbeechmorgantown.prospectportal.com',
        'livecbeechmorgantown.com'
    ]

    login_domain = 'https://copperbeechmorgantown.prospectportal.com/'
    site_domain = 'http://livecbeechmorgantown.com/'

    property_name = 'Copper Beech at Morgantown'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLiveBeechMorganTown(PPBaseParseSpiderE, MixinLiveBeechMorganTown):
    name = MixinLiveBeechMorganTown.name + '-parse'


class CrawlSpiderLiveBeechMorganTown(MixinLiveBeechMorganTown, PPBaseCrawlSpiderE):
    name = MixinLiveBeechMorganTown.name + '-crawl'
    parse_spider = ParseSpiderLiveBeechMorganTown()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
