import json
import re

from scrapy import Request, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ThermoFisher.items import ThermoType1Item
from ThermoFisher.spiders import thermo_constants as constants

catalog_ids = []


class ThermoType1Spider(CrawlSpider):
    name = "thermo_type_1"
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
                pass
            else:
                links = LinkExtractor(allow=(), restrict_css=constants.list_type_1, ).extract_links(response)
                requests = []
                for link in links:
                    yield Request(link.url, callback=self.parse_items)
                form_data = self.compile_form_data_list_type_1(response)
                total_hits = int(response.css(constants.list_1_total_hits).extract_first())
                step = 100 if 100 < total_hits else total_hits
                form_data['numHits'] = str(step)
                for offset in range(25, total_hits, step):
                    form_data['offset'] = str(offset)
                    request = FormRequest(url=constants.list_type_1_post_url, formdata=form_data,
                                          callback=self.parse_list_1_post_request)
                    request.meta['offset'] = str(offset)
                    yield request

                for request in requests:
                    yield request

    def parse_list_1_post_request(self, response):
        links = LinkExtractor(allow=(), restrict_css=constants.list_type_1, ).extract_links(response)
        for link in links:
            yield Request(link.url, callback=self.parse_items)

    def parse_items(self, response):
        diff = response.css(constants.product_type).extract_first()
        # diff identifies which type of product it is
        if diff:
            if 'Details' in diff:
                yield self.parse_type_1_items(response)
            elif 'overview' in diff:
                pass

    def parse_type_1_items(self, response):
        c_id = response.css(constants.get_cid_1).extract_first()
        if c_id not in catalog_ids:
            catalog_ids.append(c_id)
            item = self.compile_type_1_item(response)
            request = Request(constants.get_documents_info_url.format(
                response.css(constants.product_type_1_formatted_sku).extract_first()),
                              callback=self.parse_documents_info)
            request.meta['item'] = item
            return request

    def get_functions(self, response):
        if response.css(constants.product_type_1_functions_check):
            return [{'title': link.text, 'url': link.url} for link in
                    LinkExtractor(allow=(), restrict_css=(constants.product_type_1_functions,)).extract_links(response)]

    def get_processes(self, response):
        if response.css(constants.product_type_1_processes_check):
            return [{'title': link.text, 'url': link.url} for link in
                    LinkExtractor(allow=(), restrict_css=(constants.product_type_1_processes,)).extract_links(response)]

    def get_secondaries(self, response):
        if response.css(constants.product_type_1_secondaries_check):
            return [{'title': link.text, 'url': link.url} for link in
                    LinkExtractor(allow=(), restrict_css=(constants.product_type_1_secondaries,)).extract_links(
                        response)]

    def get_image_objects(self, response):
        result = []
        for image in response.css(constants.product_type_1_images):
            result.append({
                'title': image.css(constants.product_type_1_image_title).extract_first(),
                'url': image.css(constants.product_type_1_image_url).extract_first(),
                'description': image.css(constants.product_type_1_image_description).extract_first()
            })
        return result

    def get_all_table_data(self, response):
        result = {}
        for table in response.css(constants.product_type_1_specs):
            result.update(
                {clean_str(table.css(constants.product_type_1_specs_data).extract_first()): self.table_to_dict(table)})
        return result

    def table_to_dict(self, response):
        result = {}
        dict_keys = [clean_str(x) for x in response.css(constants.product_type_1_table_to_dict_keys).extract()]
        dict_values = []
        for val in response.css(constants.product_type_1_table_to_dict_values):
            dict_values.append(''.join(list(filter(None, [clean_str(x) for x in val.css(constants.get_all_text).extract()]))))
        for i in range(0, len(dict_keys)):
            result.update({dict_keys[i]: dict_values[i]})
        return result

    def get_product_specifications(self, response):
        return clean_str(response.css(constants.product_type_1_specifications).extract_first())

    def get_background_information(self, response):
        return clean_str(response.css(constants.product_type_1_background_info).extract_first())

    def get_bioinformatics(self, response):
        if response.css(constants.product_type_1_bioinformatics_check):
            return ' '.join(list(
                filter(None, [clean_str(x) for x in response.css(constants.product_type_1_bioinformatics).extract()])))

    def get_brand(self, response):
        return clean_str(response.css(constants.get_brand).extract_first())

    def get_references(self, response):
        references = {}
        for table in response.css(constants.product_type_1_references):
            table_id = table.css(constants.get_attr_id).extract_first()
            references[table_id] = []
            for reference in table.css(constants.get_table_body_tr):
                reference_object = {}
                values = reference.css(constants.get_td)
                reference_object['Species'] = clean_str(values[0].css(constants.get_td_text).extract_first())
                reference_object['Dilution'] = clean_str(values[1].css(constants.get_td_text).extract_first())
                reference_object['Authors'] = clean_str(values[3].css(constants.get_td_text).extract_first())
                reference_object['Publication'] = clean_str(values[4].css(constants.get_td_text).extract_first())
                reference_object['Year'] = clean_str(values[5].css(constants.get_td_text).extract_first())
                description = list(filter(None, [clean_str(x) for x in values[2].css(constants.get_td_text).extract()]))
                if description:
                    reference_object['Description'] = description[0]
                reference_object['Title'] = clean_str(values[2].css(constants.get_a_text).extract_first())
                reference_object['Url'] = clean_str(values[2].css(constants.get_a_attr_href).extract_first())
                references[table_id].append(reference_object)
        return references

    def parse_documents_info(self, response):
        document_info = json.loads(response.body.decode('utf-8'))
        item = response.meta['item']
        documents = {}
        documents['faqs'] = self.get_product_faqs(document_info)
        documents['manuals_and_protocols'] = self.get_product_manuals(document_info)
        documents['product_literature'] = self.get_product_brochures(document_info)
        documents['coa'] = self.get_product_coas(document_info)
        documents['Material Safety Data Sheets'] = self.get_product_msds(document_info)
        item['documents'] = documents
        yield item

    def compile_form_data_list_type_1(self, response):
        v_num = response.css(constants.list_1_body_script_tag).re(constants.v_num_regex)[0]
        return {
            'jsonSearchCriteria': str({
                'productTypeSelect': response.css(constants.get_original_product_type).extract_first(),
                'keyword': '',
                'isSimpleAny': 'false',
                'antibodyGeneFamilyPage': 'false',
                'antibodyProteinFamilyPage': 'false',
                'antibodyPantherClass': '',
                'antibodySortByValue': 'Relevancy',
                'species': response.css(constants.get_original_species).extract_first(),
                'sequence': '',
                'targetTypeSelect': response.css(constants.get_originat_target_type).extract_first(),
                'additionalFilter': '',
                'chrNum': '-',
                'chrStart': '',
                'chrStop': '',
                'multiChromoSome': '',
                'multiSequenceNames': '',
                'multiSequence': '',
                'flankingGenes': '',
                'domain': "LT",
                'filters': ''
            }),
            'numHits': '25',
            'offset': '25',
            'rev': v_num,
            'orSearch': 'false',
            'isConfiguratorFlag': 'false',
            'inventoriedOnlyFlag': 'false',
            'pluginName': ''
        }

    def compile_type_1_item(self, response):
        cat_ids = self.get_product_cat_ids(response)
        sizes = self.get_product_sizes(response)
        prices = self.get_product_prices(response)
        item = ThermoType1Item()
        item['name'] = response.css(constants.get_name_1).extract_first()
        item['category'] = list(
            filter(None,
                   [x.strip() for x in
                    response.css(constants.breadcrumbs_sel).extract()]))
        item['images'] = self.get_image_objects(response)
        item['url'] = response.url
        item['functions'] = self.get_functions(response)
        item['processes'] = self.get_processes(response)
        item['suggested_secondaries'] = self.get_secondaries(response)
        item['specifications'] = self.get_product_specifications(response)
        item['background_information'] = self.get_background_information(response)
        item['details'] = self.get_all_table_data(response)
        item['bioinformatics'] = self.get_bioinformatics(response)
        item['references'] = self.get_references(response)
        item['brand'] = self.get_brand(response)
        catalog_numbers = []
        for index in range(0, len(cat_ids)):
            catalog_numbers.append(
                {'catalog_number': cat_ids[index], 'price': prices[index], 'unit_size': sizes[index]})
        item['catalog_numbers'] = catalog_numbers
        return item
    
    def get_product_cat_ids(self, response):
        return list(filter(None, [x.strip() for x in response.css(constants.get_cat_ids).extract()]))
    
    def get_product_sizes(self, response):
        return list(filter(None, [x.strip() for x in response.css(constants.get_sizes).extract()]))
    
    def get_product_prices(self, response):
        return list(filter(None, [x.strip() for x in response.css(constants.get_price_amount).extract()])) or list(
            filter(None, [x.strip() for x in response.css(constants.get_price_quote).extract()])) or list(
            filter(None, [x.strip() for x in response.css(constants.get_price_3).extract()]))
    
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

    def get_product_msds(self, document_info):
        if 'msdsList' in document_info['searchResults']:
            msdss = []
            for msds in document_info['searchResults']['msdsList']:
                msdss.append({'title': msds['title'], 'url': msds['msdsFiles']})
            return msdss

def clean_str(input_str):
    if input_str:
        return str(re.sub('\s+', ' ', input_str.replace(u'\xa0', ' ')).strip())
