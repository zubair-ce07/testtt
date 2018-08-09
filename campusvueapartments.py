import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusVue(BaseMixinPPE):
    name = property_slug = 'campus-vue'
    allowed_domains = [
        'campusvue.prospectportal.com',
        'campusvueapartments.com'
    ]

    login_domain = 'https://campusvue.prospectportal.com/'
    site_domain = 'https://campusvueapartments.com/'

    property_name = 'Campus Vue'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusVue(PPBaseParseSpiderE, MixinCampusVue):
    name = MixinCampusVue.name + '-parse'
    room_types_map = ['Standard', 'Large', 'Shared']

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        if re.search('(Studio)', name[0]):
            return name[0]
        if re.search('(Studio)|(\d+x\d+)', name[0]):
            room_name = clean(c_sel.css('.sub-title ::text'))
            room_name = room_name[0].replace('/', '|')
            for room_type in self.room_types_map:
                if room_type in name[0]:
                    return f"{room_name} {room_type}"
            return room_name
        return name[0]


class CrawlSpiderCampusVue(MixinCampusVue, PPBaseCrawlSpiderE):
    name = MixinCampusVue.name + '-crawl'
    parse_spider = ParseSpiderCampusVue()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
