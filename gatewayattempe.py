from student.utils import clean
from .prospectportal_base import BaseMixinPPE
from .prospectportal_base import PPBaseCrawlSpiderE
from .prospectportal_base import PPBaseParseSpiderE


class MixinGatewayTempe(BaseMixinPPE):
    name = property_slug = 'gateway-at-tempe'
    allowed_domains = [
        'gatewayattempe.prospectportal.com',
        'gatewayattempe.com'
    ]

    login_domain = 'https://gatewayattempe.prospectportal.com/'
    site_domain = 'http://gatewayattempe.com/'

    property_name = 'Gateway at Tempe'
    landlord_name = 'Asset Campus Housing'


class ParseSpiderGatewayTempe(PPBaseParseSpiderE, MixinGatewayTempe):
    name = MixinGatewayTempe.name + '-parse'

    def room_name(self, response, c_sel, sel):
        room_name = clean(c_sel.css('.sub-title ::text'))
        if "0 Bedroom" in room_name:
            return f"Studio {name}"
        return room_name[0]


class CrawlSpiderGatewayTempe(MixinGatewayTempe, PPBaseCrawlSpiderE):
    name = MixinGatewayTempe.name + '-crawl'
    parse_spider = ParseSpiderGatewayTempe()
    deal_x = '//*[contains(@class, "pane-entity-field ") and contains(., "Special")]//section//text()'
