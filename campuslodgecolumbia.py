from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusLodge(BaseMixinPPE):
    name = property_slug = 'campus-lodge-columbia'
    allowed_domains = [
        'campuslodge.prospectportal.com',
        'campuslodgecolumbia.com'
    ]

    login_domain = 'https://campuslodge.prospectportal.com/'
    site_domain = 'http://www.campuslodgecolumbia.com/'

    property_name = 'Campus Lodge Columbia'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusLodge(PPBaseParseSpiderE, MixinCampusLodge):
    name = MixinCampusLodge.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderCampusLodge(MixinCampusLodge, PPBaseCrawlSpiderE):
    name = MixinCampusLodge.name + '-crawl'
    parse_spider = ParseSpiderCampusLodge()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
