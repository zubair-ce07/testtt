from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLiveRadford(BaseMixinPPE):
    name = property_slug = 'copper-beech-at-radford'
    allowed_domains = [
        'copperbeechradford.prospectportal.com',
        'livecbeechradford.com'
    ]

    login_domain = 'https://copperbeechradford.prospectportal.com/'
    site_domain = 'http://livecbeechradford.com/'

    property_name = 'Copper Beech at Radford'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLiveRadford(PPBaseParseSpiderE, MixinLiveRadford):
    name = MixinLiveRadford.name + '-parse'
    room_name_map = [
        ('Garden', 'garden'),
        ('Standard', 'standard'),
        ('Chateau', 'chateau'),
        ('Duplex', 'duplex'),
        ('Condo', 'condo')
    ]

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = clean(c_sel.css('.sub-title ::text'))
        for room, l_room in self.room_name_map:
            if l_room in name[0]:
                return f"{room_name[0]} {room}"
        return room_name[0]


class CrawlSpiderLiveRadford(MixinLiveRadford, PPBaseCrawlSpiderE):
    name = MixinLiveRadford.name + '-crawl'
    parse_spider = ParseSpiderLiveRadford()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
