from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCooperBeech(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-columbia'
    allowed_domains = [
        'copperbeechcolumbia.prospectportal.com',
        'livecbeechcomo.com'
    ]

    login_domain = 'https://copperbeechcolumbia.prospectportal.com/'
    site_domain = 'http://livecbeechcomo.com/'

    property_name = 'Copper Beech at Columbia, MO'
    landlord_name = 'Asset Campus Housing'

    login_email = "soft@gmail.com"
    login_password = "asd123"


class ParseSpiderCooperBeech(PPBaseParseSpiderE, MixinCooperBeech):
    name = MixinCooperBeech.name + '-parse'


class CrawlSpiderCooperBeech(MixinCooperBeech, PPBaseCrawlSpiderE):
    name = MixinCooperBeech.name + '-crawl'
    PPBaseCrawlSpiderE.login_email = MixinCooperBeech.login_email
    PPBaseCrawlSpiderE.login_password = MixinCooperBeech.login_password
    parse_spider = ParseSpiderCooperBeech()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
