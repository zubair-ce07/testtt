"""Utilty functions"""


def remove_relativness(link_str):
    """This function removes the '../' from start of url"""
    # or re.sub("^../|/$", "", link_str)
    return link_str.strip("../")
