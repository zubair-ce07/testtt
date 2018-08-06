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

    login_email = "arbi@gmail.com"
    login_password = "asd123"


class ParseSpiderLiveBeechAmes(PPBaseParseSpiderE, MixinLiveBeechAmes):
    name = MixinLiveBeechAmes.name + '-parse'


class CrawlSpiderCopperBeech(MixinLiveBeechAmes, PPBaseCrawlSpiderE):
    name = MixinLiveBeechAmes.name + '-crawl'
    PPBaseCrawlSpiderE.login_email = MixinLiveBeechAmes.login_email
    PPBaseCrawlSpiderE.login_password = MixinLiveBeechAmes.login_password
    parse_spider = ParseSpiderLiveBeechAmes()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
