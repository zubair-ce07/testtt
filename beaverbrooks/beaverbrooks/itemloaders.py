from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def _product_specification_parser(self, input_specs):
    """
    We get a specifications list, we need to arrange them in key-value
    pairs to make them meaningful

    Arguments:
        input_specs (list): All the salient properties of the product

    Returns:
        (dict): specifications in key-value pair form
    """

    specifications_map = dict()
    for input_spec in input_specs:
        result = input_spec.strip().split('\n')
        specifications_map[result[0]] = result[2].strip()
    return specifications_map


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    product_specification_in = MapCompose(remove_tags)
    product_specification_out = _product_specification_parser
