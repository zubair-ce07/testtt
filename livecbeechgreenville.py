from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLiveBeechGreenville(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-greenville'
    allowed_domains = [
        'copperbeechgreenville.prospectportal.com',
        'livecbeechgreenville.com'
    ]

    login_domain = 'https://copperbeechgreenville.prospectportal.com/'
    site_domain = 'http://livecbeechgreenville.com/'

    property_name = 'Copper Beech at Greenville'
    landlord_name = 'Asset Campus Housing'

    login_email = "yay@gmail.com"
    login_password = "asd123"


class ParseSpiderLiveBeechGreenville(PPBaseParseSpiderE, MixinLiveBeechGreenville):
    name = MixinLiveBeechGreenville.name + '-parse'


class CrawlSpiderLiveBeechGreenville(MixinLiveBeechGreenville, PPBaseCrawlSpiderE):
    name = MixinLiveBeechGreenville.name + '-crawl'
    PPBaseCrawlSpiderE.login_email = MixinLiveBeechGreenville.login_email
    PPBaseCrawlSpiderE.login_password = MixinLiveBeechGreenville.login_password
    parse_spider = ParseSpiderLiveBeechGreenville()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
