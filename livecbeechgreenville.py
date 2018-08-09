from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLiveBeechGreenville(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-greenville'
    allowed_domains = [
        'copperbeechgreenville.prospectportal.com',
        'livecbeechgreenville.com'
    ]

    login_domain = 'https://copperbeechgreenville.prospectportal.com/'
    site_domain = 'http://livecbeechgreenville.com/'

    property_name = 'Copper Beech at Greenville'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLiveBeechGreenville(PPBaseParseSpiderE, MixinLiveBeechGreenville):
    name = MixinLiveBeechGreenville.name + '-parse'
    room_types_map = [('standard', 'Standard'), ('handicap', 'Handicap')]

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        for l_room_type, room_type in self.room_types_map:
            if l_room_type in name[0]:
                return f"{room_name} {room_type}"
        return room_name


class CrawlSpiderLiveBeechGreenville(MixinLiveBeechGreenville, PPBaseCrawlSpiderE):
    name = MixinLiveBeechGreenville.name + '-crawl'
    parse_spider = ParseSpiderLiveBeechGreenville()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
