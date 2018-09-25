from student.utils import clean
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

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderCampusHeights(MixinCampusHeights, PPBaseCrawlSpiderE):
    name = MixinCampusHeights.name + '-crawl'
    parse_spider = ParseSpiderCampusHeights()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
