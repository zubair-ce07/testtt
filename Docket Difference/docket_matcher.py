import argparse
import json
import collections

FILE_ONE_NAME = "local"
FILE_TWO_NAME = "remote"


def value_difference(value_one, value_two, field_of_difference):
    value_difference = {}
    if (collections.Counter(value_one) != collections.Counter(value_two)) or (value_one != value_two):
        value_difference[FILE_TWO_NAME] = value_two
        value_difference[FILE_ONE_NAME] = value_one
        value_difference["field"] = field_of_difference
    return value_difference


def filing_match(filing_one, filing_two):
    return True if ((filing_one.get("slug") == filing_two.get("slug")) or
            (filing_one.get("state_id", 1) == filing_two.get("state_id")) or
            ((filing_one.get("description") == filing_two.get("description")) and
                 (filing_one.get("filed_on") == filing_two.get("filed_on")))) else False


def document_match(document_one, document_two):
    return True if ((document_one.get("slug") == document_two.get("slug")) or
            (document_one.get("source_url") == document_two.get("source_url"))) else False


def document_matcher(document_one, document_two):
    """This function given two documents returns the filed differences of the two documents
    (in the form of a dict) if the documents matched the conditions"""
    document_difference = {}
    if document_match(document_one, document_two):
        skip_fields = {"ons3"}
        all_diffs = []
        for document_one_key in document_one:
            if document_one_key not in skip_fields:
                difference = value_difference(document_one.get(document_one_key),
                                              document_two.get(document_one_key), document_one_key)
                if difference:
                    all_diffs.append(difference)
        document_difference["field_diffs"] = all_diffs
    return document_difference


def unmatched(matching_function, first_item, second_item):
    unmatched = []
    for each_item in first_item:
        no_match_found = True
        for every_item in second_item:
            match_result = matching_function(each_item, every_item)
            if match_result:
                no_match_found = False
        if no_match_found:
            unmatched.append(each_item)
    return unmatched

def filing_matcher(filing_one, filing_two):
    """given two filings matches them and then returns a dict containing all the differences in the two filings"""
    filing_difference = {}
    if filing_match(filing_one, filing_two):
        skip_fields = {"documents"}
        all_diffs = []
        for each_filing_key in filing_one:
            if each_filing_key not in skip_fields:
                difference = value_difference(filing_one.get(each_filing_key), filing_two.get(each_filing_key), each_filing_key)
                if difference:
                    all_diffs.append(difference)
        filing_difference["field_diffs"] = all_diffs
        first_documents = filing_one["documents"]
        second_documents = filing_two["documents"]
        all_document_diffs = []
        document_differences = {}
        unmatched_documents = []
        for each_doc in first_documents:
            for every_doc in second_documents:
                match_result = document_matcher(each_doc, every_doc)
                if match_result:
                    all_document_diffs.append(match_result)
        unmatched_new_documents = unmatched(document_match, first_documents, second_documents)
        unmatched_old_documents = unmatched(document_match, second_documents, first_documents)
        if unmatched_old_documents:
            old_docs = {}
            old_docs["old documents"] = unmatched_old_documents
            unmatched_documents.append(old_docs)
            document_differences["documents not matched"] = unmatched_documents
        if unmatched_new_documents:
            new_docs = {}
            new_docs["new documents"] = unmatched_new_documents
            unmatched_documents.append(new_docs)
            document_differences["documents not matched"] = unmatched_documents
        document_differences["field_diffs"] = all_document_diffs
        filing_difference["document_diffs"] = document_differences
    return filing_difference


def docket_matcher(docket_one, docket_two, skip_fields):
    """given two dockets matches them and then stores the difference as a dictionary in output"""
    docket_difference = {}
    if docket_one["slug"] == docket_two["slug"]:
        docket_diffs = []
        for each_item in docket_one:
            if each_item not in skip_fields:
                difference = value_difference(docket_one[each_item], docket_two.get(each_item), each_item)
                if difference:
                    docket_diffs.append(difference)
        docket_difference["meta_changes"] = docket_diffs
        first_filings = docket_one["filings"]
        second_filings = docket_two["filings"]
        all_filing_diffs = []
        filing_differences = {}
        unmatched_filings = []
        for filing_one in first_filings:
            for filing_two in second_filings:
                result_of_match = filing_matcher(filing_one, filing_two)
                if result_of_match:
                    all_filing_diffs.append(result_of_match)
        unmatched_new_filings = unmatched(filing_match, first_filings, second_filings)
        unmatched_old_filings = unmatched(filing_match, second_filings, first_filings)
        if unmatched_old_filings:
            old_filings = {}
            old_filings["old filings"] = unmatched_filings
            unmatched_filings.append(old_filings)
            filing_differences["filings not matched"] = unmatched_filings
        if unmatched_new_filings:
            new_filings = {}
            new_filings["new filings"] = unmatched_filings
            unmatched_filings.append(new_filings)
            filing_differences["filings not matched"] = unmatched_filings
        filing_differences["field_diffs"] = all_filing_diffs
        docket_difference["filing_changes"] = filing_differences
    return docket_difference


def main():
    """The main function of the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="name of the output JSON file")
    parser.add_argument("local", help="input the first JSON file")
    parser.add_argument("remote", help="input the second JSON file")
    args = parser.parse_args()
    with open(args.local) as f:
        docket_one = json.load(f)
    with open(args.remote) as f:
        docket_two = json.load(f)
    skip_fields = {"run_id", "uploaded", "modified", "crawled_at", "end_time", "_id", "job_id", "request_fingerprint",
                   "start_time", "spider_name", "filings"}
    docket_differences = docket_matcher(docket_one, docket_two, skip_fields)
    if args.output:
        with open(args.output, "w") as output_json:
            json.dump(docket_differences, output_json)
    else:
        print(docket_differences)


if __name__ == "__main__":
    main()
