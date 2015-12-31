# -*- coding: utf-8 -*-
import re, json, urlparse, itertools
from urllib import quote
import math
from base import BaseParseSpider, BaseCrawlSpider, clean, reset_cookies, CurrencyParser
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.url import url_query_cleaner
from scrapy.link import Link
from w3lib.url import add_or_replace_parameter

# Site will eventually ban spider on concurrent requests. Ban takes some time to expire.


class Mixin(object):
    retailer = 'flipkart-in'
    market = 'IN'
    allowed_domains = ['www.flipkart.com']
    menu_url = 'http://www.flipkart.com/xhr/getNewMenuHtml'


class FlipkartParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    price_x = '(//div[@itemprop="offers"])[1]//span[contains(@class, "price")]/text()'

    care_keys = ('Fabric', 'Material', 'Outer Material', 'Care', 'Fabric Care',
                 'Machine Washable')

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        try:
            sku_id = self.product_id(response.url)
        except IndexError:
            self.log('Not a product page %s' % response.url)
            return

        garment = self.new_unique_garment(sku_id)
        if garment is None:
            return

        # Checking for the 'coming soon' and 'back to product information' tags
        xpath = '//div[@class="coming-soon"]| //div[@class="productxseller"]/div[@class="line"]|'\
                    '/a[contains(text(),"Back to Product Information")]'

        if hxs.select(xpath):
            return

        self.boilerplate_normal(garment, hxs, response)

        reviews = self.product_reviews(hxs)
        if reviews:
            garment['number_of_reviews'], garment['review_score'] = reviews

        if not self.out_of_stock(hxs):
            garment['skus'] = self.skus(hxs, sku_id)
        else:
            garment['out_of_stock'] = True

        garment['image_urls'] = self.image_urls(hxs)

        return garment

    def product_id(self, url):
        return urlparse.urlsplit(url).path.split('/p/')[1]

    def out_of_stock(self, hxs):
        xpath = '//div[@data-evar14="Permanently Discontinued"]|'\
                '//div[@data-evar14="No Sellers Available"]|'\
                '//div[@class="out-of-stock-status"]'

        return bool(hxs.select(xpath))

    def raw_name(self, hxs):
        xpath = '//div//h1[@class="title"]/text()'
        result = clean(hxs.select(xpath))
        if result:
            return result[0]
        else:
            return

    def product_name(self, hxs):
        regex = '^%s\s+' % self.product_brand(hxs)
        return re.sub(regex, '', self.raw_name(hxs), flags=re.I | re.U)

    def product_brand(self, hxs):
        return (hxs.select('//div/@data-prop41').extract() or ['Flipkart'])[0]

    def product_category(self, hxs):
        xpath = '//div[contains(@data-tracking-id, "product_breadCrumbs")]//a/text()'
        return clean(hxs.select(xpath))[1:]

    def raw_description(self, hxs):
        soup = []

        xpath = '//div[starts-with(@class, "productSpecs")]//table[@class="specTable"]'\
            '[not(contains(.//th/text(), "installation_details"))]//tr[td]'

        for s in hxs.select(xpath):
            key = clean(s.select('td[1]/text()'))
            if key:
                key = key[0]
            else:
                key = s.select('(ancestor::table)[1]//th/text()').extract()[0]

            value = clean(s.select('td[2]/text()'))
            if value:
                value = value[0]
            else:
                value = key
                key = s.select('(ancestor::table)[1]//th/text()').extract()[0]

            soup += [(key, value)]

        return soup

    def product_description(self, hxs):
        xpath = '//div[contains(@class, "description-text")]//text()'

        part1 = itertools.takewhile(lambda x: x != 'Footwear Care', clean(hxs.select(xpath)))

        part2 = ['%s: %s' % x for x in self.raw_description(hxs) if x[0] not in self.care_keys]
        return list(part1) + part2

    def product_care(self, hxs):
        part1 = ['%s: %s' % x for x in self.raw_description(hxs) if x[0] in self.care_keys]

        xpath = '//div[contains(@class, "description-text")]/'\
            'p[strong="Footwear care"]/following-sibling::p//text()'

        part2 = clean(hxs.select(xpath))

        return part1 + part2

    def skus(self, hxs, product_id):
        # regretfully OOS sizes have no pid associated with them,
        # forcing to use composite ids
        skus = {}

        xpath = '//div[contains(@class, "shipping-details")][contains(span, "discontin")]'
        global_oos = bool(hxs.select(xpath))

        previous_price, price, currency = self.product_pricing(hxs)

        xpath = '//div[contains(@class, "selected") or contains(@class, "-disabled")]/'\
                    'div[contains(@class, "paletteImage")]/@data-selectorvalue'

        colour = (hxs.select(xpath).extract() or [''])[0]

        xpath = '//div[contains(div/text(), "Select Size")]//div[div/@data-selectorvalue]'
        size_selectors = hxs.select(xpath)

        for s_s in size_selectors:
            raw_size = s_s.select('div/@data-selectorvalue').extract()[0]

            sku_id = ('%s|%s|%s' % (product_id, colour, raw_size)).replace('.', '_')
            skus[sku_id] = sku = dict(colour=colour, price=price, currency=currency)

            sku['size'] = raw_size

            if previous_price:
                sku['previous_price'] = previous_price

            if global_oos or s_s.select('self::*[contains(@class, "selector-disabled")]'):
                sku['out_of_stock'] = True

        if not size_selectors:
            skus[product_id] = sku = dict(size=self.one_size, colour=colour,
                                          price=price, currency=currency)
            if previous_price:
                sku['previous_price'] = previous_price

            if global_oos:
                sku['out_of_stock'] = True

        return skus

    def image_urls(self, hxs):
        images = []

        xpath = '//div[@class="mainImage"]/div[@class="imgWrapper"]//img[@data-src]'
        for i_s in hxs.select(xpath):
            # not all images have zoom version
            images += (i_s.select('@data-zoomimage') or i_s.select('@data-src')).extract()

        return images

    def product_reviews(self, hxs):
        xpath = '//div[@itemprop="aggregateRating"]//span[@itemprop="ratingCount"]/text()'
        count = clean(hxs.select(xpath))

        if count:
            xpath = '//div[@itemprop="aggregateRating"]//meta[@itemprop="ratingValue"]/@content'
            value = hxs.select(xpath).extract()
            return (int(count[0]), round(float(value[0]), 2))


def clean_url(url):
    return url_query_cleaner(url, ('start', 'sid', 'p%5B%5D', 'p[]'))

# Workaround for fragile and limited pagination chain. Site limits listings to 1500 items.
class WorkaroundLE(object):
    PAGE_SIZE = 15

    def extract_links(self, response):
        if 'start=' in response.url:
            return []

        hxs = HtmlXPathSelector(response)
        raw = hxs.select('//div[@id="searchCount"]/span[@class="items"]/text()').extract()

        try:
            total = int(re.sub('[^\d]', '', raw[0]))
        except (IndexError, ValueError):
            return []

        links = []
        base_url = clean_url(response.url)

        if total <= 100*self.PAGE_SIZE:
            for start in xrange(self.PAGE_SIZE, total + 1, self.PAGE_SIZE):
                url = add_or_replace_parameter(base_url, 'start', str(start + 1))
                links.append(Link(url, str(start // self.PAGE_SIZE + 1)))
        else:
            if 'facets.brand' in response.url:
                # not much could be done if brands trick is not sufficient.
                # Just taking our 1500 items

                for start in xrange(self.PAGE_SIZE, total + 1, 100*self.PAGE_SIZE + 1):
                    url = add_or_replace_parameter(base_url, 'start', str(start + 1))
                    links.append(Link(url, str(start // self.PAGE_SIZE + 1)))
                    return links

            for li_s in hxs.select('//ul[@id="brand"]/li'):
                facet = li_s.select('.//input/@value').extract()[0]
                brand = li_s.select('@title').extract()[0]

                url = base_url + '&p[]=' + quote(facet)
                links.append(Link(url, brand))

        return links


class FlipkartCrawlSpider(BaseCrawlSpider, Mixin):
    name = Mixin.retailer + '-crawl'
    parse_spider = FlipkartParseSpider()
    download_delay = .5 # 403 is lurking around the corner, raise delay if needed.

    men_x = '//div[@id="menu-men-tab-0-content"]'
    women_x = '//div[@id="menu-women-tab-0-content"]'

    cat_x_t = '//div[@id="menu-baby-kids-tab-0-content"]/ul[position()<4]/li'\
        '//a[starts-with(@data-tracking-id, "%s")]'

    boys_x = [cat_x_t % x for x in ('0_Boys', '0_For Boys')]
    girls_x = [cat_x_t % x for x in ('0_Girls', '0_For Girls')]

    unisex_kids_x = [cat_x_t % x for x in ('0_For Baby Girls', '0_For Baby Boys')]

    homeware_x = '//div[@id="menu-home-kitchen-tab-0-content"]'

    navigation_x = '//div[starts-with(@class, "category-links")]'

    products_x = '//div[@id="products"]'

    le_args = {'process_value': clean_url, 'canonicalize': False}

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=men_x, **le_args),
             process_request=reset_cookies, callback='parse_and_add_men'),

        Rule(SgmlLinkExtractor(restrict_xpaths=women_x, **le_args),
             process_request=reset_cookies, callback='parse_and_add_women'),

        Rule(SgmlLinkExtractor(restrict_xpaths=boys_x, deny=['Games', '/toys/'], **le_args),
             process_request=reset_cookies, callback='parse_and_add_boys'),

        Rule(SgmlLinkExtractor(restrict_xpaths=girls_x, deny=['Games', '/toys/'], **le_args),
             process_request=reset_cookies, callback='parse_and_add_girls'),

        Rule(SgmlLinkExtractor(restrict_xpaths=unisex_kids_x, deny=['Games', '/toys/'], **le_args),
             process_request=reset_cookies, callback='parse_and_add_unisex_kids'),

        Rule(SgmlLinkExtractor(restrict_xpaths=homeware_x, deny=['Irons'], **le_args),
             process_request=reset_cookies, callback='parse_and_add_homeware'),

        Rule(SgmlLinkExtractor(restrict_xpaths=navigation_x, **le_args),
             process_request=reset_cookies, callback='parse'),

        Rule(WorkaroundLE(), process_request=reset_cookies, callback='parse'),

        Rule(SgmlLinkExtractor(restrict_xpaths=products_x, process_value=url_query_cleaner),
             process_request=reset_cookies, callback='parse_item')
    )

    def parse_menu(self, response):
        data = json.loads(response.body)

        results = []
        for menu_snippet in data.itervalues():
            menu_response = response.replace(body=self.html_t % menu_snippet)
            results += list(self.parse(menu_response))

        return results

    def start_requests(self):
        yield Request(self.menu_url, callback=self.parse_menu)


# -------------------------------------- #
'''
Use these as start_urls
# Lifestyle/Men
http://mobileapi.flipkart.net/2/discover/getSearch?store=2oq/s9b&start=0&count=10&disableMultipleImage=true&ads-offset=1&valid=true

Lifestyle/Women
http://mobileapi.flipkart.net/2/discover/getSearch?store=2oq/c1r&start=0&count=10&disableMultipleImage=true&ads-offset=1&valid=true

Lifestyle/Kids
http://mobileapi.flipkart.net/2/discover/getSearch?store=2oq/mpf&start=0&count=10&disableMultipleImage=true&ads-offset=1&valid=true

Lifestyle/Baby/Infant Wear
http://mobileapi.flipkart.net/2/discover/getSearch?store=kyh/mjf&start=0&count=10&disableMultipleImage=true&ads-offset=1&valid=true
'''


class MixinM(object):
    retailer = 'flipkartmobile-in'
    market = 'IN'
    allowed_domains = ['mobileapi.flipkart.net']
    user_agent = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 FKUA/Retail/610200/Android/Mobile (LGE/Nexus 4/b5b0e5deeda257b47cbd8940a387493c)'


class FlipkartMobileParseSpider(BaseParseSpider, MixinM):
    name = MixinM.retailer + '-parse'

    def parse(self, response):
        product = json.loads(response.body)['RESPONSE']['productInfo'].values()[0]

        sku_id = self.product_id(product)
        garment = self.new_unique_garment(sku_id)
        if not garment:
            return

        self.boilerplate_minimal(garment, response)
        garment['brand'] = product['marketplace'][0]['seller.displayName']
        garment['url_original'] = response.url
        garment['name'] = product['mainTitle']
        garment['description'] = self.product_description(product)
        garment['care'] = self.product_care(product)
        garment['category'] = self.product_category(product)
        garment['gender'] = self.product_gender(garment)
        garment['image_urls'] = self.image_urls(product)
        garment['skus'] = self.skus(product)

        return garment

    def product_id(self, product):
        return product['productId']

    def product_gender(self, garment):
        category_l = [x.lower() for x in garment['category']]
        name_l = garment['name'].lower()

        if any(['women' in x for x in category_l]) or 'women' in name_l:
            return 'women'
        if any(['men' in x for x in category_l]) or 'men' in name_l:
            return 'men'
        if any(['girl' in x for x in category_l]) or 'girl' in name_l:
            return 'girls'
        if any(['boy' in x for x in category_l]) or 'boy' in name_l:
            return 'boys'
        if any(['kid' in x for x in category_l]) or 'kid' in name_l:
            return 'unisex-kids'

    def product_category(self, product):
        return list(set(product['omnitureData'].values()))

    def raw_description(self, product):
        desc = (product['productDescription']['product.description.text'] or '').split('. ')
        for d in product['productSpecification']:
            desc.extend([k + ': ' + v for k, v in d['value'].iteritems()])

        return clean(desc)

    def product_description(self, product):
        return [x.lstrip(': ') for x in self.raw_description(product) if not self.care_criteria(x) and 'Fabric:' not in x]

    def product_care(self, product):
        return [x.lstrip(': ') for x in self.raw_description(product) if self.care_criteria(x) or 'Fabric:' in x]

    def skus(self, product):
        skus = {}
        currency = 'INR'
        previous_price = product['mrp']
        price = product['sellingPrice']

        if previous_price != price:
            previous_price = CurrencyParser.float_conversion(previous_price)
            price = CurrencyParser.float_conversion(price)
        else:
            price = CurrencyParser.float_conversion(previous_price)
            previous_price = None

        if product['swatch']:
            color = product['swatch'].get('color', {}).get('product.swatch.value')
            for size, info in product['swatch']['size']['product.swatch.about'].iteritems():
                sku = {
                    'currency': currency,
                    'size': size if size != 'Free' else self.one_size,
                    'out_of_stock': not info['isAvailable'],
                    'price': price
                }

                if color:
                    sku['colour'] = color

                if previous_price:
                    sku['previous_prices'] = [previous_price]

                skus[color + '_' + size if color else size] = sku
        else:
            # Color is not available in this case
            sku = {
                'currency': currency,
                'size': clean(product.get('checkoutSubTitle', self.one_size).replace('Size:', '')),
                'out_of_stock': not product['availabilityDetails']['product.availability.status'] == 'In Stock.',
                'price': price
            }
            if previous_price:
                sku['previous_prices'] = [previous_price]

            skus[sku['size']] = sku

        return skus

    def image_urls(self, product):
        images = []
        for u in product['dynamicImageUrl'].values():
            u = u.replace('{@width}/{@height}', '930/870').replace('q={@quality}', 'q=90')
            images.append(u)

        return images


class FlipkartMobileCrawlSpider(BaseCrawlSpider, MixinM):
    '''
    Under Women - we do not want to crawl "Safety"
    Under Kids - we do not want to crawl "Toys"
    Under Baby - the only category we want to crawl is "Infant Wear"

    We want to crawl Beauty & Wellness, but only the sections "Makeup", "Body and skin care", "Fragrances",
     "Men's Grooming", "Hair care", "Bath and spa" and "Beauty and Accessories"

    We want to crawl some sections under Home & Furniture, these are: "Furniture", "Home Furnishing" and "Home Decor"
     but all items to be marked as "homeware"
    '''
    name = MixinM.retailer + '-crawl'
    parse_spider = FlipkartMobileParseSpider()

    url_prefix = 'http://mobileapi.flipkart.net/2/discover'
    listing_url_t = url_prefix + '/getSearch?store=%s&start=0&count=10&disableMultipleImage=true&ads-offset=1&valid=true'
    product_url_t = url_prefix + '/productInfo/0?pids=%s&lids=%s&disableMultipleImage=true'

    def __init__(self, start_url):
        self.start_urls = [start_url]
        super(FlipkartMobileCrawlSpider, self).__init__()

    def parse(self, response):
        data = json.loads(response.body)

        # sub-categories
        if data['RESPONSE']['search']['storeMetaInfoList']:
            for category in data['RESPONSE']['search']['storeMetaInfoList']:
                url = self.listing_url_t % category['id']
                r = Request(url, meta={'trail': self.add_trail(response)})
                yield r
            return

        # paging
        if data['REQUEST']['params']['start'] == '0':
            total_products = data['RESPONSE']['search']['metadata']['totalProduct']
            default_page_size = 10
            total_pages = int(math.ceil(total_products * 1.0 / default_page_size * 1.0))

            for page_number in range(2, total_pages + 1):
                url = re.sub(r'start=\d+', 'start=' + str(page_number), response.url)
                yield Request(url, meta={'trail': self.add_trail(response)})

        # products list
        for product in data['RESPONSE']['product'].values():
            url = self.product_url_t % (product['productId'], product['preferredListingId'])
            yield Request(url, meta={'trail': self.add_trail(response)}, callback=self.parse_spider.parse)

    def add_trail(self, response):
        trail_part = [(response.meta.get('link_text', ''), response.url)]
        return response.meta.get('trail', []) + trail_part
