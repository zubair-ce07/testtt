from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusHeights(BaseMixinPPE):
    name = property_slug = 'campus-heights'
    allowed_domains = [
        'campusheightsapts.prospectportal.com',
        'livecampusheights.com'
    ]

    login_domain = 'https://campusheightsapts.prospectportal.com/'
    site_domain = 'http://www.livecampusheights.com/'

    property_name = 'Campus Heights'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusHeights(PPBaseParseSpiderE, MixinCampusHeights):
    name = MixinCampusHeights.name + '-parse'


class CrawlSpiderCampusHeights(MixinCampusHeights, PPBaseCrawlSpiderE):
    name = MixinCampusHeights.name + '-crawl'
    parse_spider = ParseSpiderCampusHeights()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
