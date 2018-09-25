from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLiveBeechMorganTown(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-morgantown'
    allowed_domains = [
        'copperbeechmorgantown.prospectportal.com',
        'livecbeechmorgantown.com'
    ]

    login_domain = 'https://copperbeechmorgantown.prospectportal.com/'
    site_domain = 'http://livecbeechmorgantown.com/'

    property_name = 'Copper Beech at Morgantown'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLiveBeechMorganTown(PPBaseParseSpiderE, MixinLiveBeechMorganTown):
    name = MixinLiveBeechMorganTown.name + '-parse'
    room_types_map = [('standard', 'Standard'), ('handicap', 'Handicap')]

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', ',')
        for l_room_type, room_type in self.room_types_map:
            if l_room_type in name[0]:
                return f"{room_name} {room_type}"
        return room_name


class CrawlSpiderLiveBeechMorganTown(MixinLiveBeechMorganTown, PPBaseCrawlSpiderE):
    name = MixinLiveBeechMorganTown.name + '-crawl'
    parse_spider = ParseSpiderLiveBeechMorganTown()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
