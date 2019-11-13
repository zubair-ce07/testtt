import json
import re

GENDERS = ['MEN', 'WOMEN']
UNWANTED_CHARS = ['', '/']
VALUE_EXTRACTOR_FROM_KEY = re.compile(r'(?:.*_|_)(.*)')


def clean_string_and_make_json(raw_text):
    raw_text = raw_text.replace('\'', '"')
    return json.loads(raw_text)


def remove_unwanted_spaces(raw_data):
    if type(raw_data) is list:
        return [d.strip() for d in raw_data]
    return raw_data.strip()


def remove_empty_strings_or_unwanted_characters(raw_data):
    clean_data = []
    for data in raw_data:
        if data not in UNWANTED_CHARS:
            clean_data.append(data)
    return clean_data


def remove_unicode_characters(raw_data):
    return [re.sub(r'[^\x00-\x7F]+', ' ', text) for text in raw_data]
