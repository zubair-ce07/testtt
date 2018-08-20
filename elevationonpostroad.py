import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinElevationPost(BaseMixinPPE):
    name = property_slug = 'elevation-on-post'
    allowed_domains = [
        'elevationonpost.prospectportal.com',
        'elevationonpostroad.com'
    ]

    login_domain = 'https://elevationonpost.prospectportal.com/'
    site_domain = 'http://elevationonpostroad.com/'

    property_name = 'Elevation on Post'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderElevationPost(PPBaseParseSpiderE, MixinElevationPost):
    name = MixinElevationPost.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', ',')
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderElevationPost(MixinElevationPost, PPBaseCrawlSpiderE):
    name = MixinElevationPost.name + '-crawl'
    parse_spider = ParseSpiderElevationPost()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
