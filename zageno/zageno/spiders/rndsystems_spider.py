import re
import json

from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from ..items import ZagenoItem


class RndsystemsSpider(CrawlSpider):
    name = 'rndsystems'
    start_url_t = 'https://www.rndsystems.com/internationalization/set/{country}'

    visited_items = set()
    locals = {'us': {'country': 'US', 'currency': 'USD', 'c_sign': '$'},
              'gb': {'country': 'GB', 'currency': 'GBP', 'c_sign': '£'},
              'de': {'country': 'DE', 'currency': 'EUR', 'c_sign': '€'},
              }

    rules = (
        Rule(LinkExtractor(restrict_css='.field-item ul li a', allow='products/')),
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class, "field-item")]//table[not(@class)]//td/a')),
        Rule(LinkExtractor(
            restrict_css=['td a', '.field-items .grid_3 a', '.field-item ul li a', 'a[rel="next"]', '.orange_button'],
            allow='search')
        ),
        Rule(LinkExtractor(
            restrict_css=['.rnd-commonname-block .colwidea a', '.ecommerce_link', 'table td a', 'blockquote a'],
            allow='product',
            deny='search'
        ), callback='parse_item'),
    )

    def start_requests(self):
        country = self.locals[self.country]['country']
        yield Request(
            self.start_url_t.format(country=country),
            method='POST',
            callback=self.parse_internationalization
        )

    def parse_internationalization(self, response):
        yield Request(
            'https://www.rndsystems.com/internationalization/topbarinfo',
            method='POST',
            callback=self.parse_listing)

    def parse_listing(self, response):
        yield Request('https://www.rndsystems.com/products')

    def parse_item(self, response):
        p_id = response.css('.ds_details .add-to-cart::attr(data-catnum)').extract_first()
        if not p_id or self.is_visited(p_id):
            return
        product = ZagenoItem()
        # Product_Table
        product_table = {}
        product_table['id'] = p_id
        product_table['product_name'] = self.product_name(response)
        product_table['description'] = self.product_description(response)
        product_table['attributes'] = self.product_attributes(response)
        product_table['brand'] = 'R&D SYSTEMS'
        product_table['categories'] = self.product_categories(response)
        product_table['url'] = response.url
        product_table['product_image'] = self.product_product_image(response)
        product['product_table'] = product_table
        # Price_Table
        product['price_table'] = self.product_prices(response, product_table['id'])
        # Resource_Table
        product['resource_table'] = self.product_resourse_files(response, product_table['id'])
        return product

    def product_resourse_files(self, response, p_id):
        types = {'Product Datasheet': 'handbook', 'SDS': 'safety', 'COA': 'article'}
        resourse_files = []
        files_selector = response.css('.ds_document_row a')
        for f_id, f_selector in enumerate(files_selector, start=1):
            file = {}
            file['id'] = f_id
            file['product_id'] = p_id
            file['title'] = "".join(f_selector.css('.ds_pdfData::text').extract()).strip()
            file['type'] = types.get(file['title'], '')
            url = "".join(f_selector.css('::attr(href)').extract())
            file['url'] = 'https:' + url if url else response.url
            resourse_files.append(file)
        s_idx = len(resourse_files) + 1
        return resourse_files + self.publication_files(response, p_id, s_idx)

    def publication_files(self, response, p_id, s_idx):
        p_files = []
        files_selector = response.css('ol#citations li')
        for f_id, f_selector in enumerate(files_selector, start=s_idx):
            file = {}
            file['id'] = f_id
            file['product_id'] = p_id
            file['url'] = "".join(f_selector.css('a::attr(href)').extract())
            file['title'] = "".join(f_selector.css('a::text').extract())
            file['type'] = 'publication'
            file['authors'] = "".join(f_selector.xpath('br/following-sibling::text()').extract())
            p_files.append(file)
        return p_files

    def product_categories(self, response):
        return ";;".join(response.css('.breadcrumb a::text').extract()[1:])

    def product_name(self, response):
        return self.clean("".join(response.css('.ds_blueHeader ::text').extract()))

    def product_attributes(self, response):
        attributes = {}
        attr_selector = response.css('ul[class="ds_details"] li')
        for s in attr_selector:
            key = "".join(s.css('.item ::text').extract()).strip()
            if not key:
                continue
            attributes[key] = "".join(s.css('.value ::text').extract())
        sub_description = self.clean("".join(response.css('.ds_textPad ::text').extract()))
        if sub_description:
            attributes['sub_description'] = sub_description
        return json.dumps(attributes)

    def product_product_image(self, response):
        img_urls = response.css('.larger_view::attr(href)').extract()
        return ['https:' + url for url in img_urls]

    def product_prices(self, response, p_id):
        prices = []
        skus_ids = set()
        c_sign = self.locals[self.country]['c_sign']
        price_selector = response.css('.sticky-enabled tbody tr')
        for p_selector in price_selector:
            manufacturer_sku = "".join(p_selector.css('td .atc_catnum::text').extract())
            price = "".join(p_selector.css('td .price::text').extract())
            if (price and c_sign not in price) or manufacturer_sku in skus_ids:
                continue
            price_map = {}
            price_map['currency'] = self.locals[self.country]['currency']
            price_map['country'] = self.locals[self.country]['country']
            price_map['manufacturer_sku'] = manufacturer_sku
            price_map['size'] = "".join(p_selector.css('td .atc_size::text').extract())
            price_map['price'] = "".join(re.findall('\d+', price)) if price else 'Please Enquire'
            prices.append(price_map)
            skus_ids.add(price_map['manufacturer_sku'])
        return prices

    def product_content(self, response, m_sku):
        result = []
        content_css = 'section[data-catalog-number="{m_sku}"] .content-item tbody tr'
        for tr in response.css(content_css.format(m_sku=m_sku)):
            content = [" ".join(td.css('::text').extract()).strip() for idx, td in enumerate(tr.css('td'))
                       if idx in [0, 2, 3]]
            result.append(", ".join(self.clean(content)))
        return ";;".join(result).replace("View Product", "")

    def product_description(self, response):
        description_css = "//div[(text()= 'Product Summary')]/following::div[1]//text()"
        return " ".join(self.clean(response.xpath(description_css).extract()))

    def is_visited(self, item_id):
        if item_id in self.visited_items:
            return True
        self.visited_items.add(item_id)
        return False

    def clean(self, to_clean):
        if isinstance(to_clean, str):
            return re.sub('\s+', ' ', to_clean).strip()
        return [re.sub('\s+', ' ', d).strip() for d in to_clean if d.strip()]
