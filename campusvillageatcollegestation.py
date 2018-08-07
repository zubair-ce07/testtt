from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusVillage(BaseMixinPPE):
    name = property_slug = 'campus-village-at-college-station'
    allowed_domains = [
        'campusvillagecs.prospectportal.com',
        'campusvillageatcollegestation.com'
    ]

    login_domain = 'https://campusvillagecs.prospectportal.com/'
    site_domain = 'http://campusvillageatcollegestation.com/'

    property_name = 'Campus Village at College Station'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusVillage(PPBaseParseSpiderE, MixinCampusVillage):
    name = MixinCampusVillage.name + '-parse'


class CrawlSpiderCampusVillage(MixinCampusVillage, PPBaseCrawlSpiderE):
    name = MixinCampusVillage.name + '-crawl'
    parse_spider = ParseSpiderCampusVillage()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
