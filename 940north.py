from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class Mixin940North(BaseMixinPPE):
    name = property_slug = '940-north'
    allowed_domains = [
        'aspyreapts.prospectportal.com',
        '940north.com'
    ]

    login_domain = 'https://aspyreapts.prospectportal.com/'
    site_domain = 'http://www.940north.com/'

    property_name = '940 North'
    landlord_name = 'Asset Campus Housing'


class ParseSpider940North(PPBaseParseSpiderE, Mixin940North):
    name = Mixin940North.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpider940North(Mixin940North, PPBaseCrawlSpiderE):
    name = Mixin940North.name + '-crawl'
    parse_spider = ParseSpider940North()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
