from scrapy.spiders import CrawlSpider, Rule
import re
import json
from scrapy.linkextractors import LinkExtractor
from ThermoFisher.spiders import thermo_constants as constants
from ThermoFisher.items import ThermoType1Item, ThermoType2Item, ThermoType3Item
from scrapy import Request

# a global array of catalog_ids is maintained to prevent duplication
catalog_ids = []


class ThermoSpider(CrawlSpider):
    name = "thermo_all"
    download_delay = 2.0
    allowed_domains = ["thermofisher.com"]
    start_urls = [
        'http://www.thermofisher.com/order/catalog/en/US/adirect/lt?cmd=IVGNcatDisplayCategory',
        ]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('div.block.group h3>a',)), follow=True),
        Rule(LinkExtractor(allow=(), restrict_css=('form>table#pagination:nth_child(3) a',)), follow=True),
        Rule(LinkExtractor(allow=(), restrict_css=('table.datatable tbody>tr>td:nth_child(1)>a',)), callback="parse_items"),
    )

    def parse_items(self, response):
        diff = response.css(constants.product_type).extract_first()
        # diff identifies which type of product it is
        if diff:
            if 'Details' in diff:
                # type 1 item
                yield self.parse_type_1_items(response)
            elif 'overview' in diff:
                if response.css(constants.product_type_2):
                    # type 3 item
                    data_unclean = clean_str(response.xpath(constants.get_type_3_product_data).extract_first())
                    data = re.findall('{ commerceBoxData: *(.*?)} *</script>', data_unclean)
                    if data:
                        json_feed = data[0]
                        item_dict = json.loads(json_feed)
                        yield self.compile_type_3_item(item_dict, response)
                else:
                    # type 2 item
                    request = self.parse_type_2_items(response)
                    yield request

# Type 1 Item methods

    def parse_type_1_items(self, response):
        c_id = response.css(constants.get_cid_1).extract_first()
        if c_id not in catalog_ids:
            catalog_ids.append(c_id)
            item = self.compile_type_1_item(response)
            request = Request(
                constants.get_documents_info_url.format(response.css(constants.product_type_1_formatted_sku).
                                                        extract_first()), callback=self.parse_documents_info)
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
        if 'searchResults' in document_info:
            documents = {'faqs': self.get_product_faqs(document_info),
                         'manuals_and_protocols': self.get_product_manuals(document_info),
                         'product_literature': self.get_product_brochures(document_info),
                         'coa': self.get_product_coas(document_info),
                         'Material Safety Data Sheets': self.get_product_msds(document_info)}
            item['documents'] = documents
        yield item

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
                msds_obj = {'title': msds['title']}
                if 'msdsFiles' in msds:
                    msds_obj['url'] = msds['msdsFiles']
                elif 'internalURL' in  msds:
                    msds_obj['url'] = msds['internalURL']
                msdss.append(msds_obj)
            return msdss

# Type 2 Item methods

    def parse_type_2_items(self, response):
        c_id = clean_str(response.css(constants.get_cid_2).extract_first())
        if c_id not in catalog_ids:
            catalog_ids.append(c_id)
            item = self.compile_type_2_item(response)
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

    def compile_type_2_item(self, response):
        item = ThermoType2Item()
        item['brand'] = self.get_brand(response)
        item['name'] = self.get_product_name(response)
        item['description'] = self.get_product_description(response)
        item['category'] = self.get_product_category(response)
        item['recommended_products'] = self.get_recommended_products(response)
        item['specifications'] = self.get_product_specifications_type_2(response)
        item['contents'] = self.get_product_contents(response)
        item['image_urls'] = self.get_product_images(response)
        item['related_applications'] = self.get_product_related_applications(response)
        item['url'] = response.url
        return item

    def get_product_name(self, response):
        return ''.join(response.css(constants.get_name_2).extract())

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

    def get_product_specifications_type_2(self, response):
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

# Type 3 Item methods

    def compile_type_3_item(self, item_dict, response):
        if self.check_catalog_ids(item_dict):
            item = ThermoType3Item()
            item['brand'] = self.get_brand(response)
            item['name'] = self.get_product_name(response)
            item['description'] = self.get_product_description(response)
            item['category'] = self.get_product_category(response)
            item['images'] = self.get_product_images_type_3(response)
            item['url'] = response.url
            catalog_numbers = self.compile_catalogs_type_3(item_dict)
            item['catalog_numbers'] = catalog_numbers
            url_parameters = ''
            for catalog in catalog_numbers:
                url_parameters = '{0},{1}'.format(url_parameters, catalog['catalog_number'])
            url_parameters = url_parameters.strip(',')
            request = Request(constants.get_price_info_url.format(url_parameters), callback=self.parse_price_info)
            request.meta['item'] = item
            family_id = response.css(constants.get_family_id).extract_first().strip('pfp-')
            if family_id:
                request.meta['f_id'] = family_id
            else:
                request.meta['c_id'] = response.css(constants.get_cid_type_3).extract_first()
            return request

    def parse_price_info(self, response):
        products = json.loads(response.body.decode('utf-8'))
        item = response.meta['item']
        if 'message' in products:
            for product in products['products']:
                for catalog in item['catalog_numbers']:
                    if catalog['catalog_number'] == product['sku']:
                        catalog.update({
                            'price': product['listPrice']['value'] if product['pricingAccess'] == "Orderable" else
                            product['pricingAccess'],
                            'currency': product['currency'] if 'currency' in product else None
                        }),
                        break
            if 'f_id' in response.meta:
                request = Request(constants.get_documents_info_url_multiple.format(response.meta['f_id']),
                                  callback=self.parse_documents_info)
            else:
                request = Request(constants.get_documents_info_url.format(response.meta['c_id']),
                                  callback=self.parse_documents_info)
            request.meta['item'] = item
            yield request

    def check_catalog_ids(self, item_dict):
        for c_item in item_dict['products']:
            if c_item['productData']['sku'] not in catalog_ids:
                return True
        return False

    def compile_catalogs_type_3(self, item_dict):
        catalog_numbers = []
        for c_item in item_dict['products']:
            if c_item['productData']['sku'] not in catalog_ids:
                catalog_ids.append(c_item['productData']['sku'])
                specifications = {}
                for spec in c_item['productData']['specifications']:
                    specifications.update(
                        {
                            spec['name']: spec['values']
                        }
                    )
                catalog = {
                        'catalog_number': c_item['productData']['sku'],
                        'unit_size': c_item['productData']['size'],
                        'specifications': specifications
                    }
                catalog.update(c_item['productData']['orderingAttributes'])
                catalog_numbers.append(catalog)
        return catalog_numbers

    def get_product_images_type_3(self, response):
        return response.css(constants.get_images_type_3).extract()


def clean_str(input_str):
    if input_str:
        return str(re.sub('\s+', ' ', input_str.replace(u'\xa0', ' ')).strip())
