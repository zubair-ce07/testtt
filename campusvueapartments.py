from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusVue(BaseMixinPPE):
    name = property_slug = 'campus-vue'
    allowed_domains = [
        'campusvue.prospectportal.com',
        'campusvueapartments.com'
    ]

    login_domain = 'https://campusvue.prospectportal.com/'
    site_domain = 'https://campusvueapartments.com/'

    property_name = 'Campus Vue'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusVue(PPBaseParseSpiderE, MixinCampusVue):
    name = MixinCampusVue.name + '-parse'


class CrawlSpiderCampusVue(MixinCampusVue, PPBaseCrawlSpiderE):
    name = MixinCampusVue.name + '-crawl'
    parse_spider = ParseSpiderCampusVue()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
