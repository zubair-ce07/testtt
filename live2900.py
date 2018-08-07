from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class Mixinlive2900(BaseMixinPPE):
    name = property_slug = '2900-student-apartments'
    allowed_domains = [
        '2900.prospectportal.com',
        'live2900.com'
    ]

    login_domain = 'https://2900.prospectportal.com/'
    site_domain = 'http://www.live2900.com/'

    property_name = '2900 Student Apartments'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderlive2900(PPBaseParseSpiderE, Mixinlive2900):
    name = Mixinlive2900.name + '-parse'


class CrawlSpiderlive2900(Mixinlive2900, PPBaseCrawlSpiderE):
    name = Mixinlive2900.name + '-crawl'
    parse_spider = ParseSpiderlive2900()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
