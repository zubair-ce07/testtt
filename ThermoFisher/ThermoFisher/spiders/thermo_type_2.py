import json
import re

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ThermoFisher.items import ThermoType2SpiderItem
from ThermoFisher.spiders import thermo_constants as constants

catalog_ids = []


class ThermoType2Spider(CrawlSpider):
    name = "thermo_type_2"
    download_delay = 2.0
    allowed_domains = ["thermofisher.com"]
    start_urls = [
        'https://www.thermofisher.com/pk/en/home/order.html',
        ]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=(constants.categories,)), callback="parse_categories"),
    )

    def parse_categories(self, response):
        p = LinkExtractor(allow=(), restrict_css=(constants.sub_categories,)).extract_links(response)
        for link in p:
            yield Request(link.url, callback=self.parse_lists)

    def parse_lists(self, response):
        if response.css(constants.is_parsable_list):
            if response.css(constants.list_type_identifier):
                requests = []
                links = LinkExtractor(allow=(), restrict_css=constants.list_type_2, ).extract_links(response)
                link_next = LinkExtractor(allow=(), restrict_css=constants.list_type_2_next, ).extract_links(response)
                for link in links:
                    requests.append(Request(link.url, callback=self.parse_items))
                for link in link_next:
                    requests.append(Request(link.url, callback=self.parse_lists))
                for request in requests:
                    yield request
            else:
                pass

    def parse_items(self, response):
        diff = response.css(constants.product_type).extract_first()
        if diff:
            if 'Details' in diff:
                pass
            elif 'overview' in diff:
                if not response.css(constants.product_type_2):
                    request = self.parse_overview_items(response)
                    yield request

    def parse_overview_items(self, response):
        c_id = response.css(constants.get_cid_2).extract_first()
        if c_id not in catalog_ids:
            catalog_ids.append(c_id)
            item = self.compile_overview_item(response)
            request = Request(constants.get_additional_info_url.format(c_id), callback=self.parse_additional_info)
            request.meta['c_id'] = c_id
            request.meta['item'] = item
            return request

    def parse_additional_info(self, response):
        products = json.loads(response.body.decode('utf-8'))
        item = response.meta['item']
        if 'message' in products:
            item['catalog_numbers'] = self.get_catalog_numbers(products)
            request = Request(constants.get_documents_info_url.format(response.meta['c_id']),
                              callback=self.parse_documents_info)
            request.meta['item'] = item
            yield request

    def parse_documents_info(self, response):
        document_info = json.loads(response.body.decode('utf-8'))
        item = response.meta['item']
        item['faqs'] = self.get_product_faqs(document_info)
        item['manuals_and_protocols'] = self.get_product_manuals(document_info)
        item['product_literature'] = self.get_product_brochures(document_info)
        item['coa'] = self.get_product_coas(document_info)
        yield item

    def compile_overview_item(self, response):
        item = ThermoType2SpiderItem()
        item['brand'] = self.get_brand(response)
        item['name'] = self.get_product_name(response)
        item['description'] = self.get_product_description(response)
        item['category'] = self.get_product_category(response)
        item['recommended_products'] = self.get_recommended_products(response)
        item['specifications'] = self.get_product_specifications(response)
        item['contents'] = self.get_product_contents(response)
        item['image_urls'] = self.get_product_images(response)
        item['related_applications'] = self.get_product_related_applications(response)
        item['url'] = response.url
        return item

    def get_catalog_numbers(self, products):
        catalog_numbers = []
        for product in products['products']:
            catalog_numbers.append({'catalog_number': product['sku'],
                                    'price': product['listPrice']['value'] if
                                    product['pricingAccess'] == "Orderable" else product['pricingAccess'],
                                    'unit_size': product['size']
                                    })
            if product['sku'] not in catalog_ids:
                catalog_ids.append(product['sku'])
        return catalog_numbers

    def get_product_name(self, response):
        return ''.join(response.css(constants.get_name_2).extract())

    def get_brand(self, response):
        return clean_str(response.css(constants.get_brand).extract_first())

    def get_product_description(self, response):
        return ''.join(list(filter(None, [x.strip() for x in response.css(
            constants.product_type_2_description).extract()]))[1:])

    def get_product_category(self, response):
        return list(filter(None, [x.strip() for x in response.css(constants.breadcrumbs_sel_2).extract()]))

    def get_recommended_products(self, response):
        if response.css(constants.product_type_2_recommended_products_check):
            recommended = []
            recommend_urls = response.css(constants.product_type_2_recommend_urls).extract()
            recommend_catalogs = response.css(constants.product_type_2_recommend_catalogs).extract()
            for i in range(0, len(recommend_catalogs)):
                recommended.append({'catalog_number': recommend_catalogs[i],
                                    'url': recommend_urls[i]
                                    })
            return recommended

    def get_product_specifications(self, response):
        if response.css(constants.product_type_2_specifications_check):
            specifications = {}
            spec_keys = [x.strip(':') for x in
                         response.css(constants.product_type_2_specifications_keys).extract()]
            spec_values = [x.strip() for x in
                           response.css(constants.product_type_2_specifications_vals).extract()]
            for i in range(0, len(spec_keys)):
                specifications.update({spec_keys[i]: spec_values[i]})
            return specifications

    def get_product_contents(self, response):
        if response.css(constants.product_type_2_contents_check):
            return ' '.join(list(
                filter(None, [x.strip() for x in response.css(constants.product_type_2_contents).extract()])))

    def get_product_images(self, response):
        return [response.css(constants.img_src_sel).extract_first()]

    def get_product_related_applications(self, response):
        return response.css(constants.product_type_2_related_apps).extract()

    def get_product_faqs(self, document_info):
        if 'faqList' in document_info['searchResults']:
            faq_list = []
            for faq in document_info['searchResults']['faqList']:
                faq_list.append({'question': faq['question'],
                                 'answer': re.sub(r'<.*?>', '', faq['answer'])})
            return faq_list

    def get_product_coas(self, document_info):
        if 'coaList' in document_info['searchResults']:
            coas = []
            for coa in document_info['searchResults']['coaList']:
                coas.append({'title': coa['lotNo'], 'url': coa['lotNoUrl']})
            return coas

    def get_product_brochures(self, document_info):
        if 'brochureList' in document_info['searchResults']:
            product_literatures = []
            for article in document_info['searchResults']['brochureList']:
                product_literatures.append({'title': article['title'], 'url': article['downloadUrl']})
            return product_literatures

    def get_product_manuals(self, document_info):
        if 'manualList' in document_info['searchResults']:
            manuals = []
            for manual in document_info['searchResults']['manualList']:
                manuals.append({'title': manual['title'], 'url': manual['titleUrl']})
            return manuals


def clean_str(input_str):
    if input_str:
        return str(re.sub('\s+', ' ', input_str.replace(u'\xa0', ' ')).strip())
