import argparse
import json
import collections


def value_difference(value_one, value_two, input_json, file_one, file_two):
    dict_of_difference = {}
    if ((collections.Counter(value_one) != collections.Counter(value_two)) or (value_one != value_two)):
        dict_of_difference[file_two] = value_two
        dict_of_difference[file_one] = value_one
        dict_of_difference["field"] = input_json
    return dict_of_difference


def document_matcher(document_one, document_two, file_one_name, file_two_name):
    """This function given two documents returns the filed differences of the two documents
    (in the form of a dict) if the documents matched the conditions"""
    document_difference = {}
    if ((document_one.get('slug') == document_two.get('slug'))
            or (document_one.get('source_url') == document_two.get('source_url'))):
        keys_to_be_skipped = {'ons3'}
        list_of_all_diffs = []
        for document_one_key in document_one:
            if document_one_key not in keys_to_be_skipped:
                difference = value_difference(document_one.get(document_one_key),
                                              document_two.get(document_one_key), document_one_key,
                                              file_one_name, file_two_name)
                if difference:
                    list_of_all_diffs.append(difference)
        document_difference["field_diffs"] = list_of_all_diffs
    return document_difference


def unmatched_documents_data(document):
    unmatched_document_data = {}
    unmatched_document_data["source_url"] = document.get("source_url")
    unmatched_document_data["blob_name"] = document.get("blob_name")
    unmatched_document_data["name"] = document.get("name")
    unmatched_document_data["extension"] = document.get("extension")
    unmatched_document_data["slug"] = document.get("slug")
    return unmatched_document_data


def filing_matcher(filing_one, filing_two, file_one_name, file_two_name):
    """given two filings matches them and then returns a dict containing all the differences in the two filings"""
    filing_difference = {}
    if ((filing_one.get('slug') == filing_two.get('slug'))
         or (filing_one.get('state_id') and (filing_one.get('state_id') == filing_two.get('state_id')))
         or ((filing_one.get('description') == filing_two.get('description')) and (filing_one.get('filed_on') == filing_two.get('filed_on')))):
        keys_skipable = {'documents'}
        all_diffs = []
        for each_filing_key in filing_one:
            if each_filing_key not in keys_skipable:
                difference = value_difference(filing_one.get(each_filing_key), filing_two.get(each_filing_key), each_filing_key,
                                     file_one_name, file_two_name)
                if difference:
                    all_diffs.append(difference)
        filing_difference["field_diffs"] = all_diffs
        first_documents = filing_one["documents"]
        second_documents = filing_two["documents"]
        document_diffs_list = []
        document_diffs_dict = {}
        document_data = []
        for each_doc in first_documents:
            no_match_found = 1
            for every_doc in second_documents:
                match_result = document_matcher(each_doc, every_doc, file_one_name, file_two_name)
                if match_result:
                    no_match_found = 0
                    document_diffs_list.append(match_result)
            if no_match_found:
                document_data.append(unmatched_documents_data(each_doc))
        for each_doc in second_documents:
            no_match_found = 1
            for every_doc in first_documents:
                match_result = document_matcher(each_doc, every_doc, file_one_name, file_two_name)
                if match_result:
                    no_match_found = 0
            if no_match_found:
                document_data.append(unmatched_documents_data(each_doc))
        if document_data:
            old_docs = {}
            old_docs["old documents"] = document_data
            document_diffs_dict["documents not matched"] = old_docs
        document_diffs_dict["field_diffs"] = document_diffs_list
        filing_difference["document_diffs"] = document_diffs_dict
    return filing_difference


def docket_matcher(docket_one, docket_two, skip_fields, file_one_name, file_two_name):
    """given two dockets matches them and then stores the difference as a dictionary in output"""
    docket_difference = {}
    if docket_one['slug'] == docket_two['slug']:
        docket_diffs = []
        for each_item in docket_one:
            if each_item not in skip_fields:
                difference = value_difference(docket_one[each_item], docket_two.get(each_item), each_item,
                                              file_one_name, file_two_name)
                if difference:
                    docket_diffs.append(difference)
        docket_difference['meta_changes'] = docket_diffs
        first_filings = docket_one["filings"]
        second_filings = docket_two["filings"]
        filing_diffs_list = []
        filing_diffs_dict = {}
        for each_element in first_filings:
            for every_element in second_filings:
                result_of_match = filing_matcher(each_element, every_element, file_one_name, file_two_name)
                if result_of_match:
                    filing_diffs_list.append(result_of_match)
        filing_diffs_dict["field_diffs"] = filing_diffs_list
        docket_difference['filing_changes'] = filing_diffs_dict
    return docket_difference


def main():
    """The main function of the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","-input_file", help = "input the name of the output JSON file")
    parser.add_argument("firstfile", help = "input the first JSON file")
    parser.add_argument("secondfile", help = "input the second JSON file")
    args = parser.parse_args()
    with open(args.firstfile) as f:
        docket_one = json.load(f)
    with open(args.secondfile) as f:
        docket_two = json.load(f)
    file_one_name = (args.firstfile.split('.'))[0]
    file_two_name = (args.secondfile.split('.'))[0]
    skip_fields = {'run_id', 'uploaded', 'modified', 'crawled_at', 'end_time', '_id','job_id', 'request_fingerprint',
                   'start_time', 'spider_name', 'filings'}
    docket_differences = docket_matcher(docket_one, docket_two, skip_fields, file_one_name, file_two_name)
    if args.o:
        with open(args.o, 'w') as output_json:
            json.dump(docket_differences, output_json)
    else:
        print(docket_differences)


if __name__ == "__main__":
    main()
