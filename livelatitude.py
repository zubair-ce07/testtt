from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLatitude(BaseMixinPPE):
    name = property_slug = 'latitude-champaign'
    allowed_domains = [
        'latitude.prospectportal.com',
        'livelatitude.com'
    ]

    login_domain = 'https://latitude.prospectportal.com/'
    site_domain = 'http://livelatitude.com/'

    property_name = 'Latitude'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLatitude(PPBaseParseSpiderE, MixinLatitude):
    name = MixinLatitude.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('room', '')
        if "0 Bed" in room_name:
            return f"{name}-Studio"
        return f"{name} {room_name}"


class CrawlSpiderLatitude(MixinLatitude, PPBaseCrawlSpiderE):
    name = MixinLatitude.name + '-crawl'
    parse_spider = ParseSpiderLatitude()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
