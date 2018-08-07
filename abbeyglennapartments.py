from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinAbbeyGlenn(BaseMixinPPE):
    name = property_slug = 'abbey-glenn-apartments'
    allowed_domains = [
        'abbeyglenn.prospectportal.com',
        'abbeyglennapartments.com'
    ]

    login_domain = 'https://abbeyglenn.prospectportal.com/'
    site_domain = 'http://www.abbeyglennapartments.com/'

    property_name = 'Abbey Glenn Apartments'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderAbbeyGlenn(PPBaseParseSpiderE, MixinAbbeyGlenn):
    name = MixinAbbeyGlenn.name + '-parse'


class CrawlSpiderAbbeyGlenn(MixinAbbeyGlenn, PPBaseCrawlSpiderE):
    name = MixinAbbeyGlenn.name + '-crawl'
    parse_spider = ParseSpiderAbbeyGlenn()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
