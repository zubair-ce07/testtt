import copy
import json

from scrapy import Request, Spider
from ScrapyPractice.items import ProductItem, SizeItem, VariationItem


class StyleRunnerSpider(Spider):
    name = "SRspider"
    domain_url = "https://www.stylerunner.com"
    items = {}
    item_details_url = "https://www.stylerunner.com/api/items?country=AU&currency=AUD&fieldset=details&include" \
                       "=facets&language=en&url={}"

    def start_requests(self):
        start_url = 'https://www.stylerunner.com/?cur={}&'.format(self.cur)
        yield Request(start_url, callback=self.parse_navigations)

    def make_request(self, selectors, response):
        category_level_label = [sel.xpath("./a/text()").extract_first('').strip() for sel in selectors]
        url = selectors[-1].xpath("./a/@href").extract_first()
        meta = copy.deepcopy(response.meta)
        meta['category'] = category_level_label
        url = response.urljoin(url) + "?page=1"
        return Request(
            url=url,
            callback=self.parse_categories,
            meta=meta,
        )

    def parse_navigations(self, response):
        for level1 in response.xpath("//ul[@class='header-menu-level1']/li")[1:]:
            yield self.make_request([level1], response)

            for level2 in level1.xpath("./ul/li/ul/li"):
                yield self.make_request([level1, level2], response)

                for level3 in level2.xpath(".//ul/li"):
                    yield self.make_request([level1, level2, level3], response)

    def parse_categories(self, response):
        for item in response.css('.facets-item-cell-grid'):
            item_url = item.css('a::attr(href)').extract_first()
            if "Gift" in item_url:
                continue
            product = ProductItem(
                product_url=response.urljoin(item_url),
                store_keeping_unit=item.css('::attr(data-sku)').extract_first().split('-')[0],
                currency=self.cur,
                breadcrumbs=response.meta['category'],
            )
            if product['store_keeping_unit'] not in self.items.keys():
                self.items[product['store_keeping_unit']] = product
                yield Request(
                    url=self.item_details_url.format(item_url[1:]),
                    callback=self.parse_product,
                    meta={'product': product},
                    dont_filter=True,
                )

        for req in self.parse_pagination(response):
            yield req

    def parse_pagination(self, response):
        next_page = response.xpath("//link[@rel='next']/@href").extract_first()
        if next_page:
            yield Request(
                url=next_page,
                callback=self.parse_categories,
                meta=response.meta,
                dont_filter=True
            )

    def parse_product(self, response):
        product = response.meta['product']
        details = json.loads(response.text)
        item = details.get("items", [])
        if not item:
            return
        item = item[0]

        product['brand'] = item.get("custitem_brand", '')
        product['title'] = item.get('displayname', '')
        product['locale'] = "en_AU"
        product['description'] = item.get("storedescription")
        product['variations'] = []

        response.meta['product'] = product
        response.meta['colors_left'] = []
        response.meta['colors_done'] = [item.get('itemid')]
        for request in self.color_info(response):
            yield request

    def color_info(self, response):
        details = json.loads(response.text)
        item = details.get("items", [])
        if not item:
            return
        item = item[0]
        product = response.meta['product']
        cur_colors = response.meta['colors_left']
        colors_done = response.meta['colors_done']

        product['variations'].append(
            VariationItem(
                display_color_name=item.get('custitem_item_colour', ''),
                images_urls=[image.get('url', '') for image in item['itemimages_detail'].get('urls', [])],
                sizes=self.size_info(item),
            )
        )

        other_colors = [clr for clr in item['custitem_related_items'].split(', ') if clr != '&nbsp;']
        if other_colors:
            other_colors = [color.split(' : ')[1].split(' ')[0] for color in other_colors]
            cur_colors.extend([clr for clr in other_colors if clr not in colors_done])

        if not cur_colors:
            yield product
            return

        next_color = cur_colors.pop()
        colors_done.append(next_color)
        next_color_url = response.url.replace(item.get('itemid', ''), next_color)
        response.meta['product'] = product
        response.meta['colors_left'] = cur_colors
        response.meta['colors_done'] = colors_done
        yield Request(
            url=next_color_url,
            callback=self.color_info,
            meta=response.meta,
            dont_filter=True,
        )

    def size_info(self, item):
        item_price = item['pricelevel7']
        sizes = item['matrixchilditems_detail']
        size_list = []

        for size in sizes:
            dis_price = size['onlinecustomerprice_detail']['onlinecustomerprice']
            is_discounted = True if dis_price < item_price else False
            size_list.append(
                SizeItem(
                    size_name=size['custitem1'],
                    is_available=size['ispurchasable'],
                    price=item_price,
                    is_discounted=is_discounted,
                    discounted_price=dis_price if is_discounted else '',
                )
            )

        return size_list
