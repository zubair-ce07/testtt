import re


def clean_text(self, description):
    return [re.sub('\s+', ' ', text) for text in description if text.strip()]


def clean_category(self, text):
    return text[0].split('/')
