import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinLakeview(BaseMixinPPE):
    name = property_slug = 'lakeview-apartments'
    allowed_domains = [
        'lakeviewseattleapts.prospectportal.com',
        'lakeviewudistrict.com'
    ]

    login_domain = 'https://lakeviewseattleapts.prospectportal.com/'
    site_domain = 'http://lakeviewudistrict.com/'

    property_name = 'Lakeview Apartments'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderLakeview(PPBaseParseSpiderE, MixinLakeview):
    name = MixinLakeview.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        name = re.findall('\w+\s\+\s\w+\s*(.*)', name)[0]
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return f"Studio {name}"
        return f"{room_name} {name}"


class CrawlSpiderLakeview(MixinLakeview, PPBaseCrawlSpiderE):
    name = MixinLakeview.name + '-crawl'
    parse_spider = ParseSpiderLakeview()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
