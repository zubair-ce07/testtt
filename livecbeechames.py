from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLiveBeechAmes(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-ames'
    allowed_domains = [
        'copperbeechatames.prospectportal.com',
        'livecbeechames.com'
    ]

    login_domain = 'https://copperbeechatames.prospectportal.com/'
    site_domain = 'http://livecbeechames.com/'

    property_name = 'Copper Beech at Ames'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLiveBeechAmes(PPBaseParseSpiderE, MixinLiveBeechAmes):
    name = MixinLiveBeechAmes.name + '-parse'


class CrawlSpiderCopperBeech(MixinLiveBeechAmes, PPBaseCrawlSpiderE):
    name = MixinLiveBeechAmes.name + '-crawl'
    parse_spider = ParseSpiderLiveBeechAmes()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
