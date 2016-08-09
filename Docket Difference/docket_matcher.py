import argparse
import json
import collections
import itertools

FILE_ONE_NAME = "local"
FILE_TWO_NAME = "remote"


def value_difference(value_one, value_two, field_of_difference):
    value_difference = {}
    if (collections.Counter(value_one) != collections.Counter(value_two)) or (value_one != value_two):
        value_difference[FILE_TWO_NAME] = value_two
        value_difference[FILE_ONE_NAME] = value_one
        value_difference["field"] = field_of_difference
    return value_difference


def filing_matched(filing_one, filing_two):
    return True if ((filing_one.get("slug") == filing_two.get("slug")) or
            (filing_one.get("state_id", 1) == filing_two.get("state_id")) or
            ((filing_one.get("description") == filing_two.get("description")) and
                 (filing_one.get("filed_on") == filing_two.get("filed_on")))) else False


def document_matched(document_one, document_two):
    return True if ((document_one.get("slug") == document_two.get("slug")) or
            (document_one.get("source_url") == document_two.get("source_url"))) else False


def document_matcher(document_one, document_two):
    """This function given two documents returns the filed differences of the two documents
    (in the form of a dict) if the documents matched the conditions"""
    document_difference = {}
    if document_matched(document_one, document_two):
        skip_fields = {"ons3"}
        remove_fields(document_one,skip_fields)
        all_diffs = []
        for document_one_key in document_one:
            difference = value_difference(document_one.get(document_one_key),
                                            document_two.get(document_one_key), document_one_key)
            if difference:
                all_diffs.append(difference)
        document_difference["field_diffs"] = all_diffs
    return document_difference


def filing_matcher(local_filing, remote_filing):
    """given two filings matches them and then returns a dict containing all the differences in the two filings"""
    filing_difference = {}
    if filing_matched(local_filing, remote_filing):
        skip_fields = {"documents"}
        local_documents = local_filing["documents"]
        remote_documents = remote_filing["documents"]
        remove_fields(local_filing, skip_fields)
        all_diffs = []
        for each_filing_key in local_filing:
                difference = value_difference(local_filing.get(each_filing_key), remote_filing.get(each_filing_key), each_filing_key)
                if difference:
                    all_diffs.append(difference)
        filing_difference["field_diffs"] = all_diffs
        all_document_diffs = []
        document_differences = {}
        unmatched_documents = []
        documents_cartesian_product = itertools.product(local_documents, remote_documents)
        for each_combination in documents_cartesian_product:
            match_result = document_matcher(each_combination[0], each_combination[1])
            if match_result:
                all_document_diffs.append(match_result)
                try:
                    local_documents.remove(each_combination[0])
                    remote_documents.remove(each_combination[1])
                except ValueError:
                    pass
        if remote_documents:
            old_docs = {}
            old_docs["old documents"] = remote_documents
            unmatched_documents.append(old_docs)
            document_differences["documents not matched"] = unmatched_documents
        if local_documents:
            new_docs = {}
            new_docs["new documents"] = local_documents
            unmatched_documents.append(new_docs)
            document_differences["documents not matched"] = unmatched_documents
        document_differences["field_diffs"] = all_document_diffs
        filing_difference["document_diffs"] = document_differences
    return filing_difference


def remove_fields(input_dictionary, fields):
    for field in fields:
        if field in input_dictionary:
            del input_dictionary[field]


def docket_matcher(local_docket, remote_docket):
    """given two dockets matches them and then stores the difference as a dictionary in output"""
    docket_difference = {}
    skip_fields = {"run_id", "uploaded", "modified", "crawled_at", "end_time", "_id", "job_id", "request_fingerprint",
                   "start_time", "spider_name", "filings"}
    local_filings = local_docket["filings"]
    remote_filings = remote_docket["filings"]
    remove_fields(local_docket, skip_fields)
    if local_docket["slug"] == remote_docket["slug"]:
        docket_diffs = []
        for each_item in local_docket:
            difference = value_difference(local_docket[each_item], remote_docket.get(each_item), each_item)
            if difference:
                docket_diffs.append(difference)
        docket_difference["meta_changes"] = docket_diffs
        all_filing_diffs = []
        filing_differences = {}
        unmatched_filings = []
        filings_cartesian_product = list(itertools.product(local_filings, remote_filings))
        for product in filings_cartesian_product:
            result_of_match = filing_matcher(product[0], product[1])
            if result_of_match:
                all_filing_diffs.append(result_of_match)
                try:
                    local_filings.remove(product[0])
                    remote_filings.remove(product[1])
                except ValueError:
                    pass
        if remote_filings:
            old_filings = {}
            old_filings["old filings"] = remote_filings
            unmatched_filings.append(old_filings)
            filing_differences["filings not matched"] = unmatched_filings
        if local_filings:
            new_filings = {}
            new_filings["new filings"] = local_filings
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
        local_docket = json.load(f)
    with open(args.remote) as f:
        remote_docket = json.load(f)
    docket_differences = docket_matcher(local_docket, remote_docket)
    if args.output:
        with open(args.output, "w") as output_json:
            json.dump(docket_differences, output_json)
    else:
        print(docket_differences)


if __name__ == "__main__":
    main()
