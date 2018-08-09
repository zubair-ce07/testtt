import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinCampusVillage(BaseMixinPPE):
    name = property_slug = 'campus-village-at-college-station'
    allowed_domains = [
        'campusvillagecs.prospectportal.com',
        'campusvillageatcollegestation.com'
    ]

    login_domain = 'https://campusvillagecs.prospectportal.com/'
    site_domain = 'http://campusvillageatcollegestation.com/'

    property_name = 'Campus Village at College Station'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderCampusVillage(PPBaseParseSpiderE, MixinCampusVillage):
    name = MixinCampusVillage.name + '-parse'
    room_size_map = [
        ('Lg', 'Large'),
        ('Sm', 'Small')
    ]

    def room_name(self, response, c_sel, sel):
        room_types = clean(sel.css('.type-col ::text'))
        name = clean(c_sel.css('.title ::text'))
        if re.search('(Studio)|(\d+x\d+)', name[0]):
            room_name = clean(c_sel.css('.sub-title ::text'))
            room_name = room_name[0].replace('/', '|')
            return self.format_name(room_name, name[0], ' ')
        return self.format_name(name[0], room_types, ' - ')

    def format_name(self, name, r_types, sep):
        for size_code, size in self.room_size_map:
            if size_code in r_types:
                return f"{name} {size}"
        return name


class CrawlSpiderCampusVillage(MixinCampusVillage, PPBaseCrawlSpiderE):
    name = MixinCampusVillage.name + '-crawl'
    parse_spider = ParseSpiderCampusVillage()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
