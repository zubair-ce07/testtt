import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinForumTallahassee(BaseMixinPPE):
    name = property_slug = 'forum-tallahassee'
    allowed_domains = [
        'forumtallahassee.prospectportal.com',
        'forumtallahasseeapts.com'
    ]

    login_domain = 'https://forumtallahassee.prospectportal.com/'
    site_domain = 'http://forumtallahasseeapts.com/'

    property_name = 'Forum Tallahassee'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderForumTallahassee(PPBaseParseSpiderE, MixinForumTallahassee):
    name = MixinForumTallahassee.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))
        name = name[0].replace('-', '')
        room_name = clean(c_sel.css('.sub-title ::text'))
        room_name = room_name[0].replace('/', '')
        if "0 Bedroom" in room_name:
            return f"Studio {name}"
        return f"{room_name} {name}"


class CrawlSpiderForumTallahassee(MixinForumTallahassee, PPBaseCrawlSpiderE):
    name = MixinForumTallahassee.name + '-crawl'
    parse_spider = ParseSpiderForumTallahassee()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
