"""
Helper functions for re-usability
"""


def get(response, path):
    """
    Returns the data fetched from response by using css selector
    :param response: response object to use by selector
    :param path: css selector path to use
    :return: list of data returned by css selector
    """
    return response.css(path).extract()


def get_first(response, path):
    """
    Returns the first element fetched from response
    by using css selector
    :param response: response object to use by selector
    :param path: css selector path to use
    :return: first item of list returned by css selector
    """
    return response.css(path).extract_first()
