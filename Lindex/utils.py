import re


def clean_text(self, description):
    return [re.sub('\s+', ' ', text).strip() for text in description if text.strip()]


def clean_category(self, text):
    return text[0].split('/')


def clean_currency(self, text):
    return "".join(re.findall(r"[^\d. ]", text[0]))
