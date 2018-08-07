from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusWalkny(BaseMixinPPE):
    name = property_slug = 'campus-walk-buffalo'
    allowed_domains = [
        'campuswalkone.prospectportal.com',
        'campuswalkny.com'
    ]

    login_domain = 'https://campuswalkone.prospectportal.com/'
    site_domain = 'http://campuswalkny.com/'

    property_name = 'Campus Walk Buffalo'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusWalkny(PPBaseParseSpiderE, MixinCampusWalkny):
    name = MixinCampusWalkny.name + '-parse'


class CrawlSpiderCampusWalkny(MixinCampusWalkny, PPBaseCrawlSpiderE):
    name = MixinCampusWalkny.name + '-crawl'
    parse_spider = ParseSpiderCampusWalkny()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
