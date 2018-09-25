import re

from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinMarqueeOrlando(BaseMixinPPE):
    name = property_slug = 'marquee-orlando'
    allowed_domains = [
        'themarqueeapts.prospectportal.com',
        'marqueeorlando.com'
    ]

    login_domain = 'https://themarqueeapts.prospectportal.com/'
    site_domain = 'http://marqueeorlando.com/'

    property_name = 'Marquee Orlando'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderMarqueeOrlando(PPBaseParseSpiderE, MixinMarqueeOrlando):
    name = MixinMarqueeOrlando.name + '-parse'

    def room_name(self, response, c_sel, sel):
        name = clean(c_sel.css('.title ::text'))[0]
        room_name = clean(c_sel.css('.sub-title ::text'))[0]
        if "0 Bedroom" in room_name:
            return f"{name}-Studio"
        return f"{name}-{room_name}"


class CrawlSpiderMarqueeOrlando(MixinMarqueeOrlando, PPBaseCrawlSpiderE):
    name = MixinMarqueeOrlando.name + '-crawl'
    parse_spider = ParseSpiderMarqueeOrlando()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
