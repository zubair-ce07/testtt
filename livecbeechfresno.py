from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLiveBeechFresno(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-fresno'
    allowed_domains = [
        'copperbeechfresno.prospectportal.com',
        'livecbeechfresno.com'
    ]

    login_domain = 'https://copperbeechfresno.prospectportal.com/'
    site_domain = 'http://livecbeechfresno.com/'

    property_name = 'Copper Beech at Fresno'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLiveBeechFresno(PPBaseParseSpiderE, MixinLiveBeechFresno):
    name = MixinLiveBeechFresno.name + '-parse'


class CrawlSpiderLiveBeechFresno(MixinLiveBeechFresno, PPBaseCrawlSpiderE):
    name = MixinLiveBeechFresno.name + '-crawl'
    parse_spider = ParseSpiderLiveBeechFresno()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
