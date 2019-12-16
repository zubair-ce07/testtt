from argparse import ArgumentTypeError
from urllib.parse import urlparse


def validate_url_as_arg(url_to_check):
    parsed = urlparse(url_to_check)
    if parsed.netloc and parsed.scheme:
        return parsed.geturl()
    else:
        msg = f'{url_to_check} is not a valid url'
        raise ArgumentTypeError(msg)
