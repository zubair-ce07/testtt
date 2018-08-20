import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinKnightsCircle(BaseMixinPPE):
    name = property_slug = 'knights-circle'
    allowed_domains = [
        'knightscircle.prospectportal.com',
        'liveatknightscircle.com'
    ]

    login_domain = 'https://knightscircle.prospectportal.com/'
    site_domain = 'http://liveatknightscircle.com/'

    property_name = 'Knights Circle'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderKnightsCircle(PPBaseParseSpiderE, MixinKnightsCircle):
    name = MixinKnightsCircle.name + '-parse'


class CrawlSpiderKnightsCircle(MixinKnightsCircle, PPBaseCrawlSpiderE):
    name = MixinKnightsCircle.name + '-crawl'
    parse_spider = ParseSpiderKnightsCircle()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
