import json
import re

GENDERS = ['MEN', 'WOMEN']
UNWANTED_CHARS = ['', '/']
VALUE_EXTRACTOR_FROM_KEY = re.compile(r'(?:.*_|_)(.*)')


def clean_string(raw_text):
    raw_text = raw_text.replace('\'', '"')
    return json.loads(raw_text)


def clean_data(raw_data):
    if isinstance(raw_data, list):
        raw_data = [d.strip() for d in raw_data]
        clean_data = []
        for data in raw_data:
            if data not in UNWANTED_CHARS:
                clean_data.append(data)
        return clean_data

    clean_data = raw_data.strip()
    if clean_data not in UNWANTED_CHARS:
        return clean_data
    return None


def remove_unicode_characters(raw_data):
    return [re.sub(r'[^\x00-\x7F]+', ' ', text) for text in raw_data]
