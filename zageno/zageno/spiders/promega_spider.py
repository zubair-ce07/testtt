import re
import json

from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from ..items import ZagenoItem


class PromegaSpider(CrawlSpider):
    name = 'promega'
    start_url_t = 'https://worldwide.promega.com/services/setCountry.ashx?countryid={c_id}&lang=en'
    visited_items = set()
    locals = {
        'us': {'country': 'US', 'currency': 'USD', 'id': '652656BA-E9B6-46B1-B2D7-1E671B00AA13'},
        'gb': {'country': 'UK', 'currency': 'GBP', 'id': '2810AC0F-3656-467A-9241-7E687FC59876'},
        'de': {'country': 'DE', 'currency': 'EUR', 'id': 'A59EB38A-7E99-4EE3-93CD-2288894DBE00'},
    }

    rules = (
        Rule(LinkExtractor(restrict_css='div[data-promega-nav-flyout="products"]')),
        Rule(LinkExtractor(restrict_css='.group-tile'), callback='parse_pagination', follow=True),
        Rule(LinkExtractor(restrict_css='.product-tile', unique=False), callback='parse_item'),
    )

    def start_requests(self):
        c_id = self.locals[self.country]['id']
        yield Request(
            self.start_url_t.format(c_id=c_id),
            callback=self.parse_listing
        )

    def parse_listing(self, response):
        yield Request('https://www.promega.com/')

    def parse_pagination(self, response):
        page_size = 15
        pagination_url_t = 'https://www.promega.com/services/products.ashx?group={p_id}&index={s_idx}&count=15'
        total_count = response.css('.group__filter-product-count span::text').extract_first()
        p_id = response.css('meta[name="itemId"]::attr(content)').extract_first()[1:-1]
        total_pages = int(total_count) // page_size + 1
        for p_no in range(1, total_pages):
            url = pagination_url_t.format(p_id=p_id, s_idx=page_size * p_no)
            yield Request(url, callback=self.parse_pagination_item)

    def parse_pagination_item(self, response):
        urls = re.findall('url":"(.+?)"', response.text)
        for url in urls:
            yield Request(url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        p_id = response.css('meta[name="itemId"]::attr(content)').extract_first()[1:-1]
        if self.is_visited(p_id):
            return

        product = ZagenoItem()
        # Product_Table
        product_table = {}
        product_table['id'] = p_id
        product_table['product_name'] = self.product_name(response)
        product_table['description'] = self.product_description(response)
        product_table['attributes'] = self.product_attributes(response)
        product_table['brand'] = 'promega'
        product_table['categories'] = self.product_categories(response)
        product_table['url'] = response.url
        product_table['product_image'] = self.product_product_image(response)
        product['product_table'] = product_table

        # Price_Table
        product['price_table'] = self.product_prices(response, product_table['id'])

        # Resource_Table
        safety_docs = self.product_safety_doc(response, product_table['id'])
        brochure_docs = self.product_brochure_doc(response, product_table['id'])
        product['resource_table'] = safety_docs + brochure_docs
        return self.parse_publication_doc(response, product)

    def parse_publication_doc(self, response, product):
        publication_url = response.xpath('//a[(contains(text(),"See all citations"))]/@href').extract_first()
        return Request(response.urljoin(publication_url), meta={'product': product}, callback=self.publication_doc)

    def product_categories(self, response):
        return ";;".join(response.css('.breadcrumb-nav a::text').extract()[2:])

    def product_name(self, response):
        name = response.css('h1[itemprop="name"] ::text').extract_first()
        return self.clean(name) if name else ''

    def product_attributes(self, response):
        attr_description = "# " + " ".join(response.css('.product-details-block h2::text').extract())
        attributes = " ".join([" * " + s for s in response.css('.product-details-block li::text').extract()])
        return json.dumps({'sub_description': attr_description + attributes})

    def product_product_image(self, response):
        img_url = response.css('.product-media img ::attr(src)').extract()
        return 'https://www.promega.com' + "".join(img_url) if img_url else ''

    def product_prices(self, response, p_id):
        prices = []
        price_values = response.css('.product-purchase__valid-catalog-numbers::attr(value)').extract_first()
        if not price_values:
            return {'product_id': p_id}
        json_prices = json.loads(price_values)
        for j_price in json_prices:
            p_dict = {}
            m_sku = j_price.get('catNum')
            p_list = j_price.get('listPrice')
            p_dict['product_id'] = p_id
            p_dict['currency'] = self.locals[self.country]['currency']
            p_dict['country'] = self.locals[self.country]['country']
            p_dict['content'] = self.product_content(response, m_sku)
            p_dict['manufacturer_sku'] = m_sku
            p_dict['price'] = "".join(re.findall('\d+', p_list)) if p_list else 'Please Enquire'
            p_dict['size'] = response.css('input[value={val}] ~ span ::text'.format(val=m_sku)).extract_first()
            prices.append(p_dict)
        return prices

    def product_content(self, response, m_sku):
        result = []
        content_css = 'section[data-catalog-number="{m_sku}"] .content-item tbody tr'
        for tr in response.css(content_css.format(m_sku=m_sku)):
            content = [" ".join(td.css('::text').extract()).strip() for idx, td in enumerate(tr.css('td')) if
                       idx in [0, 2, 3]]
            result.append(", ".join(self.clean(content)))
        return ";;".join(result).replace("View Product", "")

    def product_description(self, response):
        return " ".join(self.clean(response.css('.col--nucleus-2-3 .content-item ::text').extract()))

    def product_brochure_doc(self, response, p_id):
        brochure_docs = []
        selector_b = response.xpath('//h3[contains(text(), "Articles")]/following::div[1]//a')
        for s in selector_b:
            doc = {}
            doc['url'] = "".join(s.xpath('@href').extract())
            doc['title'] = "".join(s.xpath('text()').extract())
            doc['type'] = 'brochure'
            doc['product_id'] = p_id
            brochure_docs.append(doc)
        return brochure_docs

    def publication_doc(self, response):
        product = response.meta['product']
        publication_docs = []
        selector_p = response.css('.result')
        for s in selector_p:
            doc = {}
            doc['title'] = "".join(self.clean("".join(s.css('.resultTitle ::text').extract())))
            doc['author'] = "".join(self.clean("".join(s.css('.citationsAuthor ::text').extract())))
            doc['url'] = "".join(s.css('a[target]::attr(href)').extract())
            doc['type'] = 'publication'
            doc['product_id'] = product['product_table']['id']
            publication_docs.append(doc)
        product['resource_table'] += publication_docs
        [d.update({'id': idx}) for idx, d in enumerate(product['resource_table'], start=1)]
        return product

    def product_safety_doc(self, response, p_id):
        sds_docs = []
        temp = 'https://www.promega.com/-/media/files/resources{file}.pdf?la=en-us'
        files = response.css('.specifications__sds-link::attr(href)').extract()
        for f in files:
            doc = {}
            file_url = temp.format(file="".join(re.findall('resources(.+)\/', f)))
            doc['url'] = file_url.replace("/msdss", "")
            doc['title'] = 'SDS'
            doc['type'] = 'safety'
            doc['product_id'] = p_id
            sds_docs.append(doc)
        return sds_docs

    def is_visited(self, item_id):
        if item_id in self.visited_items:
            return True
        self.visited_items.add(item_id)
        return False

    def clean(self, to_clean):
        if isinstance(to_clean, str):
            return re.sub('\s+', ' ', to_clean).strip()
        return [re.sub('\s+', ' ', d).strip() for d in to_clean if d.strip()]
