import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinForumDenton(BaseMixinPPE):
    name = property_slug = 'forum-at-denton'
    allowed_domains = [
        'forumatdenton.prospectportal.com',
        'forumdenton.com'
    ]

    login_domain = 'https://forumatdenton.prospectportal.com/'
    site_domain = 'http://forumdenton.com/'

    property_name = 'Forum at Denton'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderForumDenton(PPBaseParseSpiderE, MixinForumDenton):
    name = MixinForumDenton.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        room_name = re.sub('(\d+)x(\d+)\s?(.?)', '\\1 Bedroom \\2 Bathroom \\3', name[0])
        if "0 Bedroom" in room_name:
            return "Studio"
        return room_name


class CrawlSpiderForumDenton(MixinForumDenton, PPBaseCrawlSpiderE):
    name = MixinForumDenton.name + '-crawl'
    parse_spider = ParseSpiderForumDenton()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
