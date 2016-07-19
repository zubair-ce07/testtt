import argparse
import json
import collections

_output = dict()
_file_one_name = ""
_file_two_name = ""

def document_matcher(document_one, document_two):
    "This function given two documents of type lists containing dict elements returns\
    the filed differences of the two documents (in the form of a dict) if the documents\
    matched the conditions otherwise it returns 0"
    if ((document_one.get('slug') == document_two.get('slug'))
        or (document_one.get('source_url') == document_two.get('source_url'))):
        keys_to_be_skipped = {'ons3'}
        my_dict_result = dict()
        list_of_all_diffs = []
        for each_key in document_one:
            if not each_key in keys_to_be_skipped:
                if type(document_one[each_key]) is list:
                    if (collections.Counter(document_one.get(each_key)) != collections.Counter(
                            document_two.get(each_key))):
                        dict_of_each_difference = dict()
                        dict_of_each_difference[_file_two_name] = document_two.get(each_key)
                        dict_of_each_difference[_file_one_name] = document_one.get(each_key)
                        dict_of_each_difference["field"] = each_key
                        list_of_all_diffs.append(dict_of_each_difference)
                else:
                    if (document_one.get(each_key) != document_two.get(each_key)):
                        dict_of_each_difference = dict()
                        dict_of_each_difference[_file_two_name] = document_two.get(each_key)
                        dict_of_each_difference[_file_one_name] = document_one.get(each_key)
                        dict_of_each_difference["field"] = each_key
                        list_of_all_diffs.append(dict_of_each_difference)
        my_dict_result["field_diffs"] = list_of_all_diffs
        return my_dict_result
    else:
        return 0


def filing_matcher(filing_one, filing_two):
    "given two filings matches them and then returns a dict containing all the differences in the two filings"
    if ((filing_one.get('slug') == filing_two.get('slug'))
         or (filing_one.get('state_id') and (filing_one.get('state_id')==filing_two.get('state_id')))
         or ((filing_one.get('description') == filing_two.get('description')) and (filing_one.get('filed_on')==filing_two.get('filed_on')))):
        keys_skippable = {'documents'}
        my_dict = dict()
        all_diffs=[]
        for each_filing_key in filing_one:
            if not each_filing_key in keys_skippable:
                if type(filing_one[each_filing_key]) is list:
                    if (collections.Counter(filing_one.get(each_filing_key)) != collections.Counter(filing_two.get(each_filing_key))):
                        each_diff = dict()
                        each_diff[_file_two_name] = filing_two.get(each_filing_key)
                        each_diff[_file_one_name] = filing_one.get(each_filing_key)
                        each_diff["field"] = each_filing_key
                        all_diffs.append(each_diff)
                else:
                    if (filing_one.get(each_filing_key) != filing_two.get(each_filing_key)):
                        each_diff=dict()
                        each_diff[_file_two_name] = filing_two.get(each_filing_key)
                        each_diff[_file_one_name] = filing_one.get(each_filing_key)
                        each_diff["field"] = each_filing_key
                        all_diffs.append(each_diff)
        my_dict["field_diffs"] = all_diffs
        first_documents = filing_one["documents"]
        second_documents = filing_two["documents"]
        document_diffs_list = []
        document_diffs_dict = dict()
        for each_doc in first_documents:
            for every_doc in second_documents:
                match_result = document_matcher(each_doc, every_doc)
                if (match_result):
                    document_diffs_list.append(match_result)
        document_diffs_dict["field_diffs"] = document_diffs_list
        my_dict["document_diffs"] = document_diffs_dict
        return my_dict
    else:
        return 0


def main():
    "The main function of the program"
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="input the name of the output JSON file")
    parser.add_argument("firstfile", help="input the first JSON file")
    parser.add_argument("secondfile", help="input the second JSON file")
    args = parser.parse_args()
    with open(args.firstfile) as f:
        docket_one = json.load(f)
    with open(args.secondfile) as f:
        docket_two = json.load(f)
    _file_one_name = (args.firstfile.split('.'))[0]
    _file_two_name = (args.secondfile.split('.'))[0]
    skip_fields = {'run_id','uploaded','modified','crawled_at','end_time','_id','job_id','request_fingerprint',
                   'start_time','spider_name','filings'}
    if (docket_one['slug']==docket_two['slug']):
        docket_diffs = []
        for each_json in docket_one:
            if not each_json in skip_fields:
                if type(docket_one[each_json]) is list:
                    if (collections.Counter(docket_one[each_json]) != collections.Counter(docket_two.get(each_json))):
                        difference = dict()
                        difference[_file_two_name] = docket_two.get(each_json)
                        difference[_file_one_name]=docket_one[each_json]
                        difference["field"] = each_json
                        docket_diffs.append(difference)

                else:
                    if (docket_one[each_json] != docket_two.get(each_json)):
                        difference = dict()
                        difference[_file_two_name] = docket_two.get(each_json)
                        difference[_file_one_name] = docket_one[each_json]
                        difference["field"] = each_json
                        docket_diffs.append(difference)
        _output['meta_changes']=docket_diffs
        first_filings = docket_one["filings"]
        second_filings = docket_two["filings"]
        filing_diffs_list = []
        filing_diffs_dict = dict()
        for each_element in first_filings:
            for every_element in second_filings:
                result_of_match = filing_matcher(each_element,every_element)
                if (result_of_match):
                    filing_diffs_list.append(result_of_match)
        filing_diffs_dict["field_diffs"] = filing_diffs_list
        _output['filing_changes']=filing_diffs_dict
        if args.o:
            with open(args.o, 'w') as output_json:
                json.dump(_output, output_json)
        else:
            print(_output)


if __name__ == "__main__": main()